/*
Navicat MySQL Data Transfer

Source Server         : localhost
Source Server Version : 50617
Source Host           : localhost:3306
Source Database       : crawl

Target Server Type    : MYSQL
Target Server Version : 50617
File Encoding         : 65001

Date: 2017-11-17 17:54:04
*/

SET FOREIGN_KEY_CHECKS=0;

-- ----------------------------
-- Table structure for `crawl_article`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_article`;
CREATE TABLE `crawl_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `author` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `body` text COLLATE utf8_unicode_ci,
  `keywords` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `favor` int(11) DEFAULT '0',
  `disfavor` int(11) DEFAULT '0',
  `type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state` tinyint(4) DEFAULT '1',
  `source_site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_id` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_url` varchar(255) COLLATE utf8_unicode_ci NOT NULL,
  `hits` int(11) DEFAULT '0',
  `publish_time` datetime DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_title` (`title`),
  KEY `ids_keywords` (`keywords`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_article
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_baidu_tongji`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_baidu_tongji`;
CREATE TABLE `crawl_baidu_tongji` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `access_time` datetime NOT NULL,
  `area` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `keywords` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `entry_page` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ip` varchar(15) COLLATE utf8_unicode_ci DEFAULT NULL,
  `user_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `visit_time` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `visit_pages` int(11) DEFAULT NULL,
  `visitorType` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `visitorFrequency` int(11) DEFAULT NULL,
  `lastVisitTime` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `endPage` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `deviceType` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fromType` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fromurl` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `fromAccount` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `isp` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `os` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `osType` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browser` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `browserType` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `language` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `resolution` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `color` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `accessPage` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `antiCode` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `site` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_baidu_tongji
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_china_time`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_china_time`;
CREATE TABLE `crawl_china_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `value` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `type` enum('rate','time') COLLATE utf8_unicode_ci DEFAULT 'rate',
  `day` datetime DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_china_time
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_douban`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_douban`;
CREATE TABLE `crawl_douban` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci NOT NULL,
  `director` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `scriptwriter` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `actor` varchar(512) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(50) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `duration` int(11) DEFAULT NULL,
  `introduct` text CHARACTER SET utf8 COLLATE utf8_unicode_ci,
  `img` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `language` char(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT '英语' COMMENT '语言',
  `alias` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '别名',
  `score1` float(3,1) DEFAULT NULL,
  `score2` float(3,1) DEFAULT NULL,
  `score3` float(3,1) DEFAULT NULL,
  `score4` float(3,1) DEFAULT NULL,
  `score5` float(3,1) DEFAULT NULL,
  `score` float(3,1) DEFAULT NULL,
  `short_comment` text CHARACTER SET utf8 COLLATE utf8_unicode_ci COMMENT '短评',
  `long_comment` text CHARACTER SET utf8 COLLATE utf8_unicode_ci COMMENT '影评',
  `comment_num` int(3) DEFAULT NULL COMMENT '评价人数',
  `imdb_link` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'imdb地址',
  `release_time` char(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '上映时间',
  `is_tv` tinyint(4) DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  `source_url` varchar(255) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_site` varchar(32) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL,
  `crawl_introduce` varchar(64) CHARACTER SET utf8 COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '抓取说明，如 "豆瓣电影top250.."',
  `updated_time` datetime DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- ----------------------------
-- Records of crawl_douban
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_economic_calendar`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_economic_calendar`;
CREATE TABLE `crawl_economic_calendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `quota_name` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pub_time` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `importance` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `former_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `predicted_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `published_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `influence` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_id` int(11) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  `dataname` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `datename` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dataname_id` int(11) DEFAULT NULL,
  `unit` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `source_id` (`source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_economic_calendar
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_economic_event`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_economic_event`;
CREATE TABLE `crawl_economic_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `importance` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event` text COLLATE utf8_unicode_ci,
  `date` date DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  `source_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_economic_event
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_economic_holiday`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_economic_holiday`;
CREATE TABLE `crawl_economic_holiday` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `market` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `holiday_name` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `detail` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  `source_id` int(11) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_economic_holiday
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_economic_jiedu`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_economic_jiedu`;
CREATE TABLE `crawl_economic_jiedu` (
  `dataname_id` int(11) NOT NULL,
  `next_pub_time` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pub_agent` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pub_frequency` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `count_way` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_influence` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_define` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `funny_read` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`dataname_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_economic_jiedu
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_error_top`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_error_top`;
CREATE TABLE `crawl_error_top` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monitor_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `value` smallint(6) NOT NULL,
  `type` char(5) COLLATE utf8_unicode_ci DEFAULT 'time' COMMENT '故障时间:time, 故障次数:count',
  `day` datetime DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_error_top
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_fx678_economic_calendar`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_fx678_economic_calendar`;
CREATE TABLE `crawl_fx678_economic_calendar` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `quota_name` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pub_time` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `importance` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `former_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `predicted_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `published_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `influence` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_id` char(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  `position` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dataname` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `datename` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dataname_id` int(11) DEFAULT NULL,
  `unit` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `source_id` (`source_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_fx678_economic_calendar
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_fx678_economic_event`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_fx678_economic_event`;
CREATE TABLE `crawl_fx678_economic_event` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `city` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `importance` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `event` text COLLATE utf8_unicode_ci,
  `date` date DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  `source_id` char(32) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_fx678_economic_event
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_fx678_economic_holiday`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_fx678_economic_holiday`;
CREATE TABLE `crawl_fx678_economic_holiday` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` varchar(24) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `market` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `holiday_name` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `detail` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `date` date DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  `source_id` char(32) COLLATE utf8_unicode_ci NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_fx678_economic_holiday
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_fx678_economic_jiedu`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_fx678_economic_jiedu`;
CREATE TABLE `crawl_fx678_economic_jiedu` (
  `dataname_id` bigint(18) NOT NULL DEFAULT '0',
  `next_pub_time` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pub_agent` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pub_frequency` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `count_way` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_influence` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `data_define` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `funny_read` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`dataname_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_fx678_economic_jiedu
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_fx678_kuaixun`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_fx678_kuaixun`;
CREATE TABLE `crawl_fx678_kuaixun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `publish_time` datetime NOT NULL,
  `body` text COLLATE utf8_unicode_ci,
  `time_detail` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `importance` tinyint(4) NOT NULL DEFAULT '1',
  `more_link` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dateid` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t0` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t5` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t7` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t8` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t10` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t12` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` tinyint(4) DEFAULT NULL,
  `real_time` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `former_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `predicted_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `published_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `influnce` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `star` tinyint(4) DEFAULT NULL,
  `calendar_id` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_fx678_kuaixun
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_ibrebates`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_ibrebates`;
CREATE TABLE `crawl_ibrebates` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(64) COLLATE utf8_unicode_ci NOT NULL,
  `description` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `spread_type` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '点差类型',
  `om_spread` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '欧美点差',
  `gold_spread` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '黄金点差',
  `offshore` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '离岸人民币',
  `a_share` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT 'A股',
  `regulatory_authority` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '监管机构',
  `trading_varieties` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '交易品种',
  `platform_type` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `account_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '开设账户类型',
  `scalp` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '剥头皮',
  `hedging` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '对冲',
  `min_transaction` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '交易最小手数',
  `least_entry` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '最少入金',
  `maximum_leverage` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '最高杠杆率',
  `maximum_trading` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '最大交易量',
  `deposit_method` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '出金方式',
  `entry_method` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '入金方式',
  `commission_fee` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '出金手续费',
  `entry_fee` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `account_currency` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rollovers` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '隔夜利息',
  `explosion_proportion` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '爆仓比例',
  `renminbi` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '人民币入金',
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `idx_name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_ibrebates
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_article`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_article`;
CREATE TABLE `crawl_jin10_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `title` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `body` text COLLATE utf8_unicode_ci,
  `publish_time` datetime DEFAULT NULL,
  `author` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `description` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state` tinyint(4) NOT NULL DEFAULT '1',
  `source_id` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_url` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hits` int(11) DEFAULT NULL,
  `keywords` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_jin10_article
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_cftc_c_report`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_cftc_c_report`;
CREATE TABLE `crawl_jin10_cftc_c_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `long_positions` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '多头仓位',
  `short_position` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '空头仓位',
  `cat_name` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '种类',
  `time` date NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='美国商品期货交易委员会CFTC商品类非商业持仓报告';

-- ----------------------------
-- Records of crawl_jin10_cftc_c_report
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_cftc_merchant_currency`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_cftc_merchant_currency`;
CREATE TABLE `crawl_jin10_cftc_merchant_currency` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `long_positions` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '多头仓位',
  `short_position` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '空头仓位',
  `cat_name` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '种类',
  `time` date NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='美国商品期货交易委员会CFTC外汇类商业持仓报告';

-- ----------------------------
-- Records of crawl_jin10_cftc_merchant_currency
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_cftc_merchant_goods`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_cftc_merchant_goods`;
CREATE TABLE `crawl_jin10_cftc_merchant_goods` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `long_positions` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '多头仓位',
  `short_position` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '空头仓位',
  `cat_name` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '种类',
  `time` date NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='美国商品期货交易委员会CFTC商品类商业持仓报告';

-- ----------------------------
-- Records of crawl_jin10_cftc_merchant_goods
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_cftc_nc_report`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_cftc_nc_report`;
CREATE TABLE `crawl_jin10_cftc_nc_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `long_positions` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '多头仓位',
  `short_position` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '空头仓位',
  `cat_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL COMMENT '种类',
  `time` date NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='美国商品期货交易委员会CFTC外汇类非商业持仓报告';

-- ----------------------------
-- Records of crawl_jin10_cftc_nc_report
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_cme_energy_report`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_cme_energy_report`;
CREATE TABLE `crawl_jin10_cme_energy_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '商品',
  `type_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '类型',
  `time` date NOT NULL,
  `transaction_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '电子交易合约',
  `inside_closing_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '场内成交合约',
  `outside_closing_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '场外成交合约',
  `volume` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '成交量',
  `open_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '未平仓合约',
  `position_change` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '持仓变化',
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='芝加哥商业交易所（CME）能源类商品成交量报告';

-- ----------------------------
-- Records of crawl_jin10_cme_energy_report
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_cme_fx_report`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_cme_fx_report`;
CREATE TABLE `crawl_jin10_cme_fx_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '商品',
  `type_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '类型',
  `time` date NOT NULL,
  `transaction_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '电子交易合约',
  `inside_closing_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '场内成交合约',
  `outside_closing_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '场外成交合约',
  `volume` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '成交量',
  `open_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '未平仓合约',
  `position_change` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='芝加哥商业交易所（CME）外汇类商品成交量报告';

-- ----------------------------
-- Records of crawl_jin10_cme_fx_report
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_cme_report`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_cme_report`;
CREATE TABLE `crawl_jin10_cme_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '商品',
  `type_name` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '类型',
  `time` date NOT NULL,
  `transaction_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '电子交易合约',
  `inside_closing_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '场内成交合约',
  `outside_closing_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '场外成交合约',
  `volume` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '成交量',
  `open_contract` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '未平仓合约',
  `position_change` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='芝加哥商业交易所（CME）金属类商品成交量报告';

-- ----------------------------
-- Records of crawl_jin10_cme_report
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_etf`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_etf`;
CREATE TABLE `crawl_jin10_etf` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `time` date NOT NULL,
  `total_inventory` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '总库存',
  `increase` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '增持减持',
  `total_value` varchar(32) COLLATE utf8_unicode_ci NOT NULL COMMENT '总价值',
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='全球最大白银ETF--iShares Silver Trust持仓报告';

-- ----------------------------
-- Records of crawl_jin10_etf
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_kuaixun`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_kuaixun`;
CREATE TABLE `crawl_jin10_kuaixun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `publish_time` datetime NOT NULL,
  `body` text COLLATE utf8_unicode_ci,
  `time_detail` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `importance` tinyint(4) NOT NULL DEFAULT '1',
  `more_link` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dateid` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t0` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t5` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t7` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t8` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t10` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t12` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` tinyint(4) DEFAULT NULL,
  `real_time` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `former_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `predicted_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `published_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `influnce` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `star` tinyint(4) DEFAULT NULL,
  `calendar_id` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_jin10_kuaixun
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_lme_report`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_lme_report`;
CREATE TABLE `crawl_jin10_lme_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `cat_name` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `stock` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '库存',
  `registered_warehouse_receipt` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '注册仓单',
  `canceled_warehouse_receipt` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '注销仓单',
  `time` date NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='伦敦金属交易所（LME）库存报告';

-- ----------------------------
-- Records of crawl_jin10_lme_report
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_lme_traders_report`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_lme_traders_report`;
CREATE TABLE `crawl_jin10_lme_traders_report` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `long_positions` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '多头仓位',
  `short_position` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '空头仓位',
  `cat_name` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '种类',
  `time` date NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='伦敦金属交易所（LME）持仓报告';

-- ----------------------------
-- Records of crawl_jin10_lme_traders_report
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_nonfarm_payrolls`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_nonfarm_payrolls`;
CREATE TABLE `crawl_jin10_nonfarm_payrolls` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` date NOT NULL,
  `cat_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `former_value` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '前值',
  `pub_value` varchar(16) COLLATE utf8_unicode_ci NOT NULL COMMENT '今值',
  `expected_value` varchar(16) COLLATE utf8_unicode_ci NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='美国非农就业人数报告';

-- ----------------------------
-- Records of crawl_jin10_nonfarm_payrolls
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends`;
CREATE TABLE `crawl_jin10_ssi_trends` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_alpari`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_alpari`;
CREATE TABLE `crawl_jin10_ssi_trends_alpari` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_alpari
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_dukscopy`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_dukscopy`;
CREATE TABLE `crawl_jin10_ssi_trends_dukscopy` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_dukscopy
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_fiboforx`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_fiboforx`;
CREATE TABLE `crawl_jin10_ssi_trends_fiboforx` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_fiboforx
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_forxfact`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_forxfact`;
CREATE TABLE `crawl_jin10_ssi_trends_forxfact` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_forxfact
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_ftroanda`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_ftroanda`;
CREATE TABLE `crawl_jin10_ssi_trends_ftroanda` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_ftroanda
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_fxcm`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_fxcm`;
CREATE TABLE `crawl_jin10_ssi_trends_fxcm` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_fxcm
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_instfor`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_instfor`;
CREATE TABLE `crawl_jin10_ssi_trends_instfor` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_instfor
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_myfxbook`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_myfxbook`;
CREATE TABLE `crawl_jin10_ssi_trends_myfxbook` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_myfxbook
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_jin10_ssi_trends_saxobank`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_jin10_ssi_trends_saxobank`;
CREATE TABLE `crawl_jin10_ssi_trends_saxobank` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `platform` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `type` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `long_position` decimal(4,2) NOT NULL,
  `time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  `created_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `idx_time` (`time`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci COMMENT='投机情绪报告';

-- ----------------------------
-- Records of crawl_jin10_ssi_trends_saxobank
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_lianjia_agent`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_lianjia_agent`;
CREATE TABLE `crawl_lianjia_agent` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `agent_id` bigint(16) DEFAULT NULL,
  `reason` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `agent_url` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `agent_level` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `agent_photo` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `feedback_good_rate` tinyint(4) DEFAULT NULL,
  `comment_count` int(11) DEFAULT NULL,
  `total_comment_score` varchar(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `agent_phone` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_lianjia_agent
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_lianjia_feedback`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_lianjia_feedback`;
CREATE TABLE `crawl_lianjia_feedback` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` int(11) NOT NULL,
  `comment` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `agent_id` int(16) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_lianjia_feedback
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_lianjia_house`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_lianjia_house`;
CREATE TABLE `crawl_lianjia_house` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `house_id` bigint(20) DEFAULT NULL,
  `title` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `residential` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `residential_id` bigint(18) DEFAULT NULL,
  `layout` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `area` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `direction` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `renovation` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '装修情况',
  `elevator` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `flood` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `related_name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `related_href` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `followed` int(11) DEFAULT NULL,
  `visited` int(11) DEFAULT NULL,
  `pub_time` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `tag` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `unit_price` int(11) DEFAULT NULL,
  `images` text COLLATE utf8_unicode_ci,
  `img_desc` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `district` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `apartment_structure` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `street` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `address` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `building_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `ladder` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `heating` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `property_term` int(11) DEFAULT NULL,
  `list_time` date DEFAULT NULL,
  `ownership` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `last_trade` date DEFAULT NULL,
  `purpose` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `hold_years` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `mortgage` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `house_register` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `core_point` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `periphery` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `traffic` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `residential_desc` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `layout_datas` text COLLATE utf8_unicode_ci,
  `layout_desc` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `img_layout` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_id` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_url` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state` tinyint(4) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=2668 DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;


-- ----------------------------
-- Table structure for `crawl_lianjia_visited`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_lianjia_visited`;
CREATE TABLE `crawl_lianjia_visited` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `hourse_id` int(11) NOT NULL,
  `visited_time` date DEFAULT NULL,
  `agent_id` bigint(16) DEFAULT NULL,
  `see_count` int(11) DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_lianjia_visited
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_lianjian_house`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_lianjian_house`;
CREATE TABLE `crawl_lianjian_house` (
  `id` int(11) NOT NULL,
  `title` varchar(256) COLLATE utf8_unicode_ci NOT NULL,
  `residential` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '小区',
  `img_desc` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `residential_id` bigint(13) DEFAULT NULL,
  `house_id` bigint(16) DEFAULT NULL,
  `layout` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `area` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '面积',
  `direction` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `renovation` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `elevator` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `flood` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `related_name` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '相关搜索',
  `related_href` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `followed` int(11) DEFAULT NULL COMMENT '关注',
  `visited` int(11) DEFAULT NULL COMMENT '带看',
  `pub_time` varchar(16) COLLATE utf8_unicode_ci DEFAULT NULL,
  `tag` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `price` int(11) DEFAULT NULL,
  `unit_price` int(11) DEFAULT NULL,
  `images` varchar(1024) COLLATE utf8_unicode_ci DEFAULT NULL,
  `district` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '区',
  `apartment_structure` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '户型结构',
  `street` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '区域片',
  `address` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `building_type` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '建筑类型',
  `ladder` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '梯户比',
  `heating` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `property_term` int(11) DEFAULT NULL COMMENT '产权期限',
  `list_time` date DEFAULT NULL COMMENT '挂牌时间',
  `ownership` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '交易权属',
  `last_trade` date DEFAULT NULL,
  `purpose` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '房屋用途',
  `hold_years` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '持有年限',
  `mortgage` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '抵押信息',
  `house_register` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '房本',
  `core_point` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '核心卖点',
  `periphery` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '周边配套',
  `traffic` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '交通出行',
  `residential_desc` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '小区介绍',
  `layout_desc` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '户型介绍',
  `img_layout` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL COMMENT '户型图',
  `layout_datas` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_id` char(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_url` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state` tinyint(4) DEFAULT '1',
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_lianjian_house
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_monitor_area_stastic`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_monitor_area_stastic`;
CREATE TABLE `crawl_monitor_area_stastic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monitor_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `province` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` char(5) COLLATE utf8_unicode_ci DEFAULT NULL,
  `area` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `mid` int(11) DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `day` datetime DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_monitor_area_stastic
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_monitor_chart`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_monitor_chart`;
CREATE TABLE `crawl_monitor_chart` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `time` datetime NOT NULL,
  `monitor_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` char(5) COLLATE utf8_unicode_ci DEFAULT 'rate' COMMENT 'rate,time',
  `day` datetime DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_monitor_chart
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_monitor_province`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_monitor_province`;
CREATE TABLE `crawl_monitor_province` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monitor_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `monitor_province` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(10) COLLATE utf8_unicode_ci NOT NULL,
  `type` char(5) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'rate' COMMENT 'rate:可用率, time:响应时间',
  `day` datetime DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_monitor_province
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_monitor_stastic`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_monitor_stastic`;
CREATE TABLE `crawl_monitor_stastic` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `mid` int(11) NOT NULL,
  `day` datetime NOT NULL,
  `min` double(10,3) NOT NULL,
  `max` double(10,3) NOT NULL,
  `avg` double(10,3) NOT NULL,
  `time_st` char(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `all_time` int(11) NOT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_monitor_stastic
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_monitor_type`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_monitor_type`;
CREATE TABLE `crawl_monitor_type` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `monitor_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `province` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `rate` varchar(6) COLLATE utf8_unicode_ci NOT NULL,
  `type_name` char(3) COLLATE utf8_unicode_ci NOT NULL,
  `catname` char(5) COLLATE utf8_unicode_ci DEFAULT 'rate' COMMENT '可用率:rate, 时间:time',
  `day` datetime DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_monitor_type
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_province_time`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_province_time`;
CREATE TABLE `crawl_province_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `province_name` varchar(32) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(6) COLLATE utf8_unicode_ci NOT NULL,
  `type` char(5) COLLATE utf8_unicode_ci NOT NULL DEFAULT 'rate' COMMENT 'time:响应时间, rate:可用率',
  `day` datetime DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_province_time
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_type_time`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_type_time`;
CREATE TABLE `crawl_type_time` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `type_name` char(3) COLLATE utf8_unicode_ci NOT NULL,
  `value` varchar(6) COLLATE utf8_unicode_ci NOT NULL,
  `type` char(5) COLLATE utf8_unicode_ci DEFAULT 'rate' COMMENT '可用率:rate, 响应时间:time',
  `day` datetime DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime NOT NULL,
  `updated_time` datetime NOT NULL,
  PRIMARY KEY (`id`),
  KEY `ids_day` (`day`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_type_time
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_wallstreetcn_kuaixun`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_wallstreetcn_kuaixun`;
CREATE TABLE `crawl_wallstreetcn_kuaixun` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `publish_time` datetime NOT NULL,
  `body` text COLLATE utf8_unicode_ci,
  `time_detail` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `importance` tinyint(4) NOT NULL DEFAULT '1',
  `more_link` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `image` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `dateid` varchar(20) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t0` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t5` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t7` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t8` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t10` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `t12` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `type` tinyint(4) DEFAULT NULL,
  `real_time` varchar(12) COLLATE utf8_unicode_ci DEFAULT NULL,
  `former_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `predicted_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `published_value` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `country` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `influnce` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `star` tinyint(4) DEFAULT NULL,
  `typename` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `calendar_id` varchar(10) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_wallstreetcn_kuaixun
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_weixin_article`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_weixin_article`;
CREATE TABLE `crawl_weixin_article` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `publish_time` datetime DEFAULT NULL,
  `title` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `favor` int(11) DEFAULT NULL,
  `disfavor` int(11) DEFAULT NULL,
  `body` text COLLATE utf8_unicode_ci,
  `type` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `state` smallint(6) DEFAULT NULL,
  `image` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_url` varchar(255) COLLATE utf8_unicode_ci DEFAULT NULL,
  `source_id` varchar(50) COLLATE utf8_unicode_ci DEFAULT NULL,
  `from_user` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_weixin_article
-- ----------------------------

-- ----------------------------
-- Table structure for `crawl_zhanzhang`
-- ----------------------------
DROP TABLE IF EXISTS `crawl_zhanzhang`;
CREATE TABLE `crawl_zhanzhang` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `keywords` varchar(128) COLLATE utf8_unicode_ci DEFAULT NULL,
  `total_index` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `pc_index` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `mobile_index` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `baidu_index` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `shoulu_count` varchar(64) COLLATE utf8_unicode_ci DEFAULT NULL,
  `shoulu_page` varchar(512) COLLATE utf8_unicode_ci DEFAULT NULL,
  `shoulu_title` varchar(256) COLLATE utf8_unicode_ci DEFAULT NULL,
  `site` varchar(32) COLLATE utf8_unicode_ci DEFAULT NULL,
  `created_time` datetime DEFAULT NULL,
  `updated_time` datetime DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of crawl_zhanzhang
-- ----------------------------

-- ----------------------------
-- Table structure for `users`
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_unicode_ci;

-- ----------------------------
-- Records of users
-- ----------------------------
