DROP TABLE IF EXISTS users CASCADE;
CREATE TABLE users(
    user_id serial PRIMARY KEY,
    user_login varchar(40) NOT NULL,
    user_password varchar(30) NOT NULL
);


DROP TABLE IF EXISTS goods CASCADE;
CREATE TABLE goods(
    goods_id serial PRIMARY KEY,
    goods_name varchar(40) NOT NULL,
    goods_description text,
    goods_price int,
    seller_id int
);
