import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import matplotlib.colors as mcolors
import os 
from datetime import datetime




folder_path = './seoul_data/seoul_lifestyle_data'

def process_file(file_path):

    df = pd.read_excel(file_path)
    nowon_df = df[df["자치구"]=="노원구"]

    young_nowon_df = nowon_df[nowon_df["연령대"].isin([20,25,30])] 
    not_young_nowon_df = nowon_df[nowon_df["연령대"].isin([35,40,45,50,55,60,65,70,75])]
    
    young_nowon_df = young_nowon_df[["행정동코드", "자치구", "행정동", "성별", "연령대", "총인구수", "1인가구수", "배달 서비스 사용일수", "배달 서비스 사용 미추정 인구수","데이터 사용량"]]
    not_young_nowon_df = not_young_nowon_df[["행정동코드", "자치구", "행정동", "성별", "연령대", "총인구수", "1인가구수", "배달 서비스 사용일수", "배달 서비스 사용 미추정 인구수","데이터 사용량"]]
    total_nowon_df = nowon_df[["행정동코드", "자치구", "행정동", "성별", "연령대", "총인구수", "1인가구수", "배달 서비스 사용일수", "배달 서비스 사용 미추정 인구수","데이터 사용량"]]

    new_df = young_nowon_df.rename(columns={"행정동코드": "adr_code", "자치구":"gu", "행정동": "dong", "성별":"gender", "연령대":"age", "총인구수":"total_pop", "1인가구수":"single_pop",
                                        "배달 서비스 사용일수": "deliver_days", "배달 서비스 사용 미추정 인구수":"deliver_not_esti", "데이터 사용량":"data_usage"})
    new_df2 = not_young_nowon_df.rename(columns={"행정동코드": "adr_code", "자치구":"gu", "행정동": "dong", "성별":"gender", "연령대":"age", "총인구수":"total_pop", "1인가구수":"single_pop",
                                        "배달 서비스 사용일수": "deliver_days", "배달 서비스 사용 미추정 인구수":"deliver_not_esti", "데이터 사용량":"data_usage"})
    new_df3 = total_nowon_df.rename(columns={"행정동코드": "adr_code", "자치구":"gu", "행정동": "dong", "성별":"gender", "연령대":"age", "총인구수":"total_pop", "1인가구수":"single_pop",
                                        "배달 서비스 사용일수": "deliver_days", "배달 서비스 사용 미추정 인구수":"deliver_not_esti", "데이터 사용량":"data_usage"})


    column_names = list(new_df.columns)
    young_group = new_df.groupby('adr_code')[["total_pop", "single_pop", "deliver_days"]].agg({'total_pop': 'sum',
                                                                                            'single_pop': 'sum',
                                                                                            'deliver_days': 'mean'
                                                                                            }).reset_index()
    not_young_group2 = new_df2.groupby('adr_code')[["total_pop", "single_pop", "deliver_days"]].agg({'total_pop': 'sum',
                                                                                            'single_pop': 'sum',
                                                                                            'deliver_days': 'mean'
                                                                                            }).reset_index()
    total_group3 = new_df3.groupby('adr_code')[["total_pop", "single_pop", "deliver_days"]].agg({'total_pop': 'sum',
                                                                                            'single_pop': 'sum',
                                                                                            'deliver_days': 'mean'
                                                                                            }).reset_index()
    total_group_age = new_df3.groupby(['adr_code','age'])[["total_pop", "single_pop", "deliver_days"]].agg({'total_pop': 'sum',
                                                                                            'single_pop': 'sum',
                                                                                            'deliver_days': 'mean'
                                                                                            }).reset_index()

    
    return young_group, not_young_group2, total_group3, total_group_age

###########################################################################

young_group, not_young_group, total_group, total_group_age = process_file('/Users/ranking/Desktop/seoul_data/seoul_lifestyle_data/202407.xlsx')
young_df = pd.DataFrame(young_group, columns=['adr_code', 'total_pop','single_pop', "deliver_days"])
not_young_df = pd.DataFrame(not_young_group, columns=['adr_code', 'total_pop','single_pop', "deliver_days"])
total_group_df = pd.DataFrame(total_group, columns=['adr_code', 'total_pop','single_pop', "deliver_days"])
total_group_age_df = pd.DataFrame(total_group_age, columns=['adr_code', 'total_pop','single_pop', "deliver_days"])

total_group_df['total_pop'] = np.round(total_group_df['total_pop'],0).astype(int)
young_df['total_pop'] = np.round(young_df['total_pop'],0).astype(int)
young_pop_ratio =  (young_df["total_pop"]/total_group_df["total_pop"])*100

pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)
print(total_group_age_df)

#print(young_df)
#print(not_young_df)
print(young_df)
print(np.average(young_pop_ratio))
print(np.sum(total_group['total_pop']))


print(np.average(young_df['deliver_days']), np.average(not_young_df['deliver_days']))


##########################################################################

gdf = gpd.read_file("./seoul_data/img/seoul_adr.shp", engine='pyogrio')


filter_gdf = gdf[gdf['adm_cd'].isin(["1111051","1111052","1111053","1111056", "1111058", "1111059", "1111060",
                                    "1111061","1111064", "1111065","1111066", "1111069", "1111072", "1111073",
                                     "1111074", "1111076", "1111077", "1111078", "1111079"]
                                    )]

filter_gdf.plot()
print(gdf.columns) # adm_nm, adm_cd, adm_cd2, sgg, sido, sidom, temp, sggnm, geometry

filter_gdf = filter_gdf.rename(columns={"adm_cd": "adr_code"})
print(filter_gdf.head(20))



###########################################
print(total_group_df['adr_code'].dtypes)
print(filter_gdf['adr_code'].dtypes)

filter_gdf['adr_code'] = filter_gdf['adr_code'].astype(int)

merge_gdf = filter_gdf.merge(total_group_df, on='adr_code',  how='inner')
print(merge_gdf["geometry"][0])
print(merge_gdf.columns) # adm_nm', 'adr_code', 'adm_cd2', 'sgg', 'sido', 'sidonm',
                         #'temp', 'sggnm', 'geometry', 'temp_split', 'total_pop', 'single_pop',
                         #'deliver_days', 'single_pop_ratio']
print(merge_gdf)

##########################################
#노원구 그냥 지도 그림, with 전통시장 위치 
longitudes = [127.068541738, 127.077480597] 
latitudes = [37.659896978, 37.622023532]

#한글 글꼴
plt.rcParams['font.family'] = 'Nanum Gothic'  
plt.rcParams['font.weight'] = 'bold'


fig, ax = plt.subplots(figsize=(10, 10))
cax = merge_gdf.plot(ax=ax, color = "bisque", legend= False, edgecolor='black')

#동별 이름 가져오기 
for idx, row in merge_gdf.iterrows():
    text = row['temp_split'][1] if len(row['temp_split']) > 1 else ''
    ax.text(row.geometry.centroid.x, row.geometry.centroid.y, text,fontsize=10, ha='center', color='black')
    
    
ax.scatter(longitudes, latitudes, color='darkorange', marker='o', s=150, label='전통시장')

# 전통시장 위치 추가 
for lon, lat in zip(longitudes, latitudes):
    ax.text(lon, lat, '', fontsize=14, color='darkorange', ha='right', va='bottom')

ax.axis("off")
plt.legend(loc = 'lower right', bbox_to_anchor=(1,0), fontsize=14)
plt.show()

################################################################################
#노원구의 전체 인구 그림3  

original_cmap = plt.get_cmap('Blues')
#colors = ['#deebf7', '#c6dbef', '#9ecae1', '#6baed6', '#4292c6', '#2171b5', '#08519c', '#08306b']
num_colors = 5
colors = [original_cmap(i / (num_colors - 1)) for i in range(num_colors)]
new_cmap = mcolors.LinearSegmentedColormap.from_list('custom_Blues', colors, N=original_cmap.N)
num_intervals = 5
bounds = np.linspace(0, 40000, num_intervals + 1)
norm = mcolors.BoundaryNorm(bounds, new_cmap.N)

#한글 글꼴
plt.rcParams['font.family'] = 'Nanum Gothic'  
plt.rcParams['font.weight'] = 'bold'

#동별 이름 가져오기 
merge_gdf['temp_split'] = merge_gdf['temp'].apply(lambda x: x.split(" "))

#지리적 그림
fig, ax = plt.subplots(figsize=(10, 10))
cax = merge_gdf.plot(column='total_pop',ax=ax, legend= False, norm=norm,
               cmap=new_cmap, edgecolor='black')




for idx, row in merge_gdf.iterrows():
    text = row['temp_split'][1] if len(row['temp_split']) > 1 else ''
    ax.text(row.geometry.centroid.x, row.geometry.centroid.y, text,fontsize=10, ha='center', color='black')
    ax.text(row.geometry.centroid.x , row.geometry.centroid.y - 0.002,  # Slightly below the main text
            f'{row["total_pop"]}', fontsize=7, ha='center', color='blue')


ax.axis("off")

sm = plt.cm.ScalarMappable(cmap=new_cmap, norm=norm)
sm.set_array([]) 
cbar = fig.colorbar(sm, ax=ax, orientation='vertical')
cbar.outline.set_linewidth(2)
cbar.ax.tick_params(width=2)

tick_positions = np.linspace(bounds[0], bounds[-1], num_colors + 1)
cbar.set_ticks(tick_positions)
tick_labels = [f'{int(x)}' for x in tick_positions]
cbar.ax.set_yticklabels(cbar.get_ticks(), fontdict={'fontsize': 12, 'fontweight': 'bold', 'family': 'Nanum Gothic'})
cbar.ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f'{int(x)}'))


plt.title("노원 동별 전체 인구", fontsize=16, fontweight='bold')
plt.show()
