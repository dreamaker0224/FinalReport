-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2025-01-02 12:21:47
-- 伺服器版本： 10.4.28-MariaDB
-- PHP 版本： 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 資料庫： `foodpangolin`
--

-- --------------------------------------------------------

--
-- 資料表結構 `customers`
--

CREATE TABLE `customers` (
  `customer_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `customers`
--

INSERT INTO `customers` (`customer_id`, `user_id`, `address`, `phone_number`) VALUES
(1, 2, 'adsfas', '093213151');

-- --------------------------------------------------------

--
-- 資料表結構 `delivery_personnel`
--

CREATE TABLE `delivery_personnel` (
  `delivery_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `availability_status` tinyint(1) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `delivery_personnel`
--

INSERT INTO `delivery_personnel` (`delivery_id`, `user_id`, `availability_status`) VALUES
(1, 1, NULL);

-- --------------------------------------------------------

--
-- 資料表結構 `feedback`
--

CREATE TABLE `feedback` (
  `review_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `rating` int(11) DEFAULT NULL CHECK (`rating` between 1 and 5),
  `comment` text DEFAULT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `feedback`
--

INSERT INTO `feedback` (`review_id`, `order_id`, `customer_id`, `rating`, `comment`, `created_at`) VALUES
(1, 13, 1, 1, 'asdfsa', '2024-12-30 20:37:05'),
(3, 23, 1, 3, '12132\r\n', '2024-12-31 16:19:17'),
(4, 24, 1, 5, '好吃', '2025-01-01 02:32:01');

-- --------------------------------------------------------

--
-- 資料表結構 `menu_items`
--

CREATE TABLE `menu_items` (
  `item_id` int(11) NOT NULL,
  `store_id` int(11) DEFAULT NULL,
  `item_name` varchar(255) NOT NULL,
  `price` decimal(10,2) NOT NULL,
  `description` text DEFAULT NULL,
  `status` enum('available','unavailable') NOT NULL,
  `img` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `menu_items`
--

INSERT INTO `menu_items` (`item_id`, `store_id`, `item_name`, `price`, `description`, `status`, `img`) VALUES
(2, 1, '雞腿', 120.00, '好吃雞腿', 'available', NULL),
(3, 1, '雞翅', 10.00, '難吃雞翅\r\n', 'available', NULL),
(4, 1, '123', 123.00, '123', 'available', NULL);

-- --------------------------------------------------------

--
-- 資料表結構 `orders`
--

CREATE TABLE `orders` (
  `order_id` int(11) NOT NULL,
  `customer_id` int(11) DEFAULT NULL,
  `store_id` int(11) DEFAULT NULL,
  `delivery_id` int(11) DEFAULT NULL,
  `total_price` decimal(10,2) NOT NULL,
  `status` enum('pending','preparing','waiting','delivering','arrival','completed','cancelled') NOT NULL,
  `created_at` datetime NOT NULL,
  `updated_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `orders`
--

INSERT INTO `orders` (`order_id`, `customer_id`, `store_id`, `delivery_id`, `total_price`, `status`, `created_at`, `updated_at`) VALUES
(13, 1, 1, 1, 253.00, 'cancelled', '2024-12-30 17:56:14', '2024-12-30 18:19:43'),
(23, 1, 1, NULL, 240.00, 'cancelled', '2024-12-31 14:54:24', '0000-00-00 00:00:00'),
(24, 1, 1, 1, 506.00, 'completed', '2024-12-31 15:12:24', '2025-01-01 00:42:23'),
(25, 1, 1, 1, 12150.00, 'completed', '2024-12-31 18:58:02', '2024-12-31 20:35:43'),
(26, 1, 1, 1, 120.00, 'completed', '2024-12-31 19:46:19', '2024-12-31 20:38:09'),
(28, 1, 1, 1, 130.00, 'cancelled', '2025-01-01 00:43:03', '2025-01-01 00:44:29'),
(30, 1, 1, 1, 133.00, 'completed', '2025-01-01 01:03:22', '2025-01-01 01:09:46'),
(31, 1, 1, NULL, 130.00, 'cancelled', '2025-01-01 01:54:35', '0000-00-00 00:00:00'),
(32, 1, 1, 1, 123.00, 'pending', '2025-01-01 01:59:56', '2025-01-01 17:29:40'),
(33, 1, 1, NULL, 120.00, 'pending', '2025-01-01 02:01:30', '0000-00-00 00:00:00'),
(34, 1, 1, NULL, 10.00, 'pending', '2025-01-01 02:10:31', '0000-00-00 00:00:00'),
(35, 1, 1, NULL, 120.00, 'cancelled', '2025-01-01 16:21:01', '0000-00-00 00:00:00');

-- --------------------------------------------------------

--
-- 資料表結構 `order_items`
--

CREATE TABLE `order_items` (
  `order_item_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `item_id` int(11) DEFAULT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `order_items`
--

INSERT INTO `order_items` (`order_item_id`, `order_id`, `item_id`, `quantity`, `price`) VALUES
(28, 13, 2, 1, 120.00),
(29, 13, 3, 1, 10.00),
(30, 13, 4, 1, 123.00),
(31, 14, 2, 2, 120.00),
(32, 14, 4, 1, 123.00),
(33, 15, 4, 2, 123.00),
(34, 16, 2, 1, 120.00),
(35, 16, 4, 1, 123.00),
(36, 17, 2, 1, 120.00),
(37, 18, 3, 1, 10.00),
(38, 19, 2, 1, 120.00),
(39, 20, 3, 1, 10.00),
(40, 21, 3, 1, 10.00),
(41, 22, 3, 1, 10.00),
(42, 23, 2, 2, 120.00),
(43, 24, 2, 2, 120.00),
(44, 24, 3, 2, 10.00),
(45, 24, 4, 2, 123.00),
(46, 25, 2, 50, 120.00),
(47, 25, 4, 50, 123.00),
(48, 26, 2, 1, 120.00),
(49, NULL, 3, 1, 10.00),
(50, 28, 2, 1, 120.00),
(51, 28, 3, 1, 10.00),
(52, 29, 2, 1, 120.00),
(53, 30, 3, 1, 10.00),
(54, 30, 4, 1, 123.00),
(55, 31, 2, 1, 120.00),
(56, 31, 3, 1, 10.00),
(57, 32, 4, 1, 123.00),
(58, 33, 2, 1, 120.00),
(59, 34, 3, 1, 10.00),
(60, 35, 2, 1, 120.00);

-- --------------------------------------------------------

--
-- 資料表結構 `stores`
--

CREATE TABLE `stores` (
  `store_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `store_name` varchar(255) NOT NULL,
  `address` varchar(255) DEFAULT NULL,
  `phone_number` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `stores`
--

INSERT INTO `stores` (`store_id`, `user_id`, `store_name`, `address`, `phone_number`) VALUES
(1, 3, 'stest', 'adsad', 'asds'),
(3, 8, 'stest2', NULL, NULL);

-- --------------------------------------------------------

--
-- 資料表結構 `transactions`
--

CREATE TABLE `transactions` (
  `transaction_id` int(11) NOT NULL,
  `order_id` int(11) DEFAULT NULL,
  `store_amount` decimal(10,2) NOT NULL,
  `delivery_amount` decimal(10,2) NOT NULL,
  `customer_amount` decimal(10,2) NOT NULL,
  `created_at` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `name` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role` enum('customer','store','delivery','platform') NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`user_id`, `name`, `email`, `password`, `role`) VALUES
(1, 'dtest', 'dtest@dtest', 'dtest', 'delivery'),
(2, 'ctest', 'ctest@ctest', 'ctest', 'customer'),
(3, 'stest', 'stest@stest', 'stest', 'store'),
(4, 'ptest', 'ptest@ptest', 'ptest', 'platform'),
(5, 'ctest2', 'ctest2@ctest2', 'ctest2', 'customer'),
(8, 'stest2', 'stest2@stest2', 'stest2', 'store');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `customers`
--
ALTER TABLE `customers`
  ADD PRIMARY KEY (`customer_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `delivery_personnel`
--
ALTER TABLE `delivery_personnel`
  ADD PRIMARY KEY (`delivery_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `feedback`
--
ALTER TABLE `feedback`
  ADD PRIMARY KEY (`review_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `customer_id` (`customer_id`);

--
-- 資料表索引 `menu_items`
--
ALTER TABLE `menu_items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `store_id` (`store_id`);

--
-- 資料表索引 `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`order_id`),
  ADD KEY `customer_id` (`customer_id`),
  ADD KEY `store_id` (`store_id`),
  ADD KEY `delivery_id` (`delivery_id`);

--
-- 資料表索引 `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`order_item_id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `item_id` (`item_id`);

--
-- 資料表索引 `stores`
--
ALTER TABLE `stores`
  ADD PRIMARY KEY (`store_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `transactions`
--
ALTER TABLE `transactions`
  ADD PRIMARY KEY (`transaction_id`),
  ADD KEY `order_id` (`order_id`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `email` (`email`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `customers`
--
ALTER TABLE `customers`
  MODIFY `customer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `delivery_personnel`
--
ALTER TABLE `delivery_personnel`
  MODIFY `delivery_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `feedback`
--
ALTER TABLE `feedback`
  MODIFY `review_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `menu_items`
--
ALTER TABLE `menu_items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `orders`
--
ALTER TABLE `orders`
  MODIFY `order_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=36;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `order_items`
--
ALTER TABLE `order_items`
  MODIFY `order_item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=61;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `stores`
--
ALTER TABLE `stores`
  MODIFY `store_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `transactions`
--
ALTER TABLE `transactions`
  MODIFY `transaction_id` int(11) NOT NULL AUTO_INCREMENT;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
