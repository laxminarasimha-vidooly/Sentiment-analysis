# -*- coding: utf-8 -*-
"""
Created on Wed Feb 06 16:51:39 2019

@author: Administrator
"""

import pandas as pd
#import math
#import urllib2
#from lxml import etree
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
#path=r"C:\Server backup\VIDOOLY NILANJAN\Python\RnD APIs\Py2_Code_for_sentiment_analysis"
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

def sentiment_analysis(emailid):
    source=pd.read_csv("source.csv",header=None,encoding="utf-8")
    
    columns=["videoid", "total","positive", "neutral", "negative"]
    sentiment_fin=pd.DataFrame(columns=columns)
    
    base_url = 'https://www.googleapis.com/youtube/v3/commentThreads?'
    base_url1='textFormat=plainText&part=snippet&key='
    base_url2='&maxResults=100&pageToken='
    
#    authorDisplayName=[]
#    textDisplay=[]
#    publishedAt=[]
#    authorChannelId=[]
#    videoId=[]
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
#                    authorDisplayName.append(item.get("snippet").get("topLevelComment").get("snippet").get("authorDisplayName"))
#                    textDisplay.append(item.get("snippet").get("topLevelComment").get("snippet").get("textDisplay").replace("\r"," ").replace("\n"," "))
#                    publishedAt.append(item.get("snippet").get("topLevelComment").get("snippet").get("publishedAt"))
#                    authorChannelId.append(item.get("snippet").get("topLevelComment").get("snippet").get("authorChannelId").get("value"))
#                    videoId.append(item.get("snippet").get("topLevelComment").get("snippet").get("videoId"))
#                          
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
    
#    comments=pd.DataFrame({"authorDisplayName":authorDisplayName,"textDisplay":textDisplay,"publishedAt":publishedAt,"authorChannelId":authorChannelId,"videoId":videoId})
    sentiment_fin.to_csv('sentiment_analysis.csv', index=False)
#    comments.to_csv('Comments.csv', sep="\t", encoding="utf-8")
    who_requested=pd.read_csv(path+"/who_requested.csv")
    who_requested=who_requested.iloc[:,1:2]
    who_requested_temp=pd.DataFrame(index=range(1), columns=['Email','Time'])
    who_requested_temp.iloc[0,0]=str(emailid)
    who_requested_temp.iloc[0,1]=(str(datetime.datetime.now())) 
    who_requested=who_requested.append(who_requested_temp)
    who_requested.to_csv("who_requested.csv",encoding='utf-8')
    mail(emailid,1,body = "Hi\nPFA\n\n\nPlease note the following:\n->Analysis is done on recent 500 comments(not their replies) with no date limitation.\n->It considers only English comments for analysis, other languages will be considered as Neutral.")
#    except Exception as e:
#        sentiment_analysis=pd.concat(sentiment_analysis)       
#        
#        sentiment_analysis.to_csv('sentiment_analysis_error.csv', index=False, header=True)
#        
def mail(addr,resp,body):  
##    addr="satya@vidooly.com"
    fromaddr = "nilanjan.vidooly@gmail.com"
##    toaddr = "nilanjan@vidooly.com"
#    addr1=['nilanjan@vidooly.com', 'laxmi.n@vidooly.com']
#    toaddr1=",".join(addr1)+","+addr
#    toaddr=toaddr1.split(",")
#    type(toaddr)

    #type(toaddr)
    # instance of MIMEMultipart 
    msg = MIMEMultipart()
    recipients = 'nilanjan@vidooly.com,laxmi.n@vidooly.com,satya@vidooly.com'+','+addr
    #recipients = 'laxmi.n@vidooly.com'
#    recipients = 'nilanjan.vidooly@gmail.com'+','+addr
    # storing the senders email address   
    msg['From'] = fromaddr
    msg["To"] = recipients
      
    # storing the receivers email address  
#    msg['To'] = toaddr 
      
    # storing the subject  
    if resp==1:
        msg['Subject'] = "sentiment_analysis_"+addr
          
        # string to store the body of the mail 
#        body = "Hi\nPFA"
          
        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 
          
        # open the file to be sent  
        filename = "sentiment_analysis_"+addr+".csv"
        attachment = open("sentiment_analysis.csv", "rb") 
          
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
          
        # To change the payload into encoded form 
        p.set_payload((attachment).read()) 
          
        # encode into base64 
        encoders.encode_base64(p) 
           
        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
        
            # attach the instance 'p' to instance 'msg' 
        msg.attach(p)
    
    else:
        msg['Subject'] = "Error Encountered_"+" "+addr
          
        # string to store the body of the mail 
#        body = "Error occured \n Verify the source file"
          
        # attach the body with the msg instance 
        msg.attach(MIMEText(body, 'plain')) 
          
        # open the file to be sent  
#        filename = "Ch_Country_"+addr+".csv"
#        attachment = open("CH_Country.csv", "rb") 
          
        # instance of MIMEBase and named as p 
        p = MIMEBase('application', 'octet-stream') 
          
        # To change the payload into encoded form 
#        p.set_payload((attachment).read()) 
          
        # encode into base64 
        encoders.encode_base64(p) 
           
#        p.add_header('Content-Disposition', "attachment; filename= %s" % filename)
      
 
      
    # creates SMTP session 
    s = smtplib.SMTP('smtp.gmail.com', 587) 
      
    # start TLS for security 
    s.starttls() 
      
    # Authentication 
    s.login(fromaddr, "nilanjan_vidooly.1") 
      
    # Converts the Multipart msg into a string 
    text = msg.as_string() 
      
    # sending the mail 
    s.sendmail(msg["From"], recipients.split(','), text)
#    s.sendmail(fromaddr, toaddr, text) 
      
    # terminating the session 
    s.quit() 

UPLOAD_FOLDER = path
ALLOWED_EXTENSIONS = set(['csv'])
 
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.secret_key = "secret key"

 
@app.route('/RnD/sentiment_analysis', methods=['GET', 'POST'])
def upload_file():
#    def flash_success():
#        flash('uploaded_file\n\nWait for mail')
#        return render_template('Try2.html')
#    emailid = ""
    if request.method == 'POST':
#        emailid = flask.request.values.get('emailid')
        
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            sleep(1)
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit a empty part without filename
#        if file.filename == '' or file.filename != "source.csv":
#            flash('No selected file')
#            sleep(1)
#            return redirect(request.url)
        if file and file.filename=="source.csv":
            emailid = flask.request.form['emailid']
            if len(emailid)!=0 and emailid.split("@")[1]=="vidooly.com":
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    #            flash('uploaded_file '+filename)

                #flash_success()
                
                try:
                    sentiment_analysis(emailid)
                except Exception as e:
                    mail(emailid,2,"following error encountered:\n\n"+str(e))
                    
                    
#                return render_template('Try2.html')
                
    #            mail(emailid)
#                return "Hi "+emailid+"\r\n\r\n Check mail"
            else:
                return "No/Wrong email id given"
                sleep(1)
                return redirect(request.url)
        else:
            return "wrong file selected"
            sleep(1)
            return redirect(request.url)
            
#            return redirect(url_for('uploaded_file',
#                                    filename=filename))
            
        
    
        
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
#app.run(host='0.0.0.0')

sentiment_analysis()