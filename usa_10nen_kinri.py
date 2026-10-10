import os
from linebot.v3.messaging import Configuration, ApiClient, MessagingApi, PushMessageRequest, TextMessage
import datetime
import pandas_datareader.data as web

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

def usa_10nen():
    # 取得期間の設定（直近30日分）
    end = datetime.datetime.today()
    start = end - datetime.timedelta(days=30)

    try:
        # FREDから米10年国債金利 (ティッカー: DGS10) を取得
        df = web.DataReader('DGS10', 'fred', start, end)

        # 最新のデータを取得
        latest_date = df.index[-1].strftime('%Y-%m-%d')
        latest_rate = df['DGS10'].iloc[-1]

        print(f"--- 米国債10年金利 (FRED) ---")
        print(f"日付: {latest_date}")
        print(f"金利: {latest_rate}%")

        print("\n--- 直近の推移 ---")
        print(df.tail())
        send_line_message(f"{latest_rate}")

    except Exception as e:
        print(f"データの取得に失敗しました: {e}")
        send_line_message(f"データの取得に失敗しました: {e}")

if __name__ == "__main__":
    usa_10nen()
