COPY words from 'to_sql.csv' 
  DELIMITER ',' 
  CSV HEADER;
ALTER TABLE words 
  ALTER COLUMN time type timestamp 
  USING to_timestamp(time, 'YYYY-MM-DD hh24:mi:ss');
