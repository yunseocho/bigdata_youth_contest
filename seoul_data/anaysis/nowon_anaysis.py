import pandas as pd
import matplotlib.pyplot as plt
import geopandas as gpd
import numpy as np
import os 
from datetime import datetime
#import fiona
import pyogrio
import shapefile
#import gdal

folder_path = './seoul_data/seoul_lifestyle_data'

def process_file(file_path):

    df = pd.read_excel(file_path)
    nowon_df = df[df["자치구"]=="노원구"]

    young_nowon_df = nowon_df[nowon_df["연령대"].isin([20,25,30])]
    young_nowon_df = young_nowon_df[["행정동코드", "자치구", "행정동", "성별", "연령대", "총인구수", "1인가구수", "배달 서비스 사용일수", "배달 서비스 사용 미추정 인구수","데이터 사용량"]]
    

    new_df = young_nowon_df.rename(columns={"행정동코드": "adr_code", "자치구":"gu", "행정동": "dong", "성별":"gender", "연령대":"age", "총인구수":"total_pop", "1인가구수":"single_pop",
                                        "배달 서비스 사용일수": "deliver_days", "배달 서비스 사용 미추정 인구수":"deliver_not_esti", "데이터 사용량":"data_usage"})

    column_names = list(new_df.columns)
    dong_group = new_df.groupby('adr_code')[["total_pop", "single_pop", "deliver_days"]].agg({'total_pop': 'sum',
                                                                                            'single_pop': 'sum',
                                                                                            'deliver_days': 'mean'
                                                                                            }).reset_index()
    
    single_pop_ratio =  (dong_group["single_pop"]/dong_group["total_pop"])*100
    dong_group["single_pop_ratio"] = single_pop_ratio
    dong_single_total = np.sum(dong_group["single_pop"])
    
    return dong_group, dong_single_total

    #single_pop_ratio_avg= np.average(single_pop_ratio)
    #twenties = new_df[new_df["age"].isin([20,25])]
    #thirties = new_df[new_df["age"].isin([30])]  

    #np.average(twenties["deliver_days"])
    #np.average(thirties["deliver_days"])
    #np.average(twenties["single_pop_ratio"])


    #deliver_avg = np.average(new_df["deliver_days"])  #13일 
    #data_usage_avg = np.average(new_df["data_usage"]) # 16GB 

    #print(deliver_avg, data_usage_avg)
    #print(new_df["age"].dtype)
    #print(new_df.head(10))
    #print(young_nowon_df.columns)
    #print(np.sum(dong_group["single_pop"]))
    #pd.set_option('display.max_rows', None)  

####################################################################
dong_group_list = []
dong_single_total_list = []

for file_name in sorted(os.listdir(folder_path)):
    if file_name.endswith('.xlsx'):
        file_path = os.path.join(folder_path, file_name)
        
        
        file_base_name = file_name.split('.')[0]
        print(file_base_name)
        year = file_base_name[:4]
        month = file_base_name[4:6]
        file_date = datetime.strptime(f'{year}-{month}', '%Y-%m').strftime('%Y-%m')
        print(f'{file_path} and file date {file_date}')
        dong_group_df, dong_single_total_df = process_file(file_path)
        
        dong_group_df["file_date"] = file_date
        dong_group_list.append(dong_group_df)
        dong_single_total_list.append(dong_single_total_df)

combined_dong_group = pd.concat(dong_group_list)
output_file_path = "/Users/ranking/Desktop/seoul_data/combined_dong_group.xlsx"
combined_dong_group.to_excel(output_file_path, index=True)

print(combined_dong_group)


july_2024 = process_file('./seoul_data/seoul_lifestyle_data/202407.xlsx')
print(july_2024)
###########################################################################
combined_dong_group.columns
wal_1dong=  combined_dong_group[combined_dong_group["adr_code"]==1111051]
wal_2dong =  combined_dong_group[combined_dong_group["adr_code"]==1111052]
wal_3dong = combined_dong_group[combined_dong_group["adr_code"]==1111053] 

gong_2dong = combined_dong_group[combined_dong_group["adr_code"]==1111056] 

hagae_1dong = combined_dong_group[combined_dong_group["adr_code"]==1111058] 
hagae_2dong = combined_dong_group[combined_dong_group["adr_code"]==1111059] 
jungae_bondong = combined_dong_group[combined_dong_group["adr_code"]==1111060] 
jungae_1dong = combined_dong_group[combined_dong_group["adr_code"]==1111061] 
jungae_4dong = combined_dong_group[combined_dong_group["adr_code"]==1111064] 


sangae_1dong = combined_dong_group[combined_dong_group["adr_code"]==1111065] 
sangae_2dong = combined_dong_group[combined_dong_group["adr_code"]==1111066] 
sangae_5dong = combined_dong_group[combined_dong_group["adr_code"]==1111069] 
sangae_8dong = combined_dong_group[combined_dong_group["adr_code"]==1111072] 
sangae_9dong = combined_dong_group[combined_dong_group["adr_code"]==1111073] 
sangae_10dong = combined_dong_group[combined_dong_group["adr_code"]==1111074] 
sangae_34dong = combined_dong_group[combined_dong_group["adr_code"]==1111076] 
sangae_67dong = combined_dong_group[combined_dong_group["adr_code"]==1111077] 
jungae_23dong = combined_dong_group[combined_dong_group["adr_code"]==1111078] 
gong_1dong = combined_dong_group[combined_dong_group["adr_code"]==1111079] 

print(wal_1dong)
print(wal_2dong)

##########################################################################
wal_1dong['file_date'] = pd.to_datetime(wal_1dong['file_date'])
wal_2dong['file_date'] = pd.to_datetime(wal_2dong['file_date'])
wal_3dong['file_date'] = pd.to_datetime(wal_3dong['file_date'])

gong_2dong['file_date'] = pd.to_datetime(gong_2dong['file_date'])
gong_1dong['file_date'] = pd.to_datetime(gong_1dong['file_date'])
                                         
hagae_1dong['file_date'] = pd.to_datetime(hagae_1dong['file_date'])
hagae_2dong['file_date'] = pd.to_datetime(hagae_2dong['file_date'])
wal_3dong['file_date'] = pd.to_datetime(wal_3dong['file_date'])
wal_3dong['file_date'] = pd.to_datetime(wal_3dong['file_date'])



plt.figure(figsize=(12, 8))
plt.plot(wal_1dong['file_date'], wal_1dong['deliver_days'], marker='o', linestyle='-', label='wal_1dong')
plt.plot(gong_2dong['file_date'], gong_2dong['deliver_days'], marker='s', linestyle='--', label='gong_2dong')
plt.plot(gong_1dong['file_date'], gong_1dong['deliver_days'], marker='s', linestyle='--', label='gong_1dong')

plt.xlabel('File Date')
plt.ylabel('Delivery Days')
plt.title('Delivery Days over Time for Different adr_code')

plt.legend()
plt.grid(True)
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()

##########################################################################

gdf = gpd.read_file("/Users/ranking/Desktop/seoul_data/img/seoul_adr.shp", engine='pyogrio')


filter_gdf = gdf[gdf['adm_cd'].isin(["1111051","1111052","1111053","1111056", "1111058", "1111059", "1111060",
                                    "1111061","1111064", "1111065","1111066", "1111069", "1111072", "1111073"
                                     "1111074", "1111076", "1111077", "1111078", "1111079"]
                                    )]


filter_gdf["temp"].split(" ")
filter_gdf.plot()
print(gdf.columns) # adm_nm, adm_cd, adm_cd2, sgg, sido, sidom, temp, sggnm, geometry
print(filter_gdf["adm_cd"].unique())
print(filter_gdf.head(20))
plt.show()




#####################


plt.rcParams['font.family'] = 'Nanum Gothic'  # Replace with the name of the installed font


# Assume 'temp' is the column with the text you want to split
filter_gdf['temp_split'] = filter_gdf['temp'].apply(lambda x: x.split(" "))

# Plot the GeoDataFrame
fig, ax = plt.subplots(figsize=(10, 10))
filter_gdf.plot(ax=ax, color='lightblue', edgecolor='black')

# Annotate the plot with split text
for idx, row in filter_gdf.iterrows():
    # Example: Plot the first element of the split text
    text = row['temp_split'][1] if len(row['temp_split']) > 1 else ''
    ax.text(row.geometry.centroid.x, row.geometry.centroid.y, text,
            fontsize=8, ha='center', color='black')

plt.show()
