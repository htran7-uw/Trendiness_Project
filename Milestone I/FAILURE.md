1. If URL does not exist -- whether it is changed inside the script, or the website changes on their end. Our code will initiate the error code and give the friendly failure message of "You might have the wrong URL inserted."  Example below.


Attempt #0
The error code is still 400.
Let's wait 2 seconds and try again
Attempt #1
The error code is still 400.
Let's wait 2 seconds and try again
Attempt #2
The error code is still 400.
Let's wait 2 seconds and try again
Attempt #3
The error code is still 400.
Let's wait 2 seconds and try again
Attempt #4
The error code is still 400.
Let's wait 2 seconds and try again
Attempt #5
The error code is still 400.
Let's wait 2 seconds and try again
Traceback (most recent call last):
  File "/home/gb760/PycharmProjects/pythonProject/main.py", line 117, in <module>
    main()
  File "/home/gb760/PycharmProjects/pythonProject/main.py", line 109, in main
    connect_to_endpoint(url)
  File "/home/gb760/PycharmProjects/pythonProject/main.py", line 71, in connect_to_endpoint
    if json_response['data']['lang'] == 'en':
KeyError: 'data'
Looks like we still get an error code of 400 You might have the wrong URL inserted.
{
    "detail": "One or more parameters to your request was invalid.",
    "errors": [
        {
            "message": "The `id` query parameter value [samstream] is not valid",
            "parameters": {
                "id": [
                    "samstream"
                ]
            }
        }
    ],
    "title": "Invalid Request",
    "type": "https://api.twitter.com/2/problems/invalid-request"
}

Process finished with exit code 1



2. Pausing the script could present and issue. This is what is displayed after the script has been runnign for 3 minutes, has not been completed yet, and then the stop button is pressed. 
 
Somebody paused the script! 
 Re-run the script to continue. However, you will be overwriting your file if you do. 
 If you do not want to lose that file, store it somewhere else and then re-run the script.



Process finished with exit code 0

3. If the script is paused in the middle of its running, then re-run script is pressed. We were concerned memory would be an issue if the user had multiple of incomplete Tweet.txt files being stored, and didn't understand why couldn't complete the process for real. If this occurs, below is the message that will be shown.

/home/gb760/PycharmProjects/pythonProject/venv/bin/python /home/gb760/PycharmProjects/pythonProject/main.py
We replaced the Tweets.txt file so you do not run out of disk space.
200

  For Hao:
  
 4. If Exit from PyCharm is attempted while Main is running, whether that be through 'Terminate' or 'Disconnect' or computer shutting down the script does stop -- however we never showcase that previous "Somebody paused the script" code.
 
 5. If the Tweets.txt file is edited while the main script is running, saving gets a little funky. The user is presented with the option to 'Load File System Change' or 'Keep Memory Changes'. If you select Keep Memory Changes, then edit even some more, then select Load File Changes -- the stream of Tweets gets messed with greatly. If it is possible, it may be a good idea to error out or pause if Tweets.txt is edited while script is running?
