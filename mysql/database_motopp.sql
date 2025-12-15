CREATE DATABASE motopp;

USE motopp;

CREATE TABLE user (
    id INT PRIMARY KEY AUTO_INCREMENT,
    email VARCHAR(100) UNIQUE,
    password VARCHAR(100),
    name VARCHAR(1000)
);


CREATE TABLE bike (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    make VARCHAR(1000),
    model VARCHAR(1000),
    year INT,
    user_id INTEGER,
    FOREIGN KEY (user_id) REFERENCES user(id)
);

CREATE TABLE part (
    id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(100),
    price DECIMAL(10, 2),
    external_url VARCHAR(255)
);


CREATE TABLE users_parts (
    id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT,
    part_id INT,
    type VARCHAR(100)
);

