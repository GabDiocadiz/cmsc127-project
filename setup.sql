DROP DATABASE IF EXISTS `foodproject`;
CREATE DATABASE IF NOT EXISTS `foodproject`;
USE `foodproject`;

-- Create table user with variables userid, username, password
CREATE TABLE `user`(
  `userno` INT(5) AUTO_INCREMENT,
  `username` VARCHAR(20) NOT NULL,
  `password` VARCHAR(20) NOT NULL,
  PRIMARY KEY (`userno`)
);

-- Create table establishment with variables establishment id, name, and average rating
CREATE TABLE `establishment` (
  `estno` INT(5) NOT NULL AUTO_INCREMENT,
  `estname` varchar(50) NOT NULL,
  `averating` DECIMAL(3,2) DEFAULT 0,
  constraint est_name_uk unique(estname),
  PRIMARY KEY (`estno`)
);

-- create table food with variable food id, name, avearage rating, price, food type, and establsihment id
CREATE TABLE `food` (
  `foodno` INT(5) NOT NULL AUTO_INCREMENT,
  `foodname` varchar(50) NOT NULL,
  `averating` DECIMAL(3,2) DEFAULT 0,
  `price` DECIMAL(7,2) NOT NULL,
  `foodtype` VARCHAR(10) NOT NULL,
  `estno` INT(5) NOT null,
  constraint food_name_uk unique(foodname),
  constraint food_estno_fk foreign key(estno) references establishment(estno) ON DELETE CASCADE,
  PRIMARY KEY (`foodno`)
);

-- Create table review with variables revied id, text, rating, date, food id, establihsment id, and user id
CREATE TABLE `review` (
  `reviewno` INT(5) NOT NULL AUTO_INCREMENT,
  `text` varchar(50) NOT NULL,
  `rating` NUMERIC(1) NOT NULL,
  `date` DATE NOT NULL,
  `foodno` INT(5),
  `estno` INT(5) NOT NULL,
  `userno` INT(5) NOT NULL,
  constraint review_estno_fk foreign key(estno) references establishment(estno) ON DELETE CASCADE,
  constraint review_foodno_fk foreign key(foodno) references food(foodno) ON DELETE CASCADE,
  constraint review_userno_fk foreign key(userno) references user(userno) ON DELETE CASCADE,
  PRIMARY KEY (`reviewno`)
);

##################
/*	Dummy Values */
##################
-- Dummy users
INSERT INTO `user` (`username`, `password`) VALUES
	('Wittea', 'Wittea'),
	('Drunk', 'tagay');

-- Dummy estabalishments
INSERT INTO `establishment` (`estname`) VALUES
	('Wittea'),
	('MyLK Tea'),
	('Boba Ka Tea'),
	('SayoTea'),
	('Atteatude');

-- Dummy food
INSERT INTO `food` (`foodname`, `price`, `foodtype`, `estno`) VALUES
	('food 1', 10, 'Meat', 1),
	('food 2', 20, 'Vegetable', 2),
	('food 3', 30, 'Meat', 3),
	('food 4', 40, 'Vegetable', 4),
	('food 5', 50, 'Meat', 5),
	('food 6', 60, 'Drinks', 1),
	('food 7', 77777.77, 'Drinks', 2),
	('food 8', 80, 'Drinks', 3),
	('food 9', 9, 'Drinks', 4),
	('food 10', 12345, 'Drinks', 5),
	('food 11', 11, 'Drinks', 1),
	('non meat non 30', 100, 'Dessert', 3),
	('non meat 30', 15.50, 'Dessert', 3),
	('meat non 30', 100, 'Meat', 3);

-- dummy reviews
INSERT INTO `review` (`text`, `rating`, `date`, `foodno`, `estno`, `userno`) VALUES
	('Good food', 5, str_to_date('17-JAN-2023','%d-%M-%Y'), 1, 1, 1),
	('Okay lang', 3, str_to_date('17-MAR-2023','%d-%M-%Y'), 2, 2, 1),
	('Never again', 1, str_to_date('17-APR-2023','%d-%M-%Y'), 7, 2, 1),
	('Bet', 4, str_to_date('17-MAY-2023','%d-%M-%Y'), 8, 3, 1),
	('Babalik ako', 4, str_to_date('17-JAN-2023','%d-%M-%Y'), 9, 4, 1),
	('XXX', 2, str_to_date('17-NOV-2023','%d-%M-%Y'), 5, 5, 1),
	('Nope', 1, str_to_date('17-NOV-2023','%d-%M-%Y'), 10, 5, 1),
	('it is what it is', 3, str_to_date('17-MAR-2023','%d-%M-%Y'), 1, 1, 2);
