-- phpMyAdmin SQL Dump
-- version 5.0.2
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1:3306
-- Generation Time: Nov 03, 2023 at 08:30 PM
-- Server version: 5.7.31
-- PHP Version: 7.3.21

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `guestbookingsystem2302021`
--

-- --------------------------------------------------------

--
-- Table structure for table `bookings`
--

DROP TABLE IF EXISTS `bookings`;
CREATE TABLE IF NOT EXISTS `bookings` (
  `bid` int(11) NOT NULL AUTO_INCREMENT,
  `guestid` int(11) DEFAULT NULL,
  `roomtypeid` int(100) DEFAULT NULL,
  `from_` datetime DEFAULT NULL,
  `to_` datetime DEFAULT NULL,
  `roomid` int(11) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  `Check_out` datetime DEFAULT NULL,
  PRIMARY KEY (`bid`),
  KEY `roomtypeid` (`roomtypeid`),
  KEY `guestid` (`guestid`),
  KEY `roomid` (`roomid`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `bookings`
--

INSERT INTO `bookings` (`bid`, `guestid`, `roomtypeid`, `from_`, `to_`, `roomid`, `status`, `Check_out`) VALUES
(1, 1, 1, '2023-11-04 00:00:00', '2023-11-06 00:00:00', 1, '4', '2023-11-04 01:54:46'),
(2, 2, 1, '2023-11-04 00:00:00', '2023-11-06 00:00:00', 1, '1', NULL);

-- --------------------------------------------------------

--
-- Table structure for table `guests`
--

DROP TABLE IF EXISTS `guests`;
CREATE TABLE IF NOT EXISTS `guests` (
  `guestid` int(11) NOT NULL AUTO_INCREMENT,
  `gname` varchar(255) DEFAULT NULL,
  `gphone` varchar(255) DEFAULT NULL,
  `gemail` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`guestid`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `guests`
--

INSERT INTO `guests` (`guestid`, `gname`, `gphone`, `gemail`) VALUES
(1, 'Locandra Sing', '1234567890', 'locandra@gmail.com'),
(2, 'Purnalata Patnayak', '9638524565', 'purna@gmail.com');

-- --------------------------------------------------------

--
-- Table structure for table `rooms`
--

DROP TABLE IF EXISTS `rooms`;
CREATE TABLE IF NOT EXISTS `rooms` (
  `roomid` int(11) NOT NULL AUTO_INCREMENT,
  `room_number` varchar(255) DEFAULT NULL,
  `room_flor` int(50) DEFAULT NULL,
  `roomtypeid` int(100) DEFAULT NULL,
  `status` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`roomid`),
  KEY `roomtypeid` (`roomtypeid`)
) ENGINE=MyISAM AUTO_INCREMENT=21 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `rooms`
--

INSERT INTO `rooms` (`roomid`, `room_number`, `room_flor`, `roomtypeid`, `status`) VALUES
(1, '100', 1, 1, 'booked'),
(2, '101', 1, 1, 'empty'),
(3, '102', 1, 1, 'empty'),
(4, '103', 1, 1, 'empty'),
(5, '104', 1, 1, 'empty'),
(6, '200', 2, 2, 'empty'),
(7, '201', 2, 2, 'empty'),
(8, '202', 2, 2, 'empty'),
(9, '203', 2, 2, 'empty'),
(10, '204', 2, 2, 'empty'),
(11, '300', 3, 3, 'empty'),
(12, '301', 3, 3, 'empty'),
(13, '302', 3, 3, 'empty'),
(14, '303', 3, 3, 'empty'),
(15, '304', 3, 3, 'empty'),
(16, '400', 4, 4, 'empty'),
(17, '401', 4, 4, 'empty'),
(18, '402', 4, 4, 'empty'),
(19, '403', 4, 4, 'empty'),
(20, '404', 4, 4, 'empty');

-- --------------------------------------------------------

--
-- Table structure for table `roomtype`
--

DROP TABLE IF EXISTS `roomtype`;
CREATE TABLE IF NOT EXISTS `roomtype` (
  `roomtypeid` int(11) NOT NULL AUTO_INCREMENT,
  `roomtype_desc` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`roomtypeid`)
) ENGINE=MyISAM AUTO_INCREMENT=5 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `roomtype`
--

INSERT INTO `roomtype` (`roomtypeid`, `roomtype_desc`) VALUES
(1, 'SINGLE WITH AC'),
(2, 'SINGLE WITHOUT AC'),
(3, 'DOUBLE WITH AC'),
(4, 'DOUBLE WITHOUT AC');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
CREATE TABLE IF NOT EXISTS `users` (
  `user_id` int(11) NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `phone` varchar(15) NOT NULL,
  `date_of_birth` date NOT NULL,
  `Type` varchar(255) NOT NULL,
  PRIMARY KEY (`user_id`)
) ENGINE=MyISAM AUTO_INCREMENT=3 DEFAULT CHARSET=latin1;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `password`, `email`, `phone`, `date_of_birth`, `Type`) VALUES
(1, 'Rekha Sing', '$2b$12$z2Zu7XjgHoZJLBZ3EOekte1dwDj4w1LSswWgBDLhKITNm4M.XBXVa', 'rekha@gmail.com', '7895222222', '1996-02-04', 'Receptionist'),
(2, 'Purnalata Patnayak', '$2b$12$cWy8lEKI4R9LBTw8JCRgJOmkGLHO8gdLczralsPOmw7KLVAOKBCK.', 'purna@gmail.com', '2589637465', '1996-07-04', 'Guest');
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
