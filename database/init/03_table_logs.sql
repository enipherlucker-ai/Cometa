CREATE TABLE logs.api_logs
(
    id          SERIAL PRIMARY KEY,
    is_err      BOOLEAN,
    user_id     INTEGER REFERENCES payment_statistic.users (id),
    service     TEXT NOT NULL,
    method      TEXT NOT NULL,
    comment     TEXT,
    input_data  TEXT NOT NULL,
    output_data TEXT NOT NULL
);

COMMENT ON TABLE logs.api_logs
    IS 'Журнал обращений к API';

COMMENT ON COLUMN logs.api_logs.id
    IS 'Уникальный идентификатор записи журнала';

COMMENT ON COLUMN logs.api_logs.is_err
    IS 'Признак ошибки при обращении к API';

COMMENT ON COLUMN logs.api_logs.user_id
    IS 'Идентификатор пользователя, инициировавшего обращение';

COMMENT ON COLUMN logs.api_logs.service
    IS 'Название сервиса API';

COMMENT ON COLUMN logs.api_logs.method
    IS 'Метод и путь запроса к API';

COMMENT ON COLUMN logs.api_logs.comment
    IS 'Дополнительная информация об обращении';

COMMENT ON COLUMN logs.api_logs.input_data
    IS 'Входные данные запроса';

COMMENT ON COLUMN logs.api_logs.output_data
    IS 'Ответ API или описание ошибки';
