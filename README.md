# TrendinessProject
UW-Madison GB760 Twitter Trendiness Project
Group Members: Matt Plantz, Keith Hines, Hao Tran, Chelsi Gondalia, Logan Butson, Daniel Waller, Xinyuan Zhang

Milestone 1

Part A- this will start reading tweets from Twitter API sampled stream and stores them in a text file- Tweets.txt, use Ctrl+C to stop. 
1) python server.py 

Part B- this will compute the frequency of the word "is" in Tweets.txt, you may replace "is" with a word or phrase of your choice. 
2) python word_count.py Tweets.txt is

Part C- this will display all the unique words in Tweets.txt alphabetically and compute the size of it. 
3) python vobulary_size.py Tweets.txt

Milestone 2 Part A - HT
Create database 
Assuming host is 'gb760', run the following commands in terminal 
1) psql
2) create database trendy;
3) \q
4) cd to the directory where 'schema_postgres.sql' is located
5) psql trendy < schema_postgres.sql
6) psql
7) \c trendy <-- go to trendy database
8) \dt  <-- This should show your tables
9) select * from base <-- You should get 0 rows 

Milestone 3 - XZ

#step 0
please make sure the following files are in the same directory:

clean_text_for_m3.py

keys_for_m3.py

trend_score_for_m3.py

word_count_for_m3.py

server_to_kafka_xz.py

server_from_kafka.py

trendiness_kafka.py

#step 1 start kafka server

sudo systemctl start kafka

sudo systemctl status kafka

#step 2 start kafka producer in window #1

python server_to_kafka_xz.py

#step 3 start kafka consumer B in window #2

python server_from_kafka.py

#step 4 check if the data is saved into database

sudo -u postgres psql

\c trendy

select * from base order by t desc limit 10;

\q

#step 5 start kafka consumer C in window #3

#we count trendiness score for the word "this"

python trendiness_kafka.py --word=this --use_nlp=1 --use_hash=1

#the script returns the trendiness score for the word "this" every 10 sec - this can be changed in code



