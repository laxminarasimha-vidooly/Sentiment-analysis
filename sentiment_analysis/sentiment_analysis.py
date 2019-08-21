#Importing libraries
import pandas as pd
from lxml import html
import requests
from random import randint
import json
import os
from flask import Flask, request, redirect, url_for, flash
import flask
from werkzeug.utils import secure_filename
from time import sleep
import smtplib 
from email.mime.multipart import MIMEMultipart 
from email.mime.text import MIMEText 
from email.mime.base import MIMEBase 
from email import encoders
import time
import re 
from textblob import TextBlob 
from random import sample 
import datetime


path=os.path.dirname(os.path.abspath(__file__))
os.chdir(path)
 #Key check          
keys=["Keys"]

keys3=[]
#key check
for k in range(len(keys)):
    base_url="https://www.googleapis.com/youtube/v3/channels?part=snippet,statistics&"
    dum_url=base_url+"key="+keys[k]+"&id=UCw9Ponb04uNH2AT5gPZ2z6A"
    responses=requests.get(dum_url)
    if responses.status_code !=403 and responses.status_code !=400:
       keys3.append(keys[k])
    else:
       continue

keys2=keys3[:]

def get_random_api_key(keys2):
    keys2
    random_no = randint(0, len(keys2)-1)
    random_api_key = keys2[random_no]
    return random_api_key,random_no  

#get comments from YouTube
def sentiment_analysis(emailid):
    source=pd.read_csv("source.csv",header=None,encoding="utf-8")
    
    columns=["videoid", "total","positive", "neutral", "negative"]
    sentiment_fin=pd.DataFrame(columns=columns)
    
    base_url = 'https://www.googleapis.com/youtube/v3/commentThreads?'
    base_url1='textFormat=plainText&part=snippet&key='
    base_url2='&maxResults=100&pageToken='
    
    for i in range(len(source)):
        sentiment_temp=pd.DataFrame(index=range(1),columns=columns)
        sentiment_temp=sentiment_temp.fillna("N/A")
        positive=0
        neutral=0
        negative=0
        video_ids=source.iloc[i,0]
        
        token=''
        countr=1
        
        textDisplay1=[]
        
        while token is not None and countr<6:
            while True:
                if len(keys2)!=0:
                    rand_key=get_random_api_key(keys2)
                    url=base_url+base_url1+rand_key[0]+"&videoId="+video_ids+base_url2+token
                    print url,emailid
            
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
                            print responses.status_code,emailid
                            index=rand_key[1]
                            del keys2[index]
    #                            print keys2
                            continue
                else:
                    print "keys are done"
                    break
            
            data = json.loads(resp.text, "utf-8")
            
            token=data.get("nextPageToken")
            if data.get("items"):
                for item in data.get("items"):       
                    textDisplay1.append(item.get("snippet").get("topLevelComment").get("snippet").get("textDisplay").replace("\r"," ").replace("\n"," "))
                    
                countr+=1
                
            else:
                break
            
        print len(textDisplay1)
        
        if len(textDisplay1)>0:
            clean_comments=[]
            for commenttt in textDisplay1:
                clean_text=re.sub('[^A-Za-z0-9 ]+', ' ', commenttt)
                clean_comments.append(clean_text)
    #            print len(clean_comments)
            #Sentiment analysis
            for clean_c in clean_comments:
                analysis = TextBlob(clean_c)
                
                if analysis.sentiment.polarity > 0: 
                    positive+=1
            
                if analysis.sentiment.polarity == 0: 
                    neutral+=1
            
                if analysis.sentiment.polarity < 0:
                    negative+=1
            sentiment_temp.iloc[0,0]=video_ids
            sentiment_temp.iloc[0,1]=positive+neutral+negative
            sentiment_temp.iloc[0,2]=positive
            sentiment_temp.iloc[0,3]=neutral
            sentiment_temp.iloc[0,4]=negative
        else:
            sentiment_temp.iloc[0,0]=video_ids
    
               
        sentiment_fin=sentiment_fin.append(sentiment_temp)
        sentiment_fin.to_csv('sentiment_analysis_temp.csv', index=False)
        print i,sentiment_fin
    
    sentiment_fin.to_csv('sentiment_analysis.csv', index=False)
    who_requested=pd.read_csv(path+"/who_requested.csv")
    who_requested=who_requested.iloc[:,1:2]
    who_requested_temp=pd.DataFrame(index=range(1), columns=['Email','Time'])
    who_requested_temp.iloc[0,0]=str(emailid)
    who_requested_temp.iloc[0,1]=(str(datetime.datetime.now())) 
    who_requested=who_requested.append(who_requested_temp)
    who_requested.to_csv("who_requested.csv",encoding='utf-8')
    mail(emailid,1,body = "Hi\nPFA\n\n\nPlease note the following:\n->Analysis is done on recent 500 comments(not their replies) with no date limitation.\n->It considers only English comments for analysis, other languages will be considered as Neutral.")
#Send email to recipeints
def mail(addr,resp,body):  
    fromaddr = "nilanjan.vidooly@gmail.com"
    msg = MIMEMultipart()
    recipients = 'nilanjan@vidooly.com,laxmi.n@vidooly.com,satya@vidooly.com'+','+addr
    msg['From'] = fromaddr
    msg["To"] = recipients
    if resp==1:
        msg['Subject'] = "sentiment_analysis_"+addr
          
        msg.attach(MIMEText(body, 'plain')) 
          
        filename = "sentiment_analysis_"+addr+".csv"
        attachment = open("sentiment_analysis.csv", "rb") 
        p = MIMEBase('application', 'octet-stream') 
        p.set_payload((attachment).read()) 
        encoders.encode_base64(p) 
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        msg.attach(p)
    else:
        msg['Subject'] = "Error Encountered_"+" "+addr
        msg.attach(MIMEText(body, 'plain')) 
          
        p = MIMEBase('application', 'octet-stream') 
        encoders.encode_base64(p) 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
    s.starttls() 
    s.login(fromaddr, "nilanjan_vidooly.1") 
    text = msg.as_string() 
    s.sendmail(msg["From"], recipients.split(','), text)
    s.quit() 

UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = set(['csv'])
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

#Dashboard creation
@app.route('/RnD/sentiment_analysis', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            sleep(1)
            return redirect(request.url)
        file = request.files['file']
        if file and file.filename=="source.csv":
            emailid = flask.request.form['emailid']
            if len(emailid)!=0 and emailid.split("@")[1]=="vidooly.com":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
                try:
                    sentiment_analysis(emailid)
                except Exception as e:
                    mail(emailid,2,"following error encountered:\n\n"+str(e))
            else:
                return "No/Wrong email id given"
                sleep(1)
                return redirect(request.url)
        else:
            return "wrong file selected"
            sleep(1)
            return redirect(request.url)
            
        
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload File containing VideoIDs For sentiment analysis in csv format</h1>
    <h2>File name should be "source.csv" with no headers<h2>
    <h2>you will get sentiment analysis for upto first 500 comments only in your mail<h2>
    <font color="red">Note: You may close the browser Tab after the page starts loading</font>
    <form method=post enctype=multipart/form-data>
      <p><input type=file name=file>
      <p>Vidooly Email ID <input type ="text" name = "emailid" /></p>
         <input type=submit value=Upload>
    </form>'''
app.run(host='0.0.0.0', port=5001, threaded=True)
sentiment_analysis()
