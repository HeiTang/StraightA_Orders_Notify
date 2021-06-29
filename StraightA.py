#!/usr/bin/python
# -*- coding: UTF-8 -*-
import requests,os,sys
import json
from bs4 import BeautifulSoup
import hashlib
from email.mime.multipart import MIMEMultipart     # 傳送多個部分
from email.mime.text import MIMEText               # 傳送文字
from email.mime.application import MIMEApplication # 傳送附件
import smtplib
import datetime
import time
import schedule

def Crawler(f):
    header = {
        'Connection': 'application/json; charset=utf-8',
        'Accept':'application/json, text/plain, */*',
        'Accept-Encoding':'gzip, deflate, br',
        'Accept-Language':'zh-TW,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:91.0) Gecko/20100101 Firefox/91.0',
        'DNT': '1',
        'Host' : 'www.straighta.com.tw',
        'Cookie' : 'XSRF-TOKEN=LV70dAFweOjzrjCkGikYWkUMA7iojxQWh3ncZiK7A0nxGQM8TmxAlUOaBeQZU5nGAny+lQfxaKbbhET/k3MpqA==; _shop_shopline_session_id_v3=' + Session_id + '; _spt=7a60a216-f266-4d27-9d99-20d92242b5b8',
    }

    # Crawler 訂單資訊、顧客資訊、送貨資訊、付款資訊
    r = requests.get("https://www.straighta.com.tw/orders/" + Order_Url,  headers = header)
    soup = BeautifulSoup(r.text, "html.parser")
    panel = soup.find_all("div",class_="panel-body")[1]
    row = panel.find_all("div", class_="order-detail-section")
    for i in range(len(row)):
        h4 = row[i].find("h4").text
        print("\n+ ",h4, file=f)
        span = row[i].find_all("span")
        for i in range(0,len(span),2):
            title = span[i].text
            result = span[i+1].text.strip()
            if(title == "送貨方式簡介:" or title == "付款指示:" ): 
                continue
            print(title, result, file=f)

    # Crawler 賣家和顧客訂單通訊
    print("\n+ ", panel.find("div", class_="col-sm-12").find("h4").text, file=f)
    r = requests.get("https://www.straighta.com.tw//api/orders/" + Order_Url + "/comments",  headers = header)
    data = json.loads(r.text)
    for i in range(len(data['data']['items'])-1, -1, -1):
        Name = data['data']['items'][i]['performer']['name']
        Date = data['data']['items'][i]['created_at']
        Text = data['data']['items'][i]['html_text']
        try:
            Media = data['data']['items'][i]['media']['images']['source']['url']
        except:
            Media = ''
            pass

        print('>>> ' + Date, file=f)
        print('| ' + Name + '：', file=f)
        if(Text != ''):
            print('| ' + str(Text), file=f)
        if(Media != ''): 
            print('| ' + str(Media), file=f)


def MD5(File_Path):
    f = open(File_Path, 'rb')
    m = hashlib.md5()
    m.update(f.read())
    f.close()
    return m.hexdigest()

def File_Write(File_Path):
    f = open(File_Path, 'w')
    Crawler(f)
    f.close()  

def Mail(file):
    content = MIMEMultipart()                      # 建立 MIMEMultipart 物件
    content["subject"] = "Straight A Notice"       # 郵件標題
    content["from"] = "Notice@gmail.com"           # 寄件者
    content["to"] = Mail_to                        # 收件者
    content.attach(MIMEText("Straight A Notice"))  # 郵件內容
    content.attach(MIMEApplication(open(file,'rb').read()))

    with smtplib.SMTP(host="smtp.gmail.com", port="587") as smtp:     # 設定 SMTP 伺服器
        try:
            smtp.ehlo()                                               # 驗證 SMTP 伺服器
            smtp.starttls()                                           # 建立加密傳輸
            smtp.login(Mail_Sender_Email, Mail_Sender_EmailPassword)  # 登入寄件者 Gmail
            smtp.send_message(content)                                # 寄送郵件
            print("> Complete!")
        except Exception as e:
            print("> Error Message: ", e)

def doMain():
    File_Write(File_Path2)
    MD5_Initial = MD5(File_Path1)
    MD5_Update = MD5(File_Path2)

    if(MD5_Initial == MD5_Update):
        print( datetime.datetime.now()," | 校驗結果一致，檔案無更新(",MD5_Update,")")
    else:
        # 覆寫 StraightA_Initial.txt，使其和 StraightA_Update.txt 一致。
        print("> StraightA_Initial 更新中...")
        File_Write(File_Path1)
        MD5_Initial = MD5(File_Path1)
        print("> StraightA_Initial (MD5) 為 ", MD5_Initial)
        Mail(File_Path2)


if __name__ == '__main__':
    os.system("clear")
    
    ## Settings ##
    File_Path1 = "StraightA_Initial.txt"              # 初始檔案路徑
    File_Path2 = "StraightA_Update.txt"               # 更新檔案路徑
    Order_Url = "{XXXXXXXXXXXX}"                      # Straight A 訂單連結 (https://www.straighta.com.tw/orders/XXXXXXXXXXXX)
    Session_id = "{YYYYYYYYYYYY}"                     # Straight A Session id (_shop_shopline_session_id_v3=YYYYYYYYYYYY)
    Mail_to = "{ReceiverEmail@gmail.com}"             # 收件者 Mail
    Mail_Sender_Email = "{senderEmail@gmail.com}"     # 寄件者 Mail 
    Mail_Sender_EmailPassword = "{senderPassword}"    # 寄件者 Password
    schedule.every(1).hours.do(doMain)                # 週期執行 (https://schedule.readthedocs.io)
    ## Settings ##

    ## Check StraightA_Initial.txt 
    if os.path.isfile(File_Path1):
        pass
    else:
        print("> StraightA_Initial 新增中...")
        File_Write(File_Path1)
    print("> StraightA_Initial (MD5) 為 ", MD5(File_Path1))
    doMain()
    
    ## Periodic Update
    while True:
        schedule.run_pending()
        time.sleep(1) 