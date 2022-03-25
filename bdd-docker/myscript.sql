-- --------------------------------------------------------
-- Hôte:                         127.0.0.1
-- Version du serveur:           5.7.33 - MySQL Community Server (GPL)
-- SE du serveur:                Win64
-- HeidiSQL Version:             11.2.0.6213
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Listage de la structure de la base pour au_bon_beurre
CREATE DATABASE IF NOT EXISTS `au_bon_beurre` /*!40100 DEFAULT CHARACTER SET latin1 */;
USE `au_bon_beurre`;
-- Listage de la structure de la table au_bon_beurre. automatons
CREATE TABLE IF NOT EXISTS `automatons` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_unit` int(11) NOT NULL,
  `number` int(11) NOT NULL,
  `type` int(11) NOT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Unit` (`id_unit`),
  CONSTRAINT `FK_Unit` FOREIGN KEY (`id_unit`) REFERENCES `units` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=101 DEFAULT CHARSET=latin1;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table au_bon_beurre. productions
CREATE TABLE IF NOT EXISTS `productions` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `id_automaton` int(11) NOT NULL,
  `id_unit` int(11) NOT NULL,
  `tankTemperature` float DEFAULT NULL,
  `outsideTemperature` float DEFAULT NULL,
  `milkWeight` float DEFAULT NULL,
  `finalizedProductWeight` float DEFAULT NULL,
  `ph` float DEFAULT NULL,
  `k` int(11) DEFAULT NULL,
  `naci` float DEFAULT NULL,
  `salmonel` int(11) DEFAULT NULL,
  `ecoli` int(11) DEFAULT NULL,
  `listeria` int(11) DEFAULT NULL,
  `generatedTime` datetime DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `FK_Automaton2` (`id_automaton`),
  KEY `FK_Unit2` (`id_unit`),
  CONSTRAINT `FK_Automaton2` FOREIGN KEY (`id_automaton`) REFERENCES `automatons` (`id`),
  CONSTRAINT `FK_Unit2` FOREIGN KEY (`id_unit`) REFERENCES `units` (`number`)
) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=latin1;

-- Les données exportées n'étaient pas sélectionnées.

-- Listage de la structure de la table au_bon_beurre. units
CREATE TABLE IF NOT EXISTS `units` (
  `number` int(11) NOT NULL,
  PRIMARY KEY (`number`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- Les données exportées n'étaient pas sélectionnées.

/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
