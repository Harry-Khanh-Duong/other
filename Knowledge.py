# -*- coding: utf-8 -*-
"""
Created on Fri Apr 22 15:58:24 2022

@author: DUONG QUOC KHANH
"""

# df.iterrows() structure (Series): 
    col_1    value   
    col_2    value

# Update row in df:
    for index, row in df.iterrows():
        df.loc[index, "Types"] = "success"

# Solution
check = df.loc[df['Product_name'] == 'Bàn Làm Việc LOFTER']

dict_types = {'Bed Normal': ['', '', ''],
              'Sofa': ['', ''],
              'Bedside': ['', '']}

# Change column orders
lst = df4.columns.tolist()

# Change column name
df.rename(columns={"old name":"new name"})

#  create dict having tupled keys
dict_trial = ref_df.groupby("Baya").Moho.apply(list).to_dict() 
df.set_index('ID').T.to_dict('list')

# array stored as string to list
from ast import literal_eval
baya["Product_description"] = baya["Product_description"].apply(literal_eval)

# Remove duplicates from lists
lst_drop_dup = list(dict.fromkeys(df[col].to_list()))

# Getting date
import datetime as dt
df['Ngày đặt hàng'] = pd.to_datetime(df['Ngày đặt hàng']).dt.date
df = df[(df['Ngày đặt hàng'] >= dt.date(2021,2,1))]

# turning groupby series into df
freq = df2.groupby(["Ngày đặt hàng"])["Số điện thoại"].value_counts().reset_index(name='count') 
 
#%%
 

 

def fix_types(r):
    temp = r['COL1']
    for key, value in dict_types.items():
        for i in value:
            if i in temp:
                return key
            continue 
    return 'Decoration'

# df['Types'] = df.apply(fix_types, axis = 1)



# ?
df3 = pd.DataFrame([pd.Series(x) for x in df1.Info]) # CỘT MATERIALS CHỨA LIST
df3.columns = ['Info_{}'.format(x+1) for x in df3.columns]

df1 = df1.join(df3)

lst = ['Info_1', 'Info_2', 'Info_3', 'Info_4']
for i in lst:
    df1[i] = df1[i].astype(str)

lst = ['Info_1', 'Info_2', 'Info_3', 'Info_4']
for i in lst:
    df1[i] = df1[i].str.replace(',', '')
def add_price(r):
    lst = [r['Info_1'], r['Info_2'], r['Info_3'], r['Info_4']]
    for i in lst:
        if 'triệu/m²' in i:
            return i
        continue
df1['Apartment_Price'] = df1.apply(add_price, axis = 1)
    
def add_project_acreage(r):
    lst = [r['Info_1'], r['Info_2'], r['Info_3'], r['Info_4']]
    for i in lst:
        if 'triệu/m²' not in i:
            if 'ha' in i or 'm²' in i:
                return i
            continue
df1['Project_acreage'] = df1.apply(add_project_acreage, axis = 1)

def add_Apartment_Quantity(r):
    lst = [r['Info_1'], r['Info_2'], r['Info_3'], r['Info_4']]
    for i in lst:
        try:
            if float(i) >= 100:
                return i
            continue
        except:
            None
df1['Apartment Quantity'] = df1.apply(add_Apartment_Quantity, axis = 1)

def add_building_qty(r):
    lst = [r['Info_1'], r['Info_2'], r['Info_3'], r['Info_4']]
    for i in lst:
        try:
            if float(i) < 100:
                return i
            continue
        except:
            None
df1['Building Quantity'] = df1.apply(add_building_qty, axis = 1)

def district_ouliers(df, col, lst): 
    for index, row in df.iterrows():
        for i in col[::-1]:
            if str(row[i]) == 'nan':
                continue
            for j in lst:
                if fuzz.WRatio(j, row[i]) >= 86:
                    df.loc[index, "Quận/Huyện"] = j
                    df.loc[index, i] = np.nan
            break
    return df 
            
df6 = df4.loc[~df4["Quận/Huyện"].isna()]
for k in city:
    temp = df4.loc[(df4["Quận/Huyện"].isna())&(df4["Tỉnh/Thành"] == k)]
    lst = df2.loc[df2["NAME_1"] == k, "NAME_2"].unique().tolist()
    temp = district_ouliers(temp, col, lst)
    df6 = df6.append(temp)

for i in range(2012, 2016):
    print("\nYear {}".format(i))
    ### 30/4 holidays
    print(df.loc[(df["Week"] <= dt.date(i,5,8))&(df["Week"] >= dt.date(i,4,24))])
    ### 2/9 holidays
    print(df.loc[(df["Week"] <= dt.date(i,9,9))&(df["Week"] >= dt.date(i,8,26))])
    ### New Year Eve
    print(df.loc[(df["Week"] <= dt.date(i+1,1,8))&(df["Week"] >= dt.date(i,12,25))])

for i in range(2016, 2023):
    print(i ,dt.date(i, 9, 2).isoweekday())

merge = merge.iloc[~merge.index.isin(lst)]

# Loss by splitting

# First orders will appear first
# x% <= 8113 (USD) (Done)
#temp = merge.groupby(["Ngày đặt hàng_x", "Số điện thoại_x"])["Chiết khấu theo hạng thành viên (%)"].mean().sort_values()
#lst = merge.drop_duplicates(subset=["Ngày đặt hàng_x", "Số điện thoại_x"], keep='last').index.tolist()
# Remove first orders in a day of each person because these are acceptable loss  
#merge = merge.iloc[~merge.index.isin(lst)]
#print("LOSS",(merge["Số tiền giảm"].sum() + merge["Số tiền chiết khấu cho khách hàng thân thiết"].sum())/20000)


#total_guests = df5.groupby("year")["month"].value_counts().reset_index(name="Total visitors").sort_values(["year", "month"])
