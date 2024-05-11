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
