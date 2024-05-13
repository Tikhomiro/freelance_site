-- Создание таблицы пользователей (Users)
CREATE TABLE Users (
    user_id SERIAL PRIMARY KEY,
    login VARCHAR(100) UNIQUE NOT NULL,
    password VARCHAR(255) NOT NULL,
    fio VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    role VARCHAR(50) NOT NULL,
    experience VARCHAR(50) DEFAULT NULL
);

-- Создание таблицы заказов (Orders)
CREATE TABLE Orders (
    order_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    description TEXT,
    price INT,
    user_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
	customer INT DEFAULT NULL
);




