/*
 Navicat Premium Data Transfer

 Source Server         : test
 Source Server Type    : MySQL
 Source Server Version : 80012 (8.0.12)
 Source Host           : localhost:3306
 Source Schema         : weather_show

 Target Server Type    : MySQL
 Target Server Version : 80012 (8.0.12)
 File Encoding         : 65001

 Date: 15/11/2023 23:00:32
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for t_city
-- ----------------------------
DROP TABLE IF EXISTS `t_city`;
CREATE TABLE `t_city`  (
  `id` int(11) NOT NULL,
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '城市名称',
  `province_id` varbinary(11) NOT NULL COMMENT '对应省份ID',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_province
-- ----------------------------
DROP TABLE IF EXISTS `t_province`;
CREATE TABLE `t_province`  (
  `id` varchar(11) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT 'id',
  `name` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '省份地区名字',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_realtime_weather
-- ----------------------------
DROP TABLE IF EXISTS `t_realtime_weather`;
CREATE TABLE `t_realtime_weather`  (
  `id` int(11) NOT NULL COMMENT 'A',
  `temperature` float NOT NULL COMMENT '温度',
  `weather` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '天气现象',
  `night_weather` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '夜间气象',
  `pressure` float NOT NULL DEFAULT 1000 COMMENT '大气压',
  `humidness` float NOT NULL DEFAULT 0 COMMENT '湿度',
  `precipitation` float NOT NULL DEFAULT 0 COMMENT '降水量',
  `wind` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NULL DEFAULT '不明' COMMENT '方向风力',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

-- ----------------------------
-- Table structure for t_weekly_weather
-- ----------------------------
DROP TABLE IF EXISTS `t_weekly_weather`;
CREATE TABLE `t_weekly_weather`  (
  `id` bigint(16) NOT NULL COMMENT 'id=城市id+日期 （数字拼接），如59298231114=59298+23/11/14',
  `city_id` int(11) NOT NULL COMMENT '城市id',
  `date` date NOT NULL COMMENT '日期',
  `weather` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '白天气象',
  `wind_direction` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '白天风向',
  `wind_power` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '白天风力',
  `min_temp` float NOT NULL COMMENT '最低温度',
  `max_temp` float NOT NULL COMMENT '最高温度',
  `night_weather` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '夜间气象',
  `night_wind_direction` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '夜间风向',
  `night_wind_power` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL COMMENT '夜间风力',
  `update_time` datetime NOT NULL COMMENT '更新时间',
  PRIMARY KEY (`id`) USING BTREE
) ENGINE = MyISAM AUTO_INCREMENT = 1 CHARACTER SET = utf8 COLLATE = utf8_unicode_ci ROW_FORMAT = Dynamic;

SET FOREIGN_KEY_CHECKS = 1;
