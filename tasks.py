
from celery import Celery
import json 

app = Celery('tasks', backend='rpc://', broker='pyamqp://')

@app.task
def readfile():

    file = open("0c7526e6-ce8c-4e59-884c-5a15bbca5eb3","r")
    read_file = file.read()
    read_file = read_file.split('\n\n')
    tweet = []
    for t in range(0,len(read_file)-1):
       json_tweet = json.loads(read_file[t])
       tweet.append(json_tweet["text"])
    return(tweet)
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
    print(pronouns)
def createfile():

    with open('data.txt', 'w') as outfile:
        json.dump(data, outfile)

    return data

