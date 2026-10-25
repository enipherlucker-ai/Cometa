CREATE TABLE payment_statistic.user_sessions
(
    id         SERIAL PRIMARY KEY,
    token_hash TEXT        NOT NULL UNIQUE,
    user_id    INTEGER     NOT NULL REFERENCES payment_statistic.users (id) ON DELETE CASCADE,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    expires_at TIMESTAMPTZ NOT NULL
);

COMMENT ON TABLE payment_statistic.user_sessions
    IS 'Сессии пользователей';

COMMENT ON COLUMN payment_statistic.user_sessions.id
    IS 'Уникальный идентификатор сессии';

COMMENT ON COLUMN payment_statistic.user_sessions.token_hash
    IS 'Уникальный хеш токена сессии';

COMMENT ON COLUMN payment_statistic.user_sessions.user_id
    IS 'Идентификатор пользователя, которому принадлежит сессия';

COMMENT ON COLUMN payment_statistic.user_sessions.created_at
    IS 'Дата и время создания сессии';

COMMENT ON COLUMN payment_statistic.user_sessions.expires_at
    IS 'Дата и время истечения срока действия сессии';
