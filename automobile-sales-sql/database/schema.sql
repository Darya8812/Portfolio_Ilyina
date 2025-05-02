-- Создание базы данных
CREATE DATABASE IF NOT EXISTS automobile_sales;
USE automobile_sales;

-- Таблица Продавцы
CREATE TABLE Продавцы (
    №_продавца INT PRIMARY KEY,
    ФИО VARCHAR(50) NOT NULL,
    Комиссионные DECIMAL(3,2),
    Город VARCHAR(30)
);

-- Таблица Модели
CREATE TABLE Модели (
    Код_модели INT PRIMARY KEY,
    Модель VARCHAR(50) NOT NULL,
    Мощность INT,
    Цвет VARCHAR(20),
    Заводская_цена_ус DECIMAL(10,2),
    Торговая_наценка_пр DECIMAL(5,2),
    Розничная_цена DECIMAL(10,2)
);

-- Таблица Клиенты
CREATE TABLE Клиенты (
    №_заказа INT PRIMARY KEY,
    Код_модели INT,
    Сумма_заказа DECIMAL(10,2),
    ФИО VARCHAR(50) NOT NULL,
    Адрес VARCHAR(50),
    Дата_заказа DATE,
    №_продавца INT,
    FOREIGN KEY (Код_модели) REFERENCES Модели(Код_модели),
    FOREIGN KEY (№_продавца) REFERENCES Продавцы(№_продавца)
);
