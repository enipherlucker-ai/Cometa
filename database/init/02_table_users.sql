CREATE TABLE payment_statistic.users
(
    id            SERIAL PRIMARY KEY,
    name          TEXT    NOT NULL,
    age           INTEGER NOT NULL CHECK (age >= 0),
    description   TEXT,
    login         TEXT UNIQUE,
    password_hash TEXT
);

COMMENT ON TABLE payment_statistic.users
    IS 'Пользователи системы';

COMMENT ON COLUMN payment_statistic.users.id
    IS 'Уникальный идентификатор пользователя';

COMMENT ON COLUMN payment_statistic.users.name
    IS 'Имя пользователя';

COMMENT ON COLUMN payment_statistic.users.age
    IS 'Возраст пользователя в годах, неотрицательное число';

COMMENT ON COLUMN payment_statistic.users.description
    IS 'Дополнительная информация о пользователе';

COMMENT ON COLUMN payment_statistic.users.login
    IS 'Уникальный логин пользователя';

COMMENT ON COLUMN payment_statistic.users.password_hash
    IS 'Хеш пароля пользователя';

INSERT INTO payment_statistic.users
    (id, name, age, description, login, password_hash)
VALUES (20260308,
        'admin_user',
        18,
        'Административная УЗ',
        NULL,
        NULL);
