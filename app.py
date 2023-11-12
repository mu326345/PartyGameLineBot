import os
import re
from flask import Flask, request, abort
from linebot.models import MessageTemplateAction, TemplateSendMessage

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
        print(msg)
        line_bot_api.reply_message(
            ReplyMessageRequest(
                replyToken=event.reply_token,
                messages=[TextMessage(text=msg)]
            )
        )

        if msg == '安安':
            print('這裡有成功進入安安')
            select_game_msg = TemplateSendMessage(
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
            print('1test')
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TemplateMessage(
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
                ))]
                )
            )
            # print('2test')
            # line_bot_api.reply_message(event.reply_token,messages=select_game_msg)


#主程式 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))     
    app.run(host='0.0.0.0', port=port)