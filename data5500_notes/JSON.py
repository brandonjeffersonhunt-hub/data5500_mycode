#JSON stands for Java Script object notation. when you build an object in java script it is saved in javas own notation which is JSON
#JSON much more readable than XML. Python disctionaries are just like JSON making them very compatable together
#API stands for application programming interface. allows you to connect to a data endpoint and send data
#rest APi is a web JSON api but it has more functionality including authentication
#method to get data from web API. take URL, put in browser, decide what information you need, make that info variables in your python code

#what is the score of the associated word mallard
import json
import requests

# example url to query datamuse web json api
url = "https://api.datamuse.com/words?ml=duck"

# variables to query alphavantage
word = 'duck'
key_word = "word"
key_score = "score"
search_word = "mallard"

#generate url
url = 'https://api.datamuse.com/words?ml=' + word
print(url)

request = requests.get(url)
# print(request.text) # print to double check data from web json api is good
dct_full = json.loads(request.text)