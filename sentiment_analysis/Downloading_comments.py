#Importing libraries
import pandas as pd
import requests
from random import randint
import json
import os
import time 
import time

os.chdir(path)
keys=["keys"]
#Key check
keys3=[]
n=1
for k in range(len(keys)):
    base_url="https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&"
    dum_url=base_url+"key="+keys[k]+"&id=UCw9Ponb04uNH2AT5gPZ2z6A"
    print dum_url
    responses=requests.get(dum_url)
    if responses.status_code !=403 and responses.status_code !=400:
       keys3.append(keys[k])
    else:
       continue

keys2=keys3[:]
len(keys2)

def get_random_api_key(keys2):
    keys2
    random_no = randint(0, len(keys2)-1)
    random_api_key = keys2[random_no]
    return random_api_key,random_no  

#Reading video ids
#def sentiment_analysis(emailid):
source=pd.read_csv("source.csv",header=None,encoding="utf-8")

columns=["videoid", "total","positive", "neutral", "negative"]
sentiment_fin=pd.DataFrame(columns=columns)

#Get comments from youtube
base_url = 'https://www.googleapis.com/youtube/v3/commentThreads?'
base_url1='textFormat=plainText&part=snippet&key='
base_url2='&maxResults=100&pageToken='
elapsed_fin=0
authorDisplayName=[]
textDisplay=[]
publishedAt=[]
authorChannelId=[]
videoId=[]

columns=["videoId", "authorChannelId","authorDisplayName", "publishedAt", "textDisplay"]
comment_fin=pd.DataFrame(columns=columns)
    

#    emailid="nilanjan"
for i in range(len(source)):
    
    sentiment_temp=pd.DataFrame(index=range(1),columns=columns)
    sentiment_temp=sentiment_temp.fillna("N/A")
    positive=0
    neutral=0
    negative=0
#    video_ids="nHoDQP_Eacs"
    video_ids=source.iloc[i,0]
    
    token=''
    length=0
    
#    textDisplay1=[]
    
    while token is not None:
        start=time.time()
        while True:
            if len(keys2)!=0:
                rand_key=get_random_api_key(keys2)
                url=base_url+base_url1+rand_key[0]+"&videoId="+video_ids+base_url2+token
                print url
        
                resp = requests.get(url)
                
                if responses.status_code == 200:
                    break
                elif responses.status_code == 400:
                    print "bad request"
                    break
                elif responses.status_code == 404:
                    print "skipped"
                    break
                elif responses.status_code == 403:
                    check_json= json.loads(responses.text,encoding='utf-8')
                    error_json=check_json.get("error").get("errors")[0].get("reason")
                    if error_json=="commentsDisabled":
                        print "skipped"
                        
                        break
                    elif error_json=="dailyLimitExceeded":
                        print "trying.."
#                        countr+=1
                        print responses.status_code
                        index=rand_key[1]
                        del keys2[index]
#                            print keys2
                        continue
            else:
                print "keys are done"
                break
        
        
        if resp.status_code==200:
            data = json.loads(resp.text, "utf-8")
            
            token=data.get("nextPageToken")
            if data.get("items"):
                for item in data.get("items"):
                    comment_temp=pd.DataFrame(index=range(1),columns=columns)
                    comment_temp=comment_temp.fillna("N/A")
                    if item.get("snippet").get("topLevelComment").get("snippet"):
                        if item.get("snippet").get("topLevelComment").get("snippet").get("videoId"):
                            comment_temp.iloc[i,0]=item.get("snippet").get("topLevelComment").get("snippet").get("videoId")
                        if item.get("snippet").get("topLevelComment").get("snippet").get("authorChannelId"):
                            comment_temp.iloc[i,1]=item.get("snippet").get("topLevelComment").get("snippet").get("authorChannelId").get("value")
                        if item.get("snippet").get("topLevelComment").get("snippet").get("authorDisplayName"):
                            comment_temp.iloc[i,2]=item.get("snippet").get("topLevelComment").get("snippet").get("authorDisplayName")
                        if item.get("snippet").get("topLevelComment").get("snippet").get("publishedAt"):
                            comment_temp.iloc[i,3]=item.get("snippet").get("topLevelComment").get("snippet").get("publishedAt")
                        if item.get("snippet").get("topLevelComment").get("snippet").get("textDisplay"):
                            comment_temp.iloc[i,4]=item.get("snippet").get("topLevelComment").get("snippet").get("textDisplay").replace("\r"," ").replace("\n"," ").replace("\t"," ")
    #                   
                    comment_fin=comment_fin.append(comment_temp)        
        end=time.time()
        elapsed=end-start
        elapsed_fin+=elapsed
        
        print elapsed,elapsed_fin,len(comment_fin)
        
comment_fin.to_csv('Comments.csv', sep="\t", encoding="utf-8")
