import os
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
import requests

def send_line_message(message_text):
    """
    LINEにメッセージを送信する関数
    """
    # 環境変数から取得
    channel_access_token = os.environ.get('LINE_CHANNEL_ACCESS_TOKEN')
    user_id = os.environ.get('LINE_USER_ID')

    configuration = Configuration(access_token=channel_access_token)

    with ApiClient(configuration) as api_client:
        line_bot_api = MessagingApi(api_client)
        line_bot_api.push_message(
            PushMessageRequest(
                to=user_id,
                messages=[TextMessage(text=message_text)]
            )
        )
        print("送信成功！")

def get_cnn_fear_and_greed():
    # CNNの非公式APIエンドポイント
    url = "https://production.dataviz.cnn.io/index/fearandgreed/graphdata"
   
    # ブロックされないようにUser-Agentを設定
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
   
    response = requests.get(url, headers=headers)
   
    if response.status_code == 200:
        data = response.json()
       
        # 最新のデータを取得
        fng_data = data.get('fear_and_greed', {})
        score = fng_data.get('score')
        rating = fng_data.get('rating')
       
        print(f"--- 株式市場 (CNN) Fear & Greed Index ---")
        # print(f"指数: {score}")
        print(f"指数: {score:.1f}")
        print(f"判定: {rating}")
        send_line_message(f"{score:.1f}({rating})")
    else:
        print(f"データの取得に失敗しました。ステータスコード: {response.status_code}")
        send_line_message(f"データの取得に失敗しました。ステータスコード: {response.status_code}")

if __name__ == "__main__":
    get_cnn_fear_and_greed()
