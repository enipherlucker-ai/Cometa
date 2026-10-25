CREATE TABLE payment_statistic.receipt
(
    id                   SERIAL        PRIMARY KEY,
    period               TIMESTAMP     NOT NULL,
    user_id              INTEGER       NOT NULL REFERENCES payment_statistic.users (id),
    qrraw                TEXT,
    retail_place         TEXT,
    retail_place_address TEXT,
    total_sum            NUMERIC(8, 2) NOT NULL,
    UNIQUE (user_id, qrraw)
);

COMMENT ON TABLE payment_statistic.receipt
    IS 'Кассовые чеки пользователей';

COMMENT ON COLUMN payment_statistic.receipt.id
    IS 'Уникальный идентификатор чека';

COMMENT ON COLUMN payment_statistic.receipt.period
    IS 'Дата и время чека';

COMMENT ON COLUMN payment_statistic.receipt.user_id
    IS 'Идентификатор пользователя, которому принадлежит чек';

COMMENT ON COLUMN payment_statistic.receipt.qrraw
    IS 'Исходные данные QR-кода чека';

COMMENT ON COLUMN payment_statistic.receipt.retail_place
    IS 'Название торговой точки';

COMMENT ON COLUMN payment_statistic.receipt.retail_place_address
    IS 'Адрес торговой точки';

COMMENT ON COLUMN payment_statistic.receipt.total_sum
    IS 'Общая сумма чека';
