-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema movies_project
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `movies_project` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci ;
-- -----------------------------------------------------
-- Table `movies_project`.`movies`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies_project`.`movies` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(100) NULL DEFAULT NULL,
  `director` VARCHAR(155) NULL DEFAULT NULL,
  `studio` VARCHAR(100) NULL DEFAULT NULL,
  `genre` VARCHAR(100) NULL DEFAULT NULL,
  `synopsis` TEXT(500) NULL DEFAULT NULL,
  `year` YEAR NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movies_project`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies_project`.`users` (
  `id` INT NOT NULL AUTO_INCREMENT,
  `user_name` VARCHAR(45) NULL DEFAULT NULL,
  `email` VARCHAR(200) NULL DEFAULT NULL,
  `password` VARCHAR(255) NULL DEFAULT NULL,
  `real_name` VARCHAR(120) NULL DEFAULT NULL,
  `gender` VARCHAR(45) NULL DEFAULT NULL,
  `bio` VARCHAR(255) NULL DEFAULT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  `updated_at` DATETIME NULL DEFAULT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB;


-- -----------------------------------------------------
-- Table `movies_project`.`likes`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `movies_project`.`likes` (
  `movie_id` INT NOT NULL,
  `user_id` INT NOT NULL,
  `created_at` DATETIME NULL DEFAULT NOW(),
  INDEX `fk_likes_movies1_idx` (`movie_id` ASC) VISIBLE,
  INDEX `fk_likes_users1_idx` (`user_id` ASC) VISIBLE,
  CONSTRAINT `fk_likes_movies1`
    FOREIGN KEY (`movie_id`)
    REFERENCES `movies_project`.`movies` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION,
  CONSTRAINT `fk_likes_users1`
    FOREIGN KEY (`user_id`)
    REFERENCES `movies_project`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB;

USE `mydb` ;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
