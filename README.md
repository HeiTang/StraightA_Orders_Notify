# StraightA Orders Notify

Where is my iPad Pro ??? 。･ﾟ･(つд`ﾟ)･ﾟ･

## Features
- Check your order in Straight A's website.
- Email Notify

## How to use ?

1. Install requirement.txt from the project.
    
    ```
    pip3 install -r requirements.txt 
    ```
   
2. Modify StraightA.py.

    ```
    ## Settings ##
    File_Path1 = "StraightA_Initial.txt"              # 初始檔案路徑
    File_Path2 = "StraightA_Update.txt"               # 更新檔案路徑
    Order_Url = "{XXXXXXXXXXXX}"                      # Straight A 訂單連結
    Session_id = "{YYYYYYYYYYYY}"                     # Straight A Session id
    Mail_to = "{ReceiverEmail@gmail.com}"             # 收件者 Mail
    Mail_Sender_Email = "{senderEmail@gmail.com}"     # 寄件者 Mail 
    Mail_Sender_EmailPassword = "{senderPassword}"    # 寄件者 Password
    schedule.every(1).hours.do(doMain)                # 週期執行 (https://schedule.readthedocs.io)
    ## Settings ##
    ```
    - Order_Url：Straight A 訂單連結
      
      ```
      https://www.straighta.com.tw/orders/XXXXXXXXXXXX
      ```
    
    - Session_id：Straight A Session id
      ```
      _shop_shopline_session_id_v3:"YYYYYYYYYYYY"
      ```
      
    - Mail_Sender_EmailPassword：Yourself Password or App Passwords.
      - [Sign in with App Passwords](https://support.google.com/accounts/answer/185833)

    - [schedule](https://schedule.readthedocs.io)：週期執行

3. Final, Run python3.


