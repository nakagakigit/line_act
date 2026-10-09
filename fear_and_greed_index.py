import requests

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
        print(f"指数: {score}")
        print(f"判定: {rating}")
    else:
        print(f"データの取得に失敗しました。ステータスコード: {response.status_code}")

if __name__ == "__main__":
    get_cnn_fear_and_greed()