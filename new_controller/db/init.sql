DROP TABLE IF EXISTS all_users CASCADE;
CREATE TABLE all_users(
	global_id Serial Primary key,
	username varchar(40) NOT NULL UNIQUE, -- Логин
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
	basket jsonb DEFAULT '{}', -- Корзина
	scores int DEFAULT 0, -- Количество бонусных очков
	customer_img varchar(300) NOT NULL, -- Путь до картинки
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
	is_visible boolean DEFAULT TRUE, -- Видим ли товар
	goods_reserve int -- Резерв товара
	);

DROP TABLE IF EXISTS articles CASCADE;
CREATE TABLE articles(
	article_id Serial Primary key,
	article_title varchar(100) NOT NULL UNIQUE, -- Название статьи
	article_small_info text NOT NULL, -- Краткое описание
	article_text text NOT NULL, -- Текст статьи
	is_visible boolean DEFAULT TRUE -- Видима ли статья
	);

DROP TABLE IF EXISTS reviews CASCADE;
CREATE TABLE reviews(
	review_id Serial Primary key,
    goods_id int NOT NULL, -- id Товара, на который пишется отзыв
    customer_id int, -- id пользователя, что пишет отзыв
    customer_name varchar(40) NOT NULL, -- Имя пользователя, что пишет отзыв
    stars varchar(40) NOT NULL, -- Рейтинг товара
    customer_text text NOT NULL, -- Текст комментария

    FOREIGN KEY (goods_id) REFERENCES goods(goods_id) ON DELETE CASCADE,
    FOREIGN KEY (customer_id) REFERENCES customers (global_id) ON DELETE SET NULL
	);


DROP TABLE IF EXISTS orders CASCADE;
CREATE TABLE orders(
	order_id Serial Primary key,
    goods_id int , -- id Товара, который купил пользователь
    customer_id int NOT NULL, -- id пользователя, который купил товар
    goods_name varchar(40) NOT NULL, -- Название товара
    city varchar(40) NOT NULL, -- Город доставки
    delivery_date date NOT NULL, --Дата доставки
    status varchar(40) NOT NULL, -- Статус
    goods_img varchar(300) NOT NULL, -- Путь до картинки

    FOREIGN KEY (goods_id) REFERENCES goods(goods_id) ON DELETE SET NULL,
    FOREIGN KEY (customer_id) REFERENCES customers (global_id) ON DELETE CASCADE
	);


