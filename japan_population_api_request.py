import requests
import pandas as pd
from dotenv import load_dotenv
import os
import io

load_dotenv()

API_KEY = os.getenv('API_KEY')

BASE_URL = "http://api.e-stat.go.jp/rest/3.0/app/getSimpleStatsData"

params = {
    "appId": API_KEY,
    "lang": "J",
    "metaGetFlg": "Y",
    "cntGetFlg": "N",
    "explanationGetFlg": "Y",
    "annotationGetFlg": "Y",
    "sectionHeaderFlg": "1",
    "replaceSpChars": "0",
}

stats_data_ids = ["0004008041", "0003448229", "0003459019"]

for stats_data_id in stats_data_ids:
    params["statsDataId"] = stats_data_id
    
    response = requests.get(BASE_URL, params=params)

    if response.status_code == 200:
        print(f"\n处理 statsDataId: {stats_data_id}")
        print("API返回的前100个字符：")
        print(response.text[:100])  
        
        csv_data = io.StringIO(response.text)
        
        try:
            df = pd.read_csv(csv_data, sep=',')  
        except:
            csv_data.seek(0) 
            try:
                df = pd.read_csv(csv_data, sep='\t')
            except:
                print("无法解析CSV数据，请检查原始数据格式")
                continue
        
        if df.empty:
            print("解析后的数据框为空，请检查原始数据格式")
        else:
            if not os.path.exists('data'):
                os.makedirs('data')
            
            output_file = os.path.join('data', f'japan_population_data_{stats_data_id}.csv')
            df.to_csv(output_file, index=False, encoding='utf-8-sig')
            print(f"CSV文件已保存为：{output_file}")
        
        print("\n解析后的数据预览：")
        print(df.head())  
    else:
        print(f"请求失败，状态码：{response.status_code}")
        print(response.text)