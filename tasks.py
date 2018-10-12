

from flask import Flask
from celery import Celery
import os
import json

appl = Flask(__name__)

appl.config['CELERY_BROKER_URL'] ='pyamqp://'

appl.config['CELERY_RESULT_BACKEND'] ='rpc://'

celery = Celery(appl.name, broker=appl.config['CELERY_BROKER_URL'])
celery.conf.update(appl.config)

#@celery.task
def openTweetsFile():

    file = open("tweets.txt","r")
    read_file = file.read()
    listofFiles = read_file.split('\n')
    listofFiles = listofFiles[:-1]
    return listofFiles
@celery.task
def readfile():
    #file = openTweetsFile()
    for f in range(0,len(file)-1):
        file = open("0c7526e6-ce8c-4e59-884c-5a15bbca5eb3","r")
        read_file = file.read()
        read_file = read_file.split('\n\n')
        tweet = []
        for t in range(0,len(read_file)-1):
    #for t in range(500):
           json_tweet = json.loads(read_file[t])
           tweet.append(json_tweet["text"])
    return(tweet)

@celery.task
def countpronoun():

    tweets = readfile()
    pronouns = {"hon":0, "han":0, "hen":0, "den":0,"det":0,"denna":0, "denne":0}

    for t in tweets:
        if "hon" in t:
 	   pronouns["hon"] += 1
        if "hen" in t:
            pronouns["hen"]+= 1

        if "han" in t:
            pronouns["han"]  += 1
        if "den" in t:
            pronouns["den"] +=1
        if "det" in t:
            pronouns["det"]  += 1
        if "denne" in t:
            pronouns["denne"] +=1

        if "denna" in t:
            pronouns["denna"] +=1
    json_pronoun = json.dumps(pronouns)
    return json_pronoun


@appl.route('/countpronouns', methods=['GET'])
def main():
    pronouns = countpronoun.delay()
    while pronouns.ready() == False:
         if pronouns.ready() == True:
            result = pronouns.get(timeout=1)
#	    return(result)
    return(result)


if __name__ == '__main__':
    appl.run(host='0.0.0.0',debug=True)
