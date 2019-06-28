import pandas as pd
import numpy as np



def dfcleaner(df):
    cols=list(df.columns)
    df1 = df.dropna(axis=0, subset=[cols[2]])
    df1[cols[2]] = df1[cols[2]].apply(np.int64)
    df1[cols[4]].fillna(" ", inplace=True)
    df1[cols[3]].fillna(" ", inplace=True)
    df2 = df1[df1['YEAR'] > 1999]
    df3 = df2[df2['YEAR'] < 2019]

    return df3


