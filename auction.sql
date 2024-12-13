-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- 主機： 127.0.0.1
-- 產生時間： 2024-10-29 14:56:39
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
-- 資料庫： `auction`
--

-- --------------------------------------------------------

--
-- 資料表結構 `bids`
--

CREATE TABLE `bids` (
  `bid_id` int(11) NOT NULL,
  `item_id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `bid_price` decimal(10,2) NOT NULL,
  `bid_time` datetime NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- 資料表結構 `items`
--

CREATE TABLE `items` (
  `item_id` int(11) NOT NULL,
  `start_price` decimal(20,2) NOT NULL,
  `start_time` datetime NOT NULL,
  `item_name` varchar(255) NOT NULL,
  `user_id` int(11) NOT NULL,
  `description` text DEFAULT NULL,
  `material` varchar(255) DEFAULT NULL,
  `dynasty` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `items`
--

INSERT INTO `items` (`item_id`, `start_price`, `start_time`, `item_name`, `user_id`, `description`, `material`, `dynasty`) VALUES
(1, 10000.00, '2024-10-22 13:30:03', '翠玉白菜', 1, '翠玉白菜是國立故宮博物院最受喜愛的藏品之一。工匠順應翠玉天然的色澤，以濃重的深綠色表現層層包覆的菜葉；白色部分雖有裂痕及雜質，但在巧妙的安排下，轉化為新鮮、飽含水分的白菜莖部。菜葉頂端的螽斯和蝗蟲，瞬間帶進了鮮活的田園氣息。翠玉白菜最初是一件華麗的宮殿陳設盆景，以栽種的形式立在琺瑯盆景上。', '玉石', '清'),
(2, 10000.00, '2024-10-26 12:45:48', '黃釉瓷硯', 1, '瓷硯，除硯面外均滿釉。高壁，內腔中空，上方的圓形墨池，既為窯燒的氣孔，且可注溫水以暖硯。將硯倒置橫放，其形長方略近梯形，後端稍高而較寬，前端略窄而低，四角皆圓，頂面中央微凹，顯然原形是一瓷枕。此種尺寸稍小的瓷枕，在唐代墓葬及窯址中均曾多次出現，有以為是脈枕，醫療診斷時所用。中央刻乾隆五十六年(1791)楷銘︰「瓷之治本澄泥也，漢之瓦或庶幾也，不見修內宣和何闕斯也。歲久如玉，視玉堂澄泥猶遜茲也。物聚所好，不能不於此而恧斯也。乾陸辛亥御銘。」印：「 比德」、「朗潤」。', '陶瓷', '清 乾隆'),
(3, 10000.00, '2024-10-26 12:50:23', '景德鎮窯 粉彩福祿壽葫蘆瓶', 1, '器作葫蘆形，腰際繫紫彩帶，彩帶雖由瓷土塑形而成，但於結繩處的轉折以及絲帶下垂的皺折痕等，無不如實寫真的表現出來。全器罩施橘紅色底釉，口緣描金，底足外壁畫如意雲紋，器身滿畫纏枝藤蔓與葫蘆。藤蔓綠葉有深淺之別，葫蘆果實施黃彩，局部點綴褐色斑點；蝙蝠施橘色釉彩，姿態或上或下，口部皆銜「卍」字。器內及底施湖綠色釉，底心留白以紅彩書「大清乾隆年製」六字篆款。乾隆官窯喜以吉祥圖案為飾，乾隆八年（1743），皇帝傳旨御窯廠，指示瓷器圖案的燒造務必「各按時令分別吉祥花樣」，故此品之葫蘆形，因葫蘆與「福祿」的諧音而有吉祥的象徵，而蝙蝠銜「卍」，意喻萬福。', '陶瓷', '清 乾隆'),
(4, 10000.00, '2024-10-26 12:51:00', '齊家文化 玉璜', 1, '青白玉質，局部沁成褐色，有璺。呈兩側對稱條弧形，邊緣不平整，兩側各鑽一孔。', '玉石', '新石器時代'),
(5, 10000.00, '2024-10-26 12:45:48', '齊家文化 玉琮', 1, '灰青帶綠，「糖包白」青玉質，糖的部分顏色極深，盤紅色澤溫潤。內圓外方琮形，製作整齊，射頸略長，射口內圓外不圓，惟一端射口切斜。外壁刻乾隆御製詩：「蘊土華仍斐玉英，為秦為漢那分明。自非魏晉以後製，疑在木金之際呈。溟溟君應遇掘塹，中山穎乃得封城。拈毫硯北擒新句，望古猶餘言外情。乾隆丁酉御題。」', '玉石', '新石器時代'),
(6, 10000.00, '2024-10-26 12:52:15', '玉版 附清代乾隆時期紫檀木架', 1, '此件成做於新石器時代龍山齊家系文化的梯形玉版，呈赭紅帶黃綠色，中間帶有斑點團塊。尺寸巨大，氣勢恢弘。進入清宮後，經內務府造辦處整理，配紫檀木架，作屏風使用。乾隆皇帝曾兩度吟詠此器。乾隆11年（1746）作〈漢玉屏風歌〉，除歌詠此器與玉所彰顯之德行外，更表現皇帝對其色澤質地的仔細觀察。因不忍破壞玉器表面，故命張若藹仿顏碑字體書寫後，將〈漢玉屏風歌〉一詩鐫刻於木架上。乾隆19年（1754）又作〈詠漢玉屏風疊舊作韻〉，並命玉匠將11及19年詩分別刻於玉版的兩面。木架另面刻有梁詩正、汪由敦、勵宗萬、張若靄、裘曰修', '玉石', '新石器時代'),
(55, 123.00, '2024-10-28 14:58:55', '345', 5, '123', '123123213', '123'),
(59, 222.00, '2024-10-28 16:22:10', '222', 6, '2222', '222', '222'),
(61, 123.00, '2024-10-29 20:31:15', '123', 7, '123', '123', '123');

-- --------------------------------------------------------

--
-- 資料表結構 `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `user_account` varchar(255) NOT NULL,
  `user_password` varchar(255) NOT NULL,
  `user_name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- 傾印資料表的資料 `users`
--

INSERT INTO `users` (`user_id`, `user_account`, `user_password`, `user_name`) VALUES
(1, '123@123', '123', 'Justin Tsai'),
(2, '456@456', '456', 'Achigo Pan'),
(3, 'test@test', '123', 'Test'),
(4, 'justintsai77@gmail.com', '123', 'admin'),
(5, '000@000', '000', '000'),
(6, 'admin@admin', 'admin', 'admin'),
(7, '999@999', '999', '999');

--
-- 已傾印資料表的索引
--

--
-- 資料表索引 `bids`
--
ALTER TABLE `bids`
  ADD PRIMARY KEY (`bid_id`),
  ADD KEY `item_id` (`item_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `items`
--
ALTER TABLE `items`
  ADD PRIMARY KEY (`item_id`),
  ADD KEY `user_id` (`user_id`);

--
-- 資料表索引 `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `user_account` (`user_account`);

--
-- 在傾印的資料表使用自動遞增(AUTO_INCREMENT)
--

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `bids`
--
ALTER TABLE `bids`
  MODIFY `bid_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=33;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `items`
--
ALTER TABLE `items`
  MODIFY `item_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=62;

--
-- 使用資料表自動遞增(AUTO_INCREMENT) `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=8;

--
-- 已傾印資料表的限制式
--

--
-- 資料表的限制式 `bids`
--
ALTER TABLE `bids`
  ADD CONSTRAINT `bids_ibfk_1` FOREIGN KEY (`item_id`) REFERENCES `items` (`item_id`),
  ADD CONSTRAINT `bids_ibfk_2` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);

--
-- 資料表的限制式 `items`
--
ALTER TABLE `items`
  ADD CONSTRAINT `items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
