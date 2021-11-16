-- Basis for schema_postgres.sql
-- Still incomplete but is the basis for the sql commands for milestone 2

CREATE OR REPLACE TABLE base (
	UNIQUE_ID INT GENERATED ALWAYS AS IDENTITY 
	t TIMESTAMP,
	tex TEXT
	);
	
COPY base(t, tex)
FROM '### insert tweets.txt file path here'
DELIMITER ','
CSV HEADER;

-- This section alters the timestamp column into a time and a date column	
BEGIN;

ALTER TABLE base ADD COLUMN dat date;
ALTER TABLE base ADD COLUMN tim time;

UPDATE base
SET
    dat = t::date,
    tim = t::time;

ALTER TABLE base DROP COLUMN t;  

COMMIT;

-- creating dimensional tables

CREATE OR REPLACE TABLE txt (
	UNIQUE_ID SERIAL,
	DAT TIMESTAMP,
	TIM TIMESTAMP,
	TWEET_TXT TEXT,
	PRIMARY KEY (UNIQUE_ID)
	)
CREATE OR REPLACE TABLE time_date(
	UNIQUE_ID SERIAL,
	DAT TIMESTAMP,
	TIM TIMESTAMP,
	PRIMARY KEY (UNIQUE_ID)
	)

-- Copy data from base table to dimensional tables

COPY txt(UNIQUE_ID, DAT, TIM, TWEET_TXT)
FROM base;

COPY time_date(UNIQUE_ID, DAT, TIM)
FROM base;
