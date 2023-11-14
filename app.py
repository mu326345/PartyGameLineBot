import os
import random
import re
from flask import Flask, request, abort

from linebot.v3 import (
    WebhookHandler
)
from linebot.v3.exceptions import (
    InvalidSignatureError
)
from linebot.v3.messaging import (
    ButtonsTemplate,
    Configuration,
    ApiClient,
    Emoji,
    ImageMessage,
    ImagemapBaseSize,
    ImagemapMessage,
    MessageAction,
    MessagingApi,
    ReplyMessageRequest,
    TemplateMessage,
    TextMessage,
    PushMessageRequest,
)
from linebot.v3.webhooks import (
    MessageEvent,
    TextMessageContent
)

app = Flask(__name__)
#Channel Access Token
configuration = Configuration(access_token='RJkuIv/f5RAlwvxCk49BfsBrO6wlmdRdaLOF+4nORfXeuaHujBERYOIy1fqS6mJRG5n5xHUCcfmwSda2zzIGQgTvrxfyQz0nEeWyZAAdDDwNBlnEc6u+0fPX+xnpylPNNZ20cLPrJ2PUazKw38Vw/gdB04t89/1O/w1cDnyilFU=')
#Channel Secret
handler = WebhookHandler('c6db96275c3c55c24b705b7fda8a7fcd')

# Add for notice start successful
with ApiClient(configuration) as api_client:
    line_bot_api = MessagingApi(api_client)
    #推播訊息給我自己
    push_message_request = PushMessageRequest(to='U581ffde1bc9cb258045fe4d4781b57cc',messages=[TextMessage(text='你可以開始了')])
    line_bot_api.push_message(push_message_request)
# End 

# 監聽所有來自 /callback 的 Post Request
@app.route("/callback", methods=['POST'])
def callback():
    # get X-Line-Signature header value
    signature = request.headers['X-Line-Signature']

    # get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)

    # handle webhook body
    try:
        handler.handle(body, signature)
    except InvalidSignatureError:
        app.logger.info("Invalid signature. Please check your channel access token/channel secret.")
        abort(400)

    return 'OK'


#訊息傳遞區塊 
##### 基本上程式編輯都在這個function ##### 
@handler.add(MessageEvent, message=TextMessageContent)
def handle_message(event):
    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        
        msg = event.message.text
        if msg == '安安':
            star_message = TemplateMessage(
                 alt_text='Buttons template',
                        template=ButtonsTemplate(
                        type='buttons',
                        title='遊戲項目',
                        text='請選擇項目',
                        actions=[
                            MessageAction(
                                label='骰子',
                                text='骰子'
                            ),
                            MessageAction(
                                label='果園菜園動物園',
                                text='果園菜園動物園'
                            ),
                            MessageAction(
                                label='比手畫腳',
                                text='比手畫腳'
                            ),
                        ]
                )
            )
            #回復訊息給用戶
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[star_message]
                )
            )
        elif msg == "骰子":
            dice_result = roll_dice()
            print(dice_result)
            #文字回覆
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text=dice_result)]
                )
            )
        elif msg == "果園菜園動物園":
            topic = get_topic_game()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text=topic)]
                )
            )

            
            
def roll_dice():
    results = []
    for _ in range(6):
        # 骰子結果1~6
        result = random.randint(1, 6)
        results.append(result)
    if set(sorted(results)) == {1,2,3,4,5,6}:
        print('同花順，在骰一次')
        return roll_dice()
    return ', '.join(map(str, sorted(results)))

def get_topic_game():
    topics = [
        # 地方
        "果園", "菜園", "動物園", "職業", "國家", "捷運站", "縣市",
        # 媒體與藝術
        "電影", "書籍",
        # 色彩
        "顏色",
        # 教育
        "大學科系", "大學名稱",
        # 飲食
        "飲料", "飲料店", "食物", "餐廳", "甜點", "垃圾食物", "速食餐廳",
        # 運動
        "運動", "球類運動", "奧運項目",
        # 科技
        "科技產品", "大公司名稱",
        # 娛樂
        "男演員", "男歌手", "男藝人", "女演員", "女歌手", "女藝人", "偶像團體",
        # 歷史與文學
        "歷史朝代", "文學作家", "歷史人物", "科學家",
        # 18+（注意：這個部分的主題可能不適合所有使用情境）
        "AV女優", "汽車旅館", "飯店名稱",
        # 休閒
        "遊樂園",
        # 地理
        "山脈名稱", "地理古蹟",
    ]
    return random.choice[topics]

            

#主程式 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))     
    app.run(host='0.0.0.0', port=port)