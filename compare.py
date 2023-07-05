# -*- coding: utf-8 -*-
"""
Created on Sat Jan 14 19:24:10 2023

@author: hpche
"""

import pandas as pd
import datetime as dt

# df = pd.read_excel("C:/Users/hpche/Downloads/CG_[BASBB] Cognos.xlsx")
# print(df.value_counts(["Actual Invoice Number"]).sort_values(ascending=False))
# Actual Invoice Number not duplicated
folder = ["C:/Users/hpche/Downloads/LK_Equipment_Spoke dml_cntr_ltst_mvmt 2023-06-30T1108.xlsx",
"C:/Users/hpche/Downloads/CG_New Report (7).xlsx"]

f = open("C:/Users/hpche/OneDrive/Desktop/Testing result.txt", "w")
j = 0
while j < len(folder) - 1:
    string = '\n' + str(folder[j]) + '\n'
    f.write(string)
    if "LK" in folder[j]:
        df_looker = pd.read_excel(folder[j])
        df_cognos = pd.read_excel(folder[j+1])
    else:
        df_looker = pd.read_excel(folder[j+1])
        df_cognos = pd.read_excel(folder[j])
    
    if df_looker.shape[1] != df_cognos.shape[1]:
        df_looker.drop('Unnamed: 0', axis=1, inplace=True)
    # df_cognos.drop('Snapshot Month', axis=1, inplace=True)
    
    if 'Vendor Code' in df_cognos.columns.values:
        cognos_pk = 'Vendor Code'
        looker_pk = 'Vendor Code'
        merge_pk = 'Vendor Code_x'
    else:
        cognos_pk = df_cognos.columns.values[0]
        looker_pk = df_looker.columns.values[0]
        merge_pk = df_cognos.columns.values[0]
        
        # Use for date type dimensions
        # df_cognos[df_cognos.columns.values[0]] = pd.to_datetime(df_cognos[df_cognos.columns.values[0]])
        # df_cognos[df_cognos.columns.values[0]] = df_cognos[df_cognos.columns.values[0]].dt.round('1min')  
        # df_looker[df_looker.columns.values[0]] = pd.to_datetime(df_looker[df_looker.columns.values[0]])
        # df_looker[df_looker.columns.values[0]] = df_looker[df_looker.columns.values[0]].dt.round('1min')  
        
        
        # cognos_pk = df_cognos.columns.values[0]
        # looker_pk = df_looker.columns.values[0]
        # merge_pk = df_cognos.columns.values[0]
        # df_cognos[df_cognos.columns.values[0]] = pd.to_datetime(df_cognos[df_cognos.columns.values[0]], format='%Y%m%d')
        # df_cognos[df_cognos.columns.values[0]] = df_cognos[df_cognos.columns.values[0]].dt.round('1min')  
        # df_looker[df_looker.columns.values[0]] = pd.to_datetime(df_looker[df_looker.columns.values[0]])
        # df_looker[df_looker.columns.values[0]] = df_looker[df_looker.columns.values[0]].dt.round('1min')  
        
    # else:
    #     cognos_pk = df_cognos.columns.values[0]
    #     looker_pk = df_looker.columns.values[0]
    #     merge_pk = cognos_pk
        
    j = j + 2
    # df_cognos['Latest Event Date (Local)'] = pd.to_datetime(df_cognos['Latest Event Date (Local)'])
    # df_cognos['Latest Event Date (Local)'] = df_cognos['Latest Event Date (Local)'].dt.round('1min')  
    
    #%% Does it apprear in Cognos but not in Looker? 
    #print('Does cognos length equal to Looker:',df_looker.shape[0] == df_cognos.shape[0])
    #%% Prepare data
    # print(df_looker.isna().any())
    print(df_looker.columns.values)
    print(df_cognos.columns.values)
    # df_cognos['Disposal Flag'] = df_cognos['Disposal Flag'].replace({'Y':'Yes', 'N':'No'})
    # df_looker['Container Work Order Quantity'] = df_looker['Container Work Order Quantity'].fillna(0) 
    # df_cognos.iloc[:,1:] = df_cognos.iloc[:,1:].fillna(0)
    # df_looker.rename(columns={'cntr_no':'Container Number' ,'STY_DAYS':'Stay Days'},inplace=True)
    #df_looker = df_looker.loc[:,['Equipment Container Number','Dml Cntr Ltst Mvmt Totald Sty Days New']]
    # df_looker = df_looker.rename(columns={' Measures Stay Days':'Stay Days'})
    # df_looker.iloc[:,2:] = df_looker.iloc[:,2:].astype('float')
    # df_cognos.iloc[:,2:] = df_cognos.iloc[:,2:].astype('float')
    # # Temporily exclude Avg, Stay Days due to many errors
    # df_looker = df_looker.drop(['To ETB/ETA Week of Year'], axis=1)
    # df_cognos = df_cognos.drop(['To ETB/ETA Week'], axis=1)
    #df_cognos['Avg Days In Event'] = df_cognos['Avg Days In Event']
    # Round avg value
    # df_looker['Average Stay Days In Event'] = df_looker['Average Stay Days In Event'].round(decimals=5)
    # df_cognos['Avg Days In Event'] = df_cognos['Avg Days In Event'].round(decimals=5)
    
    
    #%% Find any discrepancies
    df1 = df_cognos
    df2 = df_looker
    
    
    lst2 = df_cognos.columns.to_list()
    for i in lst2:
        df1.loc[:, i] = df1[i].astype(str)

    df1.loc[:,'test'] = df1[lst2].apply("-".join, axis=1)

    lst = df_looker.columns.to_list()
    for i in lst:
        df2.loc[:, i] = df2[i].astype(str)

    df2.loc[:,'test'] = df2[lst].apply("-".join, axis=1)

    result3 = pd.merge(df1, df2, on='test', how='outer', indicator=True)

    dict_match = {'both': 'Matched', 'left_only': 'Only_Cognos', 'right_only': 'Only_Looker'}
    result3['_merge'] = result3['_merge'].map(dict_match)

    data_only_looker = result3.loc[lambda v: v['_merge'] == 'Only_Looker']
    data_only_cognos = result3.loc[lambda v: v['_merge'] == 'Only_Cognos']
    data_same = result3.loc[lambda v: v['_merge'] == 'Matched']
    
    index = data_only_cognos[merge_pk].to_list()

    df_looker_diff = df_looker.loc[df_looker[looker_pk].isin(index)]
    df_cognos_diff = df_cognos.loc[df_cognos[cognos_pk].isin(index)]
        
    #%% Locating where the errors come from
    for i in range(len(lst)):
        df_looker_diff.loc[:,'test'] = df_looker_diff.loc[:,[looker_pk, lst[i]]].apply("-".join, axis=1)
        df_cognos_diff.loc[:,'test'] = df_cognos_diff.loc[:,[cognos_pk, lst2[i]]].apply("-".join, axis=1)
        detect = df_cognos_diff.merge(df_looker_diff, on='test', how='outer', indicator=True)    
        if detect.shape[0]!=df_looker_diff.shape[0]:    
            string = 'This is where error is locating: ' + str(detect.shape[0]-df_looker_diff.shape[0]) + '/' + str(df_looker.shape[0]) + ' ' + lst[i] + '\n' 
            f.write(string)
            
f.close()


print(data_only_cognos[data_only_cognos.columns.values[0]].to_list())
