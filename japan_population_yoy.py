import pandas as pd
import os
import io
import difflib

files = [
    'japan_population_data_0003459019.csv',
    'japan_population_data_0003448229.csv',
    'japan_population_data_0004008041.csv'
]

def data_clean(files, file_path, output_filename, output_file_path):
    columns_to_drop = [
            'tab_code', '表章項目', 'cat01_code', '男女別', 'cat02_code', '人口', 
            'cat03_code', '年齢5歳階級', 'area_code', '全国', 'time_code', 
            '時間軸（月）', 'unit', 'annotation'
        ]
    dataframes = []

    for file in files:
        full_file_path = os.path.join(file_path, file)  
        df = pd.read_csv(full_file_path) 
        # 月份<>12的排除
        df['time_code'] = df['time_code'].astype(str)
        if '2023' not in df['time_code'].str[:4].values:
            df = df[(df['time_code'].str[6:8] == '12')]
        else:
            df = df[(df['time_code'].str[6:8] == '10')]

        # 人口<>総人口排除
        df = df[df['人口'] == '総人口']

        # 男女別<>男女計排除
        df = df[df['男女別'] == '男女計']

        df = df[df['年齢5歳階級'] == '総数']

        df['value'] = df['value'] * 1000

        df['value'] = df['value'].astype(int)

        df['year'] = df['time_code'].str[:4].astype(int)
        # 排除year小於2014的
        df = df[df['year'] >= 2014]
        print(df)

        #重新排序
        columns_order = ['year'] + [col for col in df.columns if col != 'year']
        df = df[columns_order]

        
        df = df.drop(columns=columns_to_drop, errors='ignore')

        # 將處理後的數據框添加到dataframes列表中
        dataframes.append(df)
    
    # 將所有的數據框合併成一個
    combined_df = pd.concat(dataframes, ignore_index=True)
    combined_df = combined_df.sort_values(by='year')

    # 將合併後的數據框保存到指定的文件路徑
    output_path = os.path.join(output_file_path, output_filename)
    combined_df.to_csv(output_path, index=False, encoding='utf-8-sig')
    print(f"Data saved to {output_path}")
    

    

files = [
    'japan_population_data_0003459019.csv',
    'japan_population_data_0003448229.csv',
    'japan_population_data_0004008041.csv'
]


data_clean(files,'/Users/pochaowang/Documents/Portfolio/Japanese Passport Data/data', 'japan_population_yoy.csv', '/Users/pochaowang/Documents/Portfolio/Japanese Passport Data')













