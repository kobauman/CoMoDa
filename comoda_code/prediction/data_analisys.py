import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


filename = '../data/input/LDOS-CoMoDa.xls'

df = pd.read_excel(filename, 'Sheet1', index_col=None, na_values=['NA'])


def meanData(df_dict):
    features = ['rating','age','sex','city','country','time',
            'daytype','season','location','weather','social',
            'endEmo','dominantEmo','mood','physical','decision',
            'interaction']
    result_df = pd.DataFrame(index = features)
    for df_name in df_dict:
        s = df_dict[df_name].loc[:,features].mean()
        result_df[df_name] = s
        
    print result_df


df_dict = dict()
df_dict['df'] = df
df_dict['df_male'] = df[df.sex == 1]
df_dict['df_female'] = df[df.sex == 2]
df_dict['df_old_female'] = df[df.sex == 2][df.age > 25]
df_dict['df_yang_male'] = df[df.sex == 1][df.age < 25]

meanData(df_dict)



#print df.describe()
