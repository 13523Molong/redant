-- -- phpMyAdmin SQL Dump
-- -- version 5.2.0
-- -- https://www.phpmyadmin.net/
-- --
-- -- 主机： localhost
-- -- 生成日期： 2023-02-21 00:04:30
-- -- 服务器版本： 5.7.40-log
-- -- PHP 版本： 7.4.33

-- SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
-- START TRANSACTION;
-- SET time_zone = "+00:00";

-- --
-- -- 数据库： `system`
-- -- 数据库名： new
-- --

-- -- --------------------------------------------------------

-- --
-- -- 表的结构 `bind`
-- --

-- -- CREATE TABLE `bind` (
-- --   `box_name` varchar(1000) CHARACTER SET utf8 DEFAULT NULL COMMENT '箱体名称',
-- --   `box_status` tinyint(10) NOT NULL DEFAULT '0' COMMENT '箱体状态',
-- --   `soil_id` varchar(1000) CHARACTER SET utf8 DEFAULT NULL COMMENT '土壤模块序列号',
-- --   `soil_status` tinyint(10) NOT NULL DEFAULT '0' COMMENT '土壤模块状态1已绑定；0未绑定',
-- --   `T_H_id` varchar(1000) CHARACTER SET utf8 DEFAULT NULL COMMENT '温湿度模块序列号',
-- --   `T_H_status` tinyint(10) NOT NULL DEFAULT '0' COMMENT '温湿度模块状态1已绑定；0未绑定',
-- --   `fertilizer_id` varchar(1000) CHARACTER SET utf8 DEFAULT NULL COMMENT '水肥一体化模块序列号',
-- --   `fertilizer_status` tinyint(10) NOT NULL DEFAULT '0' COMMENT '水肥一体化模块状态1已绑定；0未绑定',
-- --   `light_id` varchar(1000) CHARACTER SET utf8 DEFAULT NULL COMMENT '灯板模块序列号',
-- --   `light_status` tinyint(10) NOT NULL DEFAULT '0' COMMENT '灯板模块状态1已绑定；0未绑定'
-- -- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='设备绑定表';

-- --
-- -- 转存表中的数据 `bind`
-- --

-- -- INSERT INTO `bind` (`box_name`, `box_status`, `soil_id`, `soil_status`, `T_H_id`, `T_H_status`, `fertilizer_id`, `fertilizer_status`, `light_id`, `light_status`) VALUES
-- -- ('1', 0, 'F-01', 1, 'W-01', 1, 'H-02', 1, 'None', 0),
-- -- ('2', 0, 'F-18', 1, NULL, 0, 'None', 0, NULL, 0);

-- -- --------------------------------------------------------

-- --
-- -- 表的结构 `box`
-- --

-- -- CREATE TABLE `box` (
-- --   `id` int(11) UNSIGNED NOT NULL,
-- --   `obj_id` varchar(1000) NOT NULL DEFAULT '' COMMENT '箱体编号',
-- --   `e_heat` varchar(1000) NOT NULL DEFAULT '' COMMENT '空气温度',
-- --   `e_wet` varchar(1000) NOT NULL DEFAULT '' COMMENT '空气湿度',
-- --   `f_heat` varchar(1000) NOT NULL DEFAULT '' COMMENT '土壤温度',
-- --   `f_wet` varchar(1000) NOT NULL DEFAULT '' COMMENT '土壤湿度',
-- --   `carbon` varchar(1000) NOT NULL DEFAULT '' COMMENT '空气中二氧化碳含量',
-- --   `floor_N` varchar(1000) NOT NULL DEFAULT '' COMMENT '土壤中氮元素',
-- --   `floor_P` varchar(1000) NOT NULL DEFAULT '' COMMENT '土壤中磷元素',
-- --   `floor_K` varchar(1000) NOT NULL DEFAULT '' COMMENT '土壤中钾元素',
-- --   `PH` varchar(1000) NOT NULL DEFAULT '' COMMENT '土壤中PH值',
-- --   `S` varchar(1000) NOT NULL DEFAULT '' COMMENT '土壤中电导率',
-- --   `type` varchar(1000) NOT NULL DEFAULT '' COMMENT '光谱波段',
-- --   `strength` varchar(1000) NOT NULL DEFAULT '' COMMENT '光照强度',
-- --   `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1：有效 0：无效',
-- --   `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
-- --   `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间'
-- -- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='箱体设置表';

-- --
-- -- 转存表中的数据 `box`
-- --

-- -- INSERT INTO `box` (`id`, `obj_id`, `e_heat`, `e_wet`, `f_heat`, `f_wet`, `carbon`, `floor_N`, `floor_P`, `floor_K`, `PH`, `S`, `type`, `strength`, `status`, `updated_time`, `created_time`) VALUES
-- --                   (1, '1', '26', '36', '20', '56', '0.03', '125', '80', '108', '', '', '560', '66', 0, '2022-08-09 07:54:38', '2022-08-09 07:54:38'),
-- --                   (4, '2', '26', '36', '22', '37', '0.03', '120', '80', '108', '', '', '460', '40', 0, '2022-08-09 17:37:17', '2022-08-09 17:37:17');

-- -- --------------------------------------------------------

-- --
-- -- 表的结构 `member`
-- --

-- -- CREATE TABLE `member` (
-- --   `id` int(11) UNSIGNED NOT NULL,
-- --   `teacher_id` varchar(50) NOT NULL DEFAULT '' COMMENT '教师id',
-- --   `student_id` varchar(50) NOT NULL DEFAULT '' COMMENT '学生id',
-- --   `nickname` varchar(100) NOT NULL DEFAULT '' COMMENT '会员名',
-- --   `name` varchar(100) NOT NULL DEFAULT '' COMMENT '真实姓名',
-- --   `mobile` varchar(11) NOT NULL DEFAULT '' COMMENT '会员手机号码',
-- --   `type` varchar(100) NOT NULL DEFAULT '' COMMENT '会员类型',
-- --   `sex` tinyint(1) NOT NULL DEFAULT '0' COMMENT '性别 1：男 2：女',
-- --   `avatar` varchar(200) NOT NULL DEFAULT '' COMMENT '会员头像',
-- --   `salt` varchar(32) NOT NULL DEFAULT '' COMMENT '随机salt',
-- --   `reg_ip` varchar(100) NOT NULL DEFAULT '' COMMENT '注册ip',
-- --   `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '状态 1：有效 0：无效',
-- --   `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
-- --   `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间'
-- -- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='会员表';

-- -- --------------------------------------------------------

-- --
-- 表的结构 `user`
--

CREATE TABLE `user` (
  `uid` bigint(20) NOT NULL COMMENT '用户uid',
  `nickname` varchar(100) NOT NULL DEFAULT '' COMMENT '用户名',
  `mobile` varchar(20) NOT NULL DEFAULT '' COMMENT '手机号码',
  `email` varchar(100) NOT NULL DEFAULT '' COMMENT '邮箱地址',
  `sex` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：男 2：女 0：没填写',
  `avatar` varchar(64) NOT NULL DEFAULT '' COMMENT '头像',
  `login_name` varchar(20) NOT NULL DEFAULT '' COMMENT '登录用户名',
  `login_pwd` varchar(32) NOT NULL DEFAULT '' COMMENT '登录密码',
  `login_salt` varchar(32) NOT NULL DEFAULT '' COMMENT '登录密码的随机加密秘钥',
  `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1：有效 0：无效',
  `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='用户表（管理员）';

--
-- 转存表中的数据 `user`
--

INSERT INTO `user` (`uid`, `nickname`, `mobile`, `email`, `sex`, `avatar`, `login_name`, `login_pwd`, `login_salt`, `status`, `updated_time`, `created_time`) VALUES
(5, '努力学习的小白', '12345678910', '19741456185523@qq.com', 0, '', 'CRJ', 'dcf3d47f960f312235d8bb4b64100122', 'Q0kuBdTHrDAR1W1S', 1, '2022-08-01 20:36:20', '2022-08-01 20:36:20'),
(6, '方帅哥', '12345678966', '1596823586@123.com', 0, '', 'ff1', '******', 'Ik63TR1A2CrWKzu7', 1, '2022-08-02 14:13:20', '2022-08-02 14:13:20'),
(7, '方方', '12345672313', '15968dssd23586@123.com', 0, '', 'fsz', '******', 'Mh0lWOg8c5kj4niN', 1, '2022-08-02 14:14:33', '2022-08-02 14:14:33'),
(8, '111', '54564545', '121212212@1212.com', 0, '', 'test', '2ff6ee5639bf5a158943099a37d35a6c', 'wkJLANRteZJQapBU', 1, '2022-08-05 07:38:57', '2022-08-05 07:38:57');

-- -- --------------------------------------------------------

-- --
-- -- 表的结构 `wait_command`
-- --

-- -- CREATE TABLE `wait_command` (
-- --   `id` int(11) UNSIGNED NOT NULL,
-- --   `obj_id` varchar(1000) NOT NULL DEFAULT '' COMMENT '箱体编号',
-- --   `nickname` varchar(1000) NOT NULL DEFAULT '' COMMENT '发布者姓名',
-- --   `radius` varchar(1000) NOT NULL DEFAULT '' COMMENT '运行半径',
-- --   `height` varchar(1000) NOT NULL DEFAULT '' COMMENT '运行高度',
-- --   `speed` varchar(1000) NOT NULL DEFAULT '' COMMENT '转圈速度',
-- --   `times` varchar(1000) NOT NULL DEFAULT '1' COMMENT '运行次数',
-- --   `type` tinyint(1) NOT NULL DEFAULT '1' COMMENT '2：弧顶 1：沿圆绕行',
-- --   `angle` varchar(1000) NOT NULL DEFAULT '' COMMENT '俯仰角',
-- --   `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1：有效 0：无效',
-- --   `start_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '任务开始时间',
-- --   `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
-- --   `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间'
-- -- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='命令下发表';

-- -- --
-- -- -- 转存表中的数据 `wait_command`
-- -- --

-- -- INSERT INTO `wait_command` (`id`, `obj_id`, `nickname`, `radius`, `height`, `speed`, `times`, `type`, `angle`, `status`, `start_time`, `updated_time`, `created_time`) VALUES
-- -- (1, '1', '努力学习的小白', '20', '50', '30', '50', 1, '15', 1, '2022-08-18 21:11:10', '2022-08-05 09:56:39', '2022-08-05 09:56:39'),
-- -- (6, '1', '111', '1', '1', '1', '1', 2, '1', 1, '2023-02-01 17:08:31', '2023-02-01 17:08:35', '2023-02-01 17:08:35');

-- -- --
-- -- 转储表的索引
-- --

-- --
-- -- -- 表的索引 `box`
-- -- --
-- -- ALTER TABLE `box`
-- --   ADD PRIMARY KEY (`id`);

-- -- --
-- -- -- 表的索引 `member`
-- -- --
-- -- ALTER TABLE `member`
-- --   ADD PRIMARY KEY (`id`);

-- --
-- 表的索引 `user`
--
ALTER TABLE `user`
  ADD PRIMARY KEY (`uid`),
  ADD UNIQUE KEY `login_name` (`login_name`);

-- --
-- -- -- 表的索引 `wait_command`
-- -- --
-- -- ALTER TABLE `wait_command`
-- --   ADD PRIMARY KEY (`id`);

-- --
-- -- 在导出的表使用AUTO_INCREMENT
-- --

-- --
-- -- 使用表AUTO_INCREMENT `box`
-- --
-- -- ALTER TABLE `box`
-- --   MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=5;

-- -- --
-- -- -- 使用表AUTO_INCREMENT `member`
-- -- --
-- -- ALTER TABLE `member`
-- --   MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT;

-- --
-- 使用表AUTO_INCREMENT `user`
--
ALTER TABLE `user`
  MODIFY `uid` bigint(20) NOT NULL AUTO_INCREMENT COMMENT '用户uid', AUTO_INCREMENT=9;

-- --
-- -- 使用表AUTO_INCREMENT `wait_command`
-- --
-- -- ALTER TABLE `wait_command`
-- --   MODIFY `id` int(11) UNSIGNED NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;
-- -- COMMIT;

-- CREATE TABLE `cars` (
--   `carID` bigint(20) NOT NULL COMMENT '小车编号',
--   `position` varchar(100) NOT NULL DEFAULT '' COMMENT '工作地点',
--   `workstate` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：正常巡航 0：关机/未运行 2：标记/消杀蚂蚁窝',
--   `status` tinyint(1) NOT NULL DEFAULT '1' COMMENT '1：有效 0：无效',
--   `updated_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '最后一次更新时间',
--   `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间'
-- ) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小车基础信息表';

CREATE TABLE `cars_run_info` (
  `carID` bigint(20) NOT NULL COMMENT '小车编号',
  `time` bigint(20) NOT NULL COMMENT '时间戳',
  `workstate` tinyint(1) NOT NULL DEFAULT '0' COMMENT '1：正常巡航 0：关机/未运行 2：/消杀蚂蚁窝 3：返回起点中 4：待机暂停中',
  `longitude` decimal(10,7) DEFAULT NULL  COMMENT '经度',
  `latitude` decimal(10,7) DEFAULT NULL  COMMENT '纬度',
  `created_time` timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COMMENT='小车运行信息表';


CREATE TABLE yichao (
    id INT PRIMARY KEY AUTO_INCREMENT,
    carID INT NOT NULL,
    longitude DECIMAL(10, 7) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    image LONGTEXT NOT NULL,
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_sanitized TINYINT(1) NOT NULL DEFAULT 0
);

CREATE TABLE relitu (
    id INT PRIMARY KEY AUTO_INCREMENT,
    longitude DECIMAL(10, 7) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    date DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    is_sanitized TINYINT(1) NOT NULL DEFAULT 0
);

-- Create a stored procedure to insert random data
DELIMITER $$

CREATE PROCEDURE InsertRandomData()
BEGIN
    DECLARE i INT DEFAULT 0;
    DECLARE rand_longitude DECIMAL(10, 7);
    DECLARE rand_latitude DECIMAL(10, 7);
    DECLARE rand_date DATETIME;

    WHILE i < 10000 DO
        -- Generate random longitude within Guangdong's range
        SET rand_longitude = ROUND(RAND() * (117.319 - 109.650) + 109.650, 7); -- 109.6500000 to 117.3190000
        
        -- Generate random latitude within Guangdong's range
        SET rand_latitude = ROUND(RAND() * (25.517 - 20.217) + 20.217, 7);   -- 20.2170000 to 25.5170000
        
        -- Generate a random date between 2023-01-01 and 2024-06-30
        SET rand_date = '2023-01-01 00:00:00' + INTERVAL FLOOR(RAND() * 547) DAY; 
        
        INSERT INTO 'relitu' (longitude, latitude, date)
        VALUES (rand_longitude, rand_latitude, rand_date);

        SET i = i + 1;
    END WHILE;
END$$

DELIMITER ;

-- Call the procedure to insert data
CALL InsertRandomData();

-- Drop the procedure if not needed anymore
DROP PROCEDURE IF EXISTS InsertRandomData;

CREATE TABLE give_point (
    carid INT PRIMARY KEY AUTO_INCREMENT,
    longitude DECIMAL(10, 7) NOT NULL,
    latitude DECIMAL(10, 7) NOT NULL,
    created_time timestamp NOT NULL DEFAULT CURRENT_TIMESTAMP COMMENT '插入时间'
);