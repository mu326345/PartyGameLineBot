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
    CreateRichMenuAliasRequest,
    Emoji,
    ImageMessage,
    ImagemapBaseSize,
    ImagemapMessage,
    MessageAction,
    MessagingApi,
    MessagingApiBlob,
    ReplyMessageRequest,
    RichMenuArea,
    RichMenuBounds,
    RichMenuRequest,
    RichMenuSize,
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
    # push_message_request = PushMessageRequest(to='',messages=[TextMessage(text='你可以開始了')])
    # line_bot_api.push_message(push_message_request)
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
                        thumbnailImageUrl=get_funny_image(),
                        imageAspectRatio='rectangle',
                        imageSize='contain',
                        title='派對遊戲',
                        text='請選擇遊戲項目',
                        imageBackgroundColor='#FFFFFF',
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
            fruit_topic = get_topic_game()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text=fruit_topic)]
                )
            )
        elif msg == "比手畫腳":
            body_topic = get_body_game()
            line_bot_api.reply_message(
                ReplyMessageRequest(
                    replyToken=event.reply_token,
                    messages=[TextMessage(text=body_topic)]
                )
            )


def get_funny_image():
    imgs = [
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1688146935606.jpg',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1679856272453.jpg',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1672581521294.jpg',
        'https://megapx-assets.dcard.tw/images/0cb79dda-a5c1-4b62-b3ae-8f78e044c986/1280.jpeg',
        'https://img.kuku9.com/uploadimg/image/20190815/1565840862759.jpg',
        'https://img.youjidi.net/uploadimg/image/20190826/20190826145207_59540.jpg',
        'https://img.qq241.com/uploads/images/20201229/20201229162115_62884.jpg',
        'https://memeprod.sgp1.digitaloceanspaces.com/user-wtf/1611334408361.jpg'
    ]
    img = random.choice(imgs)
    return img
            
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
    fruit_topics = [
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
        "男演員", "男歌手", "男藝人", "女演員", "女歌手", "女藝人", "偶像團體", "化妝品牌", "化妝品項",
        # 歷史與文學
        "歷史朝代", "文學作家", "歷史人物", "科學家", "元素週期表",
        # 18+（注意：這個部分的主題可能不適合所有使用情境）
        "AV女優", "汽車旅館", "飯店名稱",
        # 休閒
        "遊樂園",
        # 地理
        "山脈名稱", "地理古蹟",
    ]
    topic = random.choice(fruit_topics)
    return topic

def get_body_game():
    body_topics = [
        # 成語類型
        "雨後春筍", "放下屠刀，立地成佛", "畫蛇添足", "一石二鳥", "豁然開朗", 
        "百發百中", "杞人憂天", "掩耳盜鈴", "忍俊不禁", "揠苗助長", 
        "發揮牛刀小試", "物極必反", "亡羊補牢", "唇亡齒寒", "借刀殺人", 
        "如魚得水", "狐假虎威", "守株待兔", "雞犬不寧", "東風化雨", 
        "背水一戰", "虎頭蛇尾", "獨木難支", "自相矛盾", "坐井觀天", 
        "紙上談兵", "井底之蛙", "東窗事發", "喜上眉梢", "前人種樹，後人乘涼",
        "放馬後炮", "畫蛇添足", "投桃報李", "打草驚蛇", "鶴立雞群", 
        "狼狽為奸", "一石二鳥", "烏合之眾", "螳螂捕蟬", "順手牽羊", 
        "節外生枝", "亡羊補牢", "開門見山", "雞飛狗跳", "掩耳盜鈴", 
        "螳螂拒轍", "倒果為因", "井底之蛙", "獨木難支", "杞人憂天",
        # 歌曲類
        "黃金時間","紅豆","小幸運","青花瓷","告白氣球","演員","平凡之路","大城小愛","歲月神偷","最初的夢想","約定","大海","心太軟","遠走高飛",
        "愛情轉移","擱淺","遙遠的她","春夏秋冬","以後別做朋友","晴天","星晴","飄移","遺憾","她說","不再猶豫","不能说的秘密","夢一場","遙遠的她",
        "親愛的","逆光","無與倫比的美麗","突然好想你","說好的幸福呢","月亮代表我的心","成全","小幸運","明明就","聽見下雨的聲音","橙色年華",
        "我的愛","愛情懸崖","溫柔","等你下課","穿越","不痛","日不落","月光","心電心","告白氣球","花田錯","雨愛","下雨天","布拉格廣場","愛在西元前",
        # 生活類
        "刷牙", "洗澡", "煮泡麵", "打噴嚏", "收拾房間", "吃早餐", "開冰箱", "摺衣服", "買菜", "刮鬍子",
        "拖地", "打電話", "聽音樂", "看電視", "整理書桌", "做運動", "寫日記", "擦窗戶", "打掃庭院", "購物",
        "穿鞋子", "按鈴鈴", "收郵件", "擠牙膏", "看報紙", "做家庭作業", "買午餐", "切水果", "打休閒遊戲", "擦桌子",
        "看時鐘", "玩寵物", "寫信", "整理收納櫃", "洗碗", "舉重", "刷馬桶", "看手錶", "遛狗", "梳頭髮",
        "喝水", "打字", "關窗戶", "吸塵", "看電影", "修理東西", "搭公車", "看雲朵", "吹風", "倒垃圾",
    ]
    topic = random.choice(body_topics)
    return topic
            

#主程式 
if __name__ == "__main__":
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)