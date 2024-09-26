import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os 
import pyogrio
import geopandas as gpd


folder_path = './seoul_data/seoul_market_visit_data/'
file_path = './seoul_data/seoul_market_visit_data/S_2024.04.15-04.21.csv'
file_path2 = './seoul_data/seoul_market_visit_data/S_2024.07.15-21.csv'

df = pd.read_csv(file_path2, encoding='euc-kr')
#print(df)
nowon_market_df = df[df["자치구"]=="Nowon-gu"]
#print(nowon_market_df.head(5))
#print(nowon_market_df.columns) #'모델명', '시리얼', '측정시간', '지역', '자치구', '행정동', '방문자수', '등록 일시'


nowon_mar_df = nowon_market_df.rename(columns={"모델명": "model_name", "시리얼":"serial_num", "측정시간": "time", "지역":"location", "자치구":"gu", "행정동":"dong", "방문자수":"visit",
                                        "등록일시": "update_date"})
nowon_mar_df['time'] = pd.to_datetime(nowon_mar_df['time'].str.replace('_', ' '), format='%Y-%m-%d %H:%M:%S', errors='coerce')
grouped_df = nowon_mar_df.groupby(['serial_num', nowon_mar_df['time'].dt.to_period('H')])['visit'].mean().reset_index()
grouped_df['time'] = grouped_df['time'].dt.to_timestamp()

start_time = pd.Timestamp(year=2024, month=1, day=1, hour=10)  # 필터링 시작 시간
end_time = pd.Timestamp(year=2024, month=1, day=1, hour=20) 
filtered_df = grouped_df[(grouped_df['time'].dt.hour >= start_time.hour) & (grouped_df['time'].dt.hour <= end_time.hour)]

filtered_df['date'] = filtered_df['time'].dt.date
mar_date_group = filtered_df.groupby(['serial_num','date'])[["serial_num", "visit"]].agg({'visit': 'sum'}).reset_index()
mar_df = mar_date_group[mar_date_group['serial_num'].isin([3007, 3028])]
print(mar_df)

#pd.set_option('display.max_columns', None)
#pd.set_option('display.max_rows', None)
print(grouped_df) ## 원본에서 데이터 누락 4/16-5/12

#################################################################
# 위 과정 함수로 만들기 

folder_path = './seoul_data/seoul_market_visit_data/'
    
def process_file(file_path): 
    df = pd.read_csv(file_path, encoding='euc-kr')
    nowon_market_df = df[df["자치구"]=="Nowon-gu"]
    nowon_mar_df = nowon_market_df.rename(columns={"모델명": "model_name", "시리얼":"serial_num", "측정시간": "time", "지역":"location", "자치구":"gu", "행정동":"dong", "방문자수":"visit",
                                        "등록일시": "update_date"})
    nowon_mar_df['time'] = pd.to_datetime(nowon_mar_df['time'].str.replace('_', ' '), format='%Y-%m-%d %H:%M:%S', errors='coerce')
    grouped_df = nowon_mar_df.groupby(['serial_num', nowon_mar_df['time'].dt.to_period('H')])['visit'].mean().reset_index()
    grouped_df['time'] = grouped_df['time'].dt.to_timestamp()

    start_time = pd.Timestamp(year=2024, month=1, day=1, hour=10)  # 필터링 시작 시간
    end_time = pd.Timestamp(year=2024, month=1, day=1, hour=20) 
    filtered_df = grouped_df[(grouped_df['time'].dt.hour >= start_time.hour) & (grouped_df['time'].dt.hour <= end_time.hour)]

    filtered_df['date'] = filtered_df['time'].dt.date
    mar_date_group = filtered_df.groupby(['serial_num','date'])[["serial_num", "visit"]].agg({'visit': 'sum'}).reset_index()
    mar_df = mar_date_group[mar_date_group['serial_num'].isin([3007, 3028])]
    return mar_df


##############################################################################
# 유동인구 데이터 합친 파일 만들기 
market_time_list = []

for file_name in sorted(os.listdir(folder_path)):
    if file_name.endswith('.csv'):
        file_path = os.path.join(folder_path, file_name)
        p_market_df = process_file(file_path)
        market_time_list.append(p_market_df)
    

combine_market_group = pd.concat(market_time_list)
combine_market_final = combine_market_group.groupby(['serial_num','date'])[["serial_num", "visit"]].agg({'visit': 'sum'}).reset_index()

print(combine_market_final)


output_file_path = "./seoul_data/anaysis/combined_market_time.csv"
combine_market_final.to_csv(output_file_path, index=True)

##############################################################################
# 전통시장별 유동인구 최대인 5일 추출 

max_visit = np.max(combine_market_final['visit'])


max_visit_row = combine_market_final[combine_market_final['visit'] == max_visit]

print(max_visit_row)


sorted_df = combine_market_final.sort_values(by='visit', ascending=False)

top_10_days_sang = sorted_df[sorted_df["serial_num"]==3028].head(10)
top_10_days_gong = sorted_df[sorted_df["serial_num"]==3007].head(10)
print(top_10_days_sang)
print(top_10_days_gong)


sorted_df2 = combine_market_final.sort_values(by='visit', ascending=True)

min_10_days_sang = sorted_df2[sorted_df2["serial_num"]==3028].head(10)
min_10_days_gong = sorted_df2[sorted_df2["serial_num"]==3007].head(10)

print(min_10_days_sang)
print(min_10_days_gong)


##############################################################################
#전통시장 유동인구 그림 

plt.rcParams['font.family'] = 'Nanum Gothic'
plt.rcParams['font.weight'] = 'bold'

sange_mar =  combine_market_final[combine_market_final["serial_num"]==3028]
gong_mar =  combine_market_final[combine_market_final["serial_num"]==3007]

plt.figure(figsize=(12, 8))
plt.plot(sange_mar['date'], sange_mar['visit'], linestyle='-', label='상계중앙시장', linewidth=3, color='sienna')
plt.plot(gong_mar['date'], gong_mar['visit'], linestyle='-', label='공릉도깨비시장', linewidth=3, color='orange')

plt.xlabel('날짜' ,fontsize=20, fontfamily='Nanum Gothic', fontweight='bold')
plt.ylabel('유동인구', fontsize=20, fontfamily='Nanum Gothic', fontweight='bold')
plt.title('전통시장별 유동인구', fontsize=24, fontfamily='Nanum Gothic', fontweight='bold')

plt.legend(fontsize=20)
plt.grid(True)
plt.xticks(fontsize=16, rotation=45)
plt.yticks(fontsize=16)
plt.tight_layout()
plt.show()
