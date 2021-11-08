# Initial Thought Process for Schema Design -- STILL IN PROGRESS

Our data warehouse will feature two dimension tables that can be joined together using a central fact table. The data currently warehoused in the data lake (tweets.txt) is currently in the form timestamp, tweet_text. 

The main fact table will have the following columns: Unique ID | Date | Time | Tweet Text

The date and time columns will be derived from the timestamp read in from the text file as will the tweet text. A unique ID will be assigned to each tweet in the data with each tweet having its own row. 

The two dimension tables will then separate the time information from the text information. First, the time table will be in the following form: Unique ID | Date | Time

The second table will warehouse the text related to each tweet. It will be in the following form: Unique ID | Tweet Text

Each dimension table will be joined to the fact table using the Unique ID column as a foreign key in both dimension tables. 

The thought process behind this logic is it will allow for a python script to first parse through all the time stamp data and determine the set of tweets needed to be analyzed in the trendiness score calculation. Then, this set of unique IDs can be used to pull all the associated text in the time range and use this text to calculate the score. By separating the two dimension tables, only the time stamp table will need to be parsed to obtain our subset of data for the calculation. This subset can then be used to query the text table and obtain all the text needed for calculation.
