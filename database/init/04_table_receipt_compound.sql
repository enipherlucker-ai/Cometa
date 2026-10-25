CREATE TABLE payment_statistic.receipt_compound
(
    id          SERIAL PRIMARY KEY,
    name        TEXT           NOT NULL,
    receipt_id  INTEGER        NOT NULL REFERENCES payment_statistic.receipt (id),
    user_id     INTEGER        NOT NULL REFERENCES payment_statistic.users (id),
    category_id INTEGER        NOT NULL REFERENCES payment_statistic.categories (id),
    vat         INTEGER        NOT NULL,
    vat_sum     NUMERIC(8, 2)  NOT NULL,
    price       NUMERIC(8, 2)  NOT NULL,
    quantity    NUMERIC(10, 3) NOT NULL,
    sum         NUMERIC(8, 2)  NOT NULL
);

COMMENT ON TABLE payment_statistic.receipt_compound
    IS 'Товарные позиции кассовых чеков';

COMMENT ON COLUMN payment_statistic.receipt_compound.id
    IS 'Уникальный идентификатор позиции чека';

COMMENT ON COLUMN payment_statistic.receipt_compound.name
    IS 'Наименование товара или услуги';

COMMENT ON COLUMN payment_statistic.receipt_compound.receipt_id
    IS 'Идентификатор чека, к которому относится позиция';

COMMENT ON COLUMN payment_statistic.receipt_compound.category_id
    IS 'Идентификатор категории товара или услуги';

COMMENT ON COLUMN payment_statistic.receipt_compound.vat
    IS 'Код ставки НДС';

COMMENT ON COLUMN payment_statistic.receipt_compound.vat_sum
    IS 'Сумма НДС по позиции';

COMMENT ON COLUMN payment_statistic.receipt_compound.price
    IS 'Цена за единицу товара или услуги';

COMMENT ON COLUMN payment_statistic.receipt_compound.quantity
    IS 'Количество товара или услуги';

COMMENT ON COLUMN payment_statistic.receipt_compound.sum
    IS 'Общая сумма позиции чека';