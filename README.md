# TrendinessProject
UW-Madison GB760 Twitter Trendiness Project
Group Members: Matt Plantz, Keith Hines, Hao Tran, Chelsi Gondalia, Logan Butson, Daniel Waller, Xinyuan Zhang

**Milestone 1**

Part A- this will start reading tweets from Twitter API sampled stream and stores them in a text file- Tweets.txt, use Ctrl+C to stop. 
1) python server.py 

Part B- this will compute the frequency of the word "is" in Tweets.txt, you may replace "is" with a word or phrase of your choice. 

2) python word_count.py Tweets.txt is

Part C- this will display all the unique words in Tweets.txt alphabetically and compute the size of it. 

3) python vobulary_size.py Tweets.txt

**Milestone 2**

Part A: Create database 'trendy' and tables within to store streamed tweets. 

Assuming host is 'gb760', run the following commands in terminal: 
1) psql
2) create database trendy;
3) \q
4) cd to the directory where 'schema_postgres.sql' is located
5) psql trendy < schema_postgres.sql
6) psql
7) \c trendy <-- go to trendy database
8) \dt  <-- This should show your tables
9) select * from base <-- You should get 0 rows 

Part B: Stream tweets from Twitter API and store them in the tables created previously.

1) python server_postgres_HT.py
2) Ctrl+C to stop

Part C: Takes a word or phrase as an input and calculates its count in the current minute from schema. 

1) python word_count_postgres_HT.py with desired word or phrase in quotes. Ex: python word_count_postgres_HT.py 'covid'
2) server_postgres_HT.py must be running simultaneously

Part D: Counts number of unique words in current minute from schema. 

1) python vocabulary_size_postgres_HT.py
2) server_postgres_HT.py must be running simultaneously

Part E: Takes a word or phrase as an input, then calculates and prints trendiness score and probability of being in the previous minute and current minute. 

1) python trendiness_score_HT.py 'covid' (to calculate trendiness of covid)
2) server_postgres_HT.py must be running simultaneously

**Milestone 3**

#step 0
please make sure the following files are in the same directory:
1)keys_for_m3.py
2)trend_score_for_m3.py
3)word_count_for_m3.py
4)server_to_kafka_xz.py
5)server_from_kafka.py
6)trendiness_kafka.py

#step 1 start kafka server
1)sudo systemctl start kafka
2)sudo systemctl status kafka

#step 2 start kafka producer in window #1
python server_to_kafka_xz.py

#step 3 start kafka consumer B in window #2
python server_from_kafka.py

#step 4 check if the data is saved into database
1)sudo -u postgres psql
2)\c trendy
3)select * from base order by t desc limit 10;
4)\q

#step 5 start kafka consumer C in window #3
#we count trendiness score for the word "this"
python trendiness_kafka.py --word=this --use_nlp=1 --use_hash=1
#the script returns the trendiness score for the word "this" every 10 sec - this can be changed in code
#now we count trendiness score for the phrase "Good Morning"
python trendiness_kafka.py --word="Good Morning" --use_nlp=1 --use_hash=1

**Kafka Partition**

#Step 0 Create Kafka topic with 2 partitions
~/kafka/bin/kafka-topics.sh --create --topic testkfk2 --bootstrap-server
localhost:9092 --partitions 2 --replication-factor 1

#Step 1 Change Kafka.conf

#Step 2 Start Producer
python server_to_kafka.py

#Step 3 Start two consumers
1)python server_from_kafka.py
2)python server_from_kafka.py

**Failure Resilience** #Single consumer error
1)python server_to_kafka.py *in terminal #1*
2)python server_from_kafka.py *in terminal #2*
3)python server_from_kafka.py *in terminal #3*
4)stop one consumer for 10 seconds, the living consumer only receives data from its partition
5)restart the dead consumer, two consumers will soon rebalance





