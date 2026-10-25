import json
from datetime import datetime
from decimal import Decimal
from collections.abc import Sequence

from fastapi import APIRouter, HTTPException

from app.api.dependencies import (
    ApiCheckReceiptDep,
    ApiLogsDep,
    CategoryRepoDep,
    ReceiptCompoundDep,
    ReceiptDep,
    SessionDep,
    CategorizerDep,
    CurrentUserDep,
)
from app.constants import DEFAULT_CATEGORY_NAME
from app.foreign_api.categorizer import ReceiptCategorizer, CategorizerError
from app.foreign_api.check_receipt import CheckReceipt, CheckReceiptUnavailableError, ReceiptNotFoundError
from app.repositories import ReceiptCompoundRepository, ApiLogsRepository
from app.schemas import ReceiptBase, ReceiptCreated
from app.models.categories import Category

router = APIRouter(tags=["receipt"])


def kopecks_to_rubles(value: int) -> Decimal:
    return Decimal(value) / 100

async def assign_categories(
        names: list[str],
        user_id: int,
        categories: Sequence[Category],
        default_category_id: int,
        receipt_compound: ReceiptCompoundRepository,
        categorizer: ReceiptCategorizer | None,
        api_logs: ApiLogsRepository,
):
    logs_model = {
        "user_id": user_id,
        "is_err": False,
        "service": "openai",
        "method": "[POST]/chat/completions",
        "comment": "Определение групп",
        "input_data": None,
        "output_data": None,
    }
    category_ids = [default_category_id] * len(names)

    known = await receipt_compound.known_categories(
        user_id=user_id,
        names=names,
        exclude_category_id=default_category_id,
    )
    uknown: list[int] = []
    for i, name in enumerate(names):
        if name in known:
            category_ids[i] = known[name]
        else:
            uknown.append(i)

    if not uknown or categorizer is None:
        return category_ids

    unknown_names = [names[i] for i in uknown]
    categories_for_prompt = [
        {"id": g.id, "name": g.name, "description": g.description} for g in categories
    ]
    try:
        answer = await categorizer.categorize(
            names=unknown_names,
            categories=categories_for_prompt,
        )
        output = answer.model_dump_json()

    except CategorizerError as exc:
        answer = None
        output = f"Ошибка: {exc}"
        logs_model["is_err"] = True

    logs_model["input_data"] = f"{unknown_names} ||| {categories_for_prompt}"
    logs_model["output_data"] = output
    await api_logs.logs_add(**logs_model)

    if answer is None:
        return category_ids

    allowed = {g.id for g in categories}
    for item in answer.items:
        if 0 <= item.index < len(uknown) and item.category_id in allowed:
            category_ids[uknown[item.index]] = item.category_id

    return category_ids

@router.post("/create_receipt", response_model=ReceiptCreated, status_code=201)
async def create_receipt(
        data: ReceiptBase,
        api_receipt: ApiCheckReceiptDep,
        api_logs: ApiLogsDep,
        session: SessionDep,
        receipt: ReceiptDep,
        receipt_compound: ReceiptCompoundDep,
        categories: CategoryRepoDep,
        categorized: CategorizerDep,
        current_user: CurrentUserDep,
) -> ReceiptCreated:
    logs_model = {
        "user_id": current_user.id,
        "is_err": False,
        "service": "proverka_cheka_api",
        "method": f"[POST]{CheckReceipt.CHECK_PATH}",
        "comment": "Проверка чека",
        "input_data": data.raw_receipt,
        "output_data": None,
    }

    if await receipt.get_by_qrraw(current_user.id, data.raw_receipt) is not None:
        _error = HTTPException(status_code=409, detail="Этот чек уже добавлен")
        logs_model["is_err"] = True
        logs_model["output_data"] = f"{_error}"
        await api_logs.logs_add(**logs_model)
        await session.commit()
        raise _error

    try:
        response = await api_receipt.check(raw_receipt=data.raw_receipt)
    except ReceiptNotFoundError as exc:
        _error = HTTPException(status_code=400, detail=f"Чек не найден: {exc}")
        logs_model["is_err"] = True
        logs_model["output_data"] = f"{_error}"
        await api_logs.logs_add(**logs_model)
        await session.commit()
        raise _error from exc
    except CheckReceiptUnavailableError as exc:
        _error = HTTPException(status_code=502, detail="Сервис проверки чеков недоступен")
        logs_model["is_err"] = True
        logs_model["output_data"] = f"{_error}"
        await api_logs.logs_add(**logs_model)
        await session.commit()
        raise _error from exc

    logs_model["output_data"] = json.dumps(response, ensure_ascii=False)
    await api_logs.logs_add(**logs_model)

    default_category = await categories.get_by_name(DEFAULT_CATEGORY_NAME)
    if default_category is None:
        _error = HTTPException(status_code=500, detail=f"Нет группы «{DEFAULT_CATEGORY_NAME}» в базе")
        logs_model["is_err"] = True
        logs_model["output_data"] = f"{_error}"
        await api_logs.logs_add(**logs_model)
        await session.commit()
        raise _error

    main_data = response["data"]["json"]

    items = main_data["items"]
    category_ids = await assign_categories(
        names=[item["name"] for item in items],
        user_id=current_user.id,
        categories=await categories.list_for_user(current_user.id),
        default_category_id=default_category.id,
        receipt_compound=receipt_compound,
        categorizer=categorized,
        api_logs=api_logs,
    )

    receipt_object = await receipt.create(
        period=datetime.fromisoformat(main_data["dateTime"]),
        user_id=current_user.id,
        qrraw=data.raw_receipt,
        retail_place=main_data.get("retailPlace"),
        retail_place_address=main_data.get("retailPlaceAddress"),
        total_sum=kopecks_to_rubles(main_data["totalSum"]),
    )
    for item, category_id in zip(items, category_ids, strict=True):
        await receipt_compound.create(
            name=item["name"],
            receipt_id=receipt_object.id,
            user_id=current_user.id,
            category_id=category_id,
            vat=item["nds"],
            vat_sum=kopecks_to_rubles(item.get("ndsSum", 0)),
            price=kopecks_to_rubles(item["price"]),
            quantity=Decimal(str(item["quantity"])),
            sum=kopecks_to_rubles(item["sum"]),
        )
    await session.commit()

    return ReceiptCreated(id=receipt_object.id)

# @router.post("/receipt", response_model=ReceiptCreated)
# async def get