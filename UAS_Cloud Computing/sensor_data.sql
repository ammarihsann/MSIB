-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 07, 2024 at 02:13 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ammar_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `sensor_data`
--

CREATE TABLE `sensor_data` (
  `id` int(11) NOT NULL,
  `temperature` float DEFAULT NULL,
  `humidity` float DEFAULT NULL,
  `timestamp` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `sensor_data`
--

INSERT INTO `sensor_data` (`id`, `temperature`, `humidity`, `timestamp`) VALUES
(1, 80, 100, '2024-11-07 10:38:09'),
(2, 80, 100, '2024-11-07 10:38:15'),
(3, 32.4, 100, '2024-11-07 10:38:18'),
(4, 32.4, 56.5, '2024-11-07 10:38:21'),
(5, 32.4, 56.5, '2024-11-07 10:38:26'),
(6, 32.4, 56.5, '2024-11-07 10:38:32'),
(7, 32.4, 56.5, '2024-11-07 10:38:35'),
(8, 32.4, 56.5, '2024-11-07 10:38:37'),
(9, 32.4, 56.5, '2024-11-07 10:38:40'),
(10, 32.4, 56.5, '2024-11-07 10:38:53'),
(11, 32.4, 56.5, '2024-11-07 10:39:13'),
(12, 32.4, 56.5, '2024-11-07 11:13:22'),
(13, 27.9, 78, '2024-11-07 12:11:27'),
(14, 27.9, 78, '2024-11-07 12:11:30'),
(15, 27.9, 78, '2024-11-07 12:11:33'),
(16, 27.9, 78, '2024-11-07 12:11:41'),
(17, 27.9, 78, '2024-11-07 12:11:44'),
(18, 27.9, 78, '2024-11-07 12:11:46'),
(19, 27.9, 78, '2024-11-07 12:11:49'),
(20, 27.9, 78, '2024-11-07 12:11:52'),
(21, 30, 70, '2024-11-07 12:18:56');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `sensor_data`
--
ALTER TABLE `sensor_data`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `sensor_data`
--
ALTER TABLE `sensor_data`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
