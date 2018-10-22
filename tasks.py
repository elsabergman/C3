
from flask import Flask
from celery import Celery
import os
import json
import re
appl = Flask(__name__)

#appl.config['CELERY_BROKER_URL'] ='pyamqp://'

#appl.config['CELERY_RESULT_BACKEND'] ='rpc://'

#celery = Celery(appl.name, broker=appl.config['CELERY_BROKER_URL'])

celery = Celery('tasks'', backend='rpc://', broker = 'pyamqp://')
#celery.conf.update(appl.config)

@celery.task
def openTweetsFile():

    file = open("tweets.txt","r")
    read_file = file.read()
    read_file = read_file.strip()
    listofFiles = read_file.split('\n')
    return listofFiles

@celery.task
def testfile():
    tweet = []
    thefile = open("test.txt","r")
    read_file = thefile.read()
    read_file = read_file.split('\n\n')
    for t in range(0,len(read_file)):
        json_tweet = json.loads(read_file[t])
        tweet.append(json_tweet["text"])

    return(tweet)
@celery.task
def readfile():
    file = openTweetsFile()
    tweet = []
    for f in file:

        thefile = open(f,"r")
        read_file = thefile.read()
        read_file = read_file.split('\n\n')
       	for t in range(0,len(read_file)-1):
           json_tweet = json.loads(read_file[t])
           tweet.append(json_tweet["text"])

    return(tweet)

@celery.task
def removeRT():
    tweets = readfile()
    tweetsNoRT = []
    for t in tweets:
        if t.startswith("RT ") == False:
	    tweetsNoRT.append(t)
    return(tweetsNoRT)

def tweetCount():
    tweets = removeRT()
    tweetCount = 0
    for t in tweets:
        tweetCount += 1
    return tweetCount


@celery.task
def countpronoun():

    tweets = removeRT()
    pronouns = {"hon":0, "han":0, "hen":0, "den":0,"det":0,"denna":0, "denne":0}
    for line in tweets:
	for word in line.split():
	    word = re.sub(r"[^a-zA-Z0-9]+",'', word)
            word = word.lower()
            if "hon" == word:
	        pronouns["hon"] += 1
            if "hen" == word:
                pronouns["hen"]+= 1
            if "han" == word:
                pronouns["han"]  += 1
            if "den" == word:
                pronouns["den"] +=1
            if "det" == word:
                pronouns["det"]  += 1
            if "denne" == word:
                pronouns["denne"] +=1
            if "denna" == word:
                pronouns["denna"] +=1
    json_pronoun = json.dumps(pronouns)
    return json_pronoun
@appl.route("/countpronouns", methods=['GET'])
def main():
     pronouns = countpronoun.delay()
     while pronouns.ready() == False:
         continue
     if pronouns.ready() == True:
         result = pronouns.get(timeout=1)
         return(result + "\n")

if __name__ == '__main__':
    appl.run(host='0.0.0.0',debug=True)
