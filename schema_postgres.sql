-- Basis for schema_postgres.sql
-- Still incomplete but is the basis for the sql commands for milestone 2

CREATE OR REPLACE TABLE fact (
	unique_id SERIAL,
	date TIMESTAMP,
	time INTEGER,
	tweet_text TEXT,
	PRIMARY KEY (unique_id)
	);

CREATE OR REPLACE TABLE time (
	unique_id SERIAL,
	date TIMESTAMP,
	time TIMESTAMP,
	PRIMARY KEY (unique_id)
	);

COPY fact(date, tweet_text)
FROM ### insert tweets.txt file location here ###
DELIMITER ‘,’
CSV HEADER;

COPY time(date)
FROM ### insert tweets.txt file location here ###
DELIMITER ‘,’
CSV HEADER;
