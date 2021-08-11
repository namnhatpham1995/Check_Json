CREATE DATABASE IF NOT EXISTS customer_DB;
USE customer_DB;
CREATE TABLE IF NOT EXISTS customer (
    id INT(11) UNSIGNED NOT NULL PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(255) NOT NULL UNIQUE,
    active TINYINT(255) UNSIGNED NOT NULL DEFAULT 1
    
);
INSERT INTO customer (name, active)
VALUES ('Big News Media Corp',1),
('Online Mega Store',1),
('Nachoroo Delivery',0),
('Euro Telecom Group',1);

CREATE TABLE IF NOT EXISTS ip_blacklist (
    ip VARCHAR(255) NOT NULL PRIMARY KEY UNIQUE
);
INSERT INTO ip_blacklist(ip)
VALUES ('0.0.0.0'),
('21.30.70.33'),
('192.168.0.123');

CREATE TABLE IF NOT EXISTS ua_blacklist (
    ua VARCHAR(255) NOT NULL PRIMARY KEY UNIQUE
);
INSERT INTO ua_blacklist(ua)
VALUES ('A6-Indexer'),
('Googlebot-News'),
('Googlebot');

CREATE TABLE IF NOT EXISTS hourly_stats (
  `id` INT(11) UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `customer_id` INT(11) UNSIGNED NOT NULL,
  `time` TIMESTAMP NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `request_count` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0',
  `invalid_count` BIGINT(20) UNSIGNED NOT NULL DEFAULT '0',
  KEY `customer_idx` (`customer_id`),
  CONSTRAINT `hourly_stats_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
);
