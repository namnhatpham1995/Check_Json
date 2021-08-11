# Check_Json
 Validate Json request
## Installation

- Clone this repo:
	
	```
	$ git clone https://github.com/namnhatpham1995/Check_Json.git
	```

- Install the requirements:
	
	```
	pip install -r requirements.txt
	```

## Usage
- To run application, move to project folder and run:
	
	```
	$ python app.py
	```
 or\\
 	```
	$ python3 app.py
	```
## Test
- To test application, use Postman (https://web.postman.co/) (or any methods) to send Json request to the address  http://[computer's IP address]:5000/check_json \\
for example:\\
	```
             {
                "customerID":1,
                "customerName":"abc",
                "request_info":"ask questions",
                "remoteIP":"123.456.789"
             }
	```
	
## Background
Our customers are sending billions of requests each day that need to be
processed. Today, all incoming requests are processed regardless of
their validity, leading to slower processing. We want to filter out
invalid requests (badly formatted, containing invalid values, missing
required fields, …) but keep a history on a day-by-day basis so that
we can properly charge customers for the traffic they send.

## Task
You must write an HTTP service that 
- receives requests generated by our collector
- check the validity of each request
- reject invalid requests
- count and store statistics per customer per hour
Your code should contain a stub function to which you should pass all valid requests.

The service must also provide
- an endpoint to get the statistics
  - for a specific customer 
  AND
  - a specific day
The response must also contain the total number of requests for that day.

### Requests considered as invalid are:
* malformed JSON
* missing one or more fields
* with a customer ID not found in the database or for a customer which is disabled
* with a remote IP address which is in the blacklist
* with a user agent which is in the blacklist

### The stats table will contain:
* one entry per hour and per customer ID
* the `request_count` column contains the number of valid requests
* the `invalid_count` column will be used for the number of invalid requests
## Sample Data

### Sample Request
```json
{"customerID":1,"tagID":2,"userID":"aaaaaaaa-bbbb-cccc-1111-222222222222","remoteIP":"123.234.56.78","timestamp":1500000000}
```

### Suggested Tables

```sql
CREATE TABLE `customer` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `active` tinyint(1) unsigned NOT NULL DEFAULT '1',
  PRIMARY KEY (`id`)
);
```
```sql
INSERT INTO `customer` VALUES (1,'Big News Media Corp',1),(2,'Online Mega Store',1),(3,'Nachoroo Delivery',0),(4,'Euro Telecom Group',1);
```
```sql
CREATE TABLE `ip_blacklist` (
  `ip` int(11) unsigned NOT NULL,
  PRIMARY KEY (`ip`)
);
```
```sql
INSERT INTO `ip_blacklist` VALUES (0),(2130706433),(4294967295);
```
```sql
CREATE TABLE `ua_blacklist` (
  `ua` varchar(255) NOT NULL,
  PRIMARY KEY (`ua`)
);
```
```sql
INSERT INTO `ua_blacklist` VALUES ('A6-Indexer'),('Googlebot-News'),('Googlebot');
```
```sql
CREATE TABLE `hourly_stats` (
  `id` int(11) unsigned NOT NULL AUTO_INCREMENT,
  `customer_id` int(11) unsigned NOT NULL,
  `time` timestamp NOT NULL,
  `request_count` bigint(20) unsigned NOT NULL DEFAULT '0',
  `invalid_count` bigint(20) unsigned NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  UNIQUE KEY `unique_customer_time` (`customer_id`,`time`),
  KEY `customer_idx` (`customer_id`),
  CONSTRAINT `hourly_stats_customer_id` FOREIGN KEY (`customer_id`) REFERENCES `customer` (`id`) ON DELETE CASCADE ON UPDATE NO ACTION
);
```
