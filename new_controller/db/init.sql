DROP TABLE IF EXISTS all_users CASCADE;
CREATE TABLE all_users(
	global_id Serial Primary key,
	login varchar(40) NOT NULL UNIQUE, -- Логин
	password text NOT NULL, --Пароль
	user_group char(1) NOT NULL --Тип пользователя
	);


DROP TABLE IF EXISTS customers CASCADE;
CREATE TABLE customers(
	global_id Serial Primary key,
	phone_number varchar(11) NOT NULL UNIQUE, -- Номер телефона
	email varchar(40) NOT NULL UNIQUE, -- Почта
	customer_name varchar(40) NOT NULL, -- Имя пользователя
	birthday date, --Дата рождения
	city varchar(40), -- Город
	basket jsonb -- Корзина
	);


DROP TABLE IF EXISTS goods CASCADE;
CREATE TABLE goods(
	goods_id Serial Primary key,
	goods_name varchar(100) NOT NULL, -- Название товара
	goods_price varchar(30) NOT NULL, -- Цена
	goods_small_info text, -- Краткое описание товара
	goods_description jsonb, -- Полное описание
	goods_tag varchar(40), -- Подкатегория товара
	goods_img varchar(300) NOT NULL, -- Путь до картинки
	is_visible boolean DEFAULT TRUE -- Видим ли товар
	);
