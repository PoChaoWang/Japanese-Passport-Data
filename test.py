import pandas as pd
import os
import glob
import difflib

def find_closest_sheet(excel_file, target_name):
    sheet_names = excel_file.sheet_names
    closest_match = difflib.get_close_matches(target_name, sheet_names, n=1, cutoff=0.6)
    return closest_match[0] if closest_match else None

file_path = 'data/2016.xlsx'
year = os.path.basename(file_path).split('.')[0]
excel_file = pd.ExcelFile(file_path)
target_sheet_name = '一般旅券有効旅券数'
sheet_name = find_closest_sheet(excel_file, target_sheet_name)

# if not sheet_name:
#     print(f"Warning: No matching sheet found in file {file_path}")
#     exit()
print(sheet_name)
df = pd.read_excel(file_path, sheet_name=sheet_name)

df = df.iloc[1:].reset_index(drop=True)
df.columns = ['city', 'na1', 'na2', '5_years', '10_years', 'total']
df = df[df['city'] == '合計']
df = df.drop(columns=['city','na1', 'na2', '5_years', '10_years'])
df.insert(0, 'year', year)

print(df)

# df = df[df['都道府県名'] == '合計']
# df.insert(0, 'year', year)
# print(df)