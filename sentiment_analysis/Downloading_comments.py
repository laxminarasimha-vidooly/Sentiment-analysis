# -*- coding: utf-8 -*-
"""
Created on Wed Feb 06 16:51:39 2019

@author: Administrator
"""

import pandas as pd
import requests
from random import randint
import json
import os
import time 
#from random import sample 
import time



#path=os.path.dirname(os.path.abspath(__file__))
path=r"C:\Server backup\VIDOOLY NILANJAN\Python\RnD APIs\Py2_Code_for_sentiment_analysis"
os.chdir(path)



            
keys=[  "AIzaSyAAbyrs8ofXHbyVDZV-u7DpH9c9IVAOok0",
        "AIzaSyB2NcRfFR2NwggTtobJpEOnY9YoEM9byZM",
        "AIzaSyDE_ihZTZB-3V29zzl9VqdEV945ZtaUMEQ",
        "AIzaSyBOoIbMV06l1-Vn10acksO54OCE2gmrjNE",
        "AIzaSyDw4U6z7GOqZLncFKUIaLj789ZxumPINkc",
        "AIzaSyAHegHlR1UfY6R-imJr1faqDxGM0YL-sBY",
        "AIzaSyBZvJhBF1MZn579tGdpta50HCl2CW374_U",
        "AIzaSyDUxDpxv1crwr4h3ZF9f7MCEV4kbPBMOCY",
        "AIzaSyDIuWfiFyyQ2TEihNVtnjqM39h7DoDPF3M",
        "AIzaSyDGIUHpM-KvnD1Xpa7m60KhxoJpEA1Iejk",
        "AIzaSyBedbS79J8txSToZqtelgaVyhY4mV9_7Bo",
        "AIzaSyBHiE5t86GKVX-YuKrV-09flVtZ1R1s6mA",
        "AIzaSyAV4W2ILFEl_4pkCZqAtjbK72I3Gp1m0Cc",
        "AIzaSyDMHv0urqfb2mKOMaUS5WNEdb4Oy5ZEYj8",
        "AIzaSyDQKbA4-SgwChoW7o-eWyPCNZ4YXG9RiI4",
        "AIzaSyAJiPQIjjRkB3Q5WEAg6FgHZANastW9KKA",
        "AIzaSyACrpudPvAJRNdj5ivQvG-J3RCikudfgpU",
        "AIzaSyCy97QAOAgYVfZ9Ow-jA5NK7Htx3d4ccF0",
        "AIzaSyD17YtJy2QvWPLYux58kGTvui88fmkqGdk",
        "AIzaSyCk2wFTWETQ1S7seIi2EpLiBx1ca441np0",
        "AIzaSyBhFtmV1-g9VjAYAiBqUjK345E9DDjS9GU",
        "AIzaSyAKowKJtGAwfXB2jyyDVwPPEfb6h7pf38w",
        "AIzaSyAsaTykyKSl5RJU-VblfzbWZV91xBsU3LY",
        "AIzaSyDKx06vBwIV9xEyJ8f4jtzF9paYrobo2LQ",
        "AIzaSyCJWDycPhHWdNa-Aq4szg-qCUG9duvYCQM",
        "AIzaSyBldusMn6DgCytnfT7qOOSkQCN3v0Vhx4Y",
        "AIzaSyBrJDpvtSIy3QuOy_8z0bMmMMLpHd00aRg",
        "AIzaSyBzIjt_wqzV1eerCxs8MxIe7OFQZUi450o",
        "AIzaSyCTcH5_7gtbJj0H5dUaVlU_s6GVYAFK2C0",
        "AIzaSyBtJUkwwoxy358XDULHrhQ3P1y5byB09bk",
        "AIzaSyAMBkTSh_pAExcZAdw8YkRrLCrufL6CoeQ",
        "AIzaSyAEc4oyEhv6DRzqoTjR4L1I364FXoOf8lM",
        "AIzaSyCpaoS2su4DL0olktnyijJ_4xjAEF56CNE",
        "AIzaSyBZkyYbqhjXFw3AQ3dy5XTGuQ47juXUHUY",
        "AIzaSyCjgXwsY1YI-Q20x0_SKu3ExjRgnRvgjio",
        "AIzaSyAjFS4riCr8nwOMpund3jFwWbnSXidFd5s",
        "AIzaSyB8knEJrV_iSDnWUMwPJQa2QM2Pm2jAhIw",
        "AIzaSyD-gVbpxr8LWSiIHjDuTT-wlFARSC9KZ2w"]

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

#def sentiment_analysis(emailid):
source=pd.read_csv("source.csv",header=None,encoding="utf-8")

columns=["videoid", "total","positive", "neutral", "negative"]
sentiment_fin=pd.DataFrame(columns=columns)

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
    #                    if item.get("snippet").get("topLevelComment").get("snippet").get("authorDisplayName"):
    #                        authorDisplayName.append(item.get("snippet").get("topLevelComment").get("snippet").get("authorDisplayName"))
    #                    else:
    #                        authorDisplayName.append("N/A")
    #                    if item.get("snippet").get("topLevelComment").get("snippet").get("textDisplay"):
    #                        textDisplay.append(item.get("snippet").get("topLevelComment").get("snippet").get("textDisplay"))
    #                    else:
    #                        authorDisplayName.append("N/A")
    #                    if item.get("snippet").get("topLevelComment").get("snippet").get("publishedAt"):
    #                        publishedAt.append(item.get("snippet").get("topLevelComment").get("snippet").get("publishedAt"))
    #                    else:
    #                        authorDisplayName.append("N/A")
    #                    if item.get("snippet").get("topLevelComment").get("snippet").get("authorChannelId"):
    #                        authorChannelId.append(item.get("snippet").get("topLevelComment").get("snippet").get("authorChannelId").get("value"))
    #                    else:
    #                        authorDisplayName.append("N/A")
    #                    if item.get("snippet").get("topLevelComment").get("snippet").get("videoId"):
    #                        videoId.append(item.get("snippet").get("topLevelComment").get("snippet").get("videoId"))
    #                    else:
    #                        authorDisplayName.append("N/A")         
    

        end=time.time()
        elapsed=end-start
        elapsed_fin+=elapsed
        
        print elapsed,elapsed_fin,len(comment_fin)
        
#len(videoId)
#len(authorDisplayName)
#len(publishedAt)
#len(authorChannelId)
#
#nest=[authorDisplayName,textDisplay,publishedAt,authorChannelId]
#
#comments=pd.DataFrame((_ for _ in itertools.zip_longest(nest)), columns=["authorDisplayName","textDisplay","publishedAt","authorChannelId"])
#comments=pd.DataFrame(data={'value':nest},index=["authorDisplayName","textDisplay","publishedAt","authorChannelId"]).value.apply(pd.Series).T
#comments=pd.DataFrame({"authorDisplayName":authorDisplayName,"textDisplay":textDisplay,"publishedAt":publishedAt,"authorChannelId":authorChannelId,"videoId":videoId})
comment_fin.to_csv('Comments.csv', sep="\t", encoding="utf-8")