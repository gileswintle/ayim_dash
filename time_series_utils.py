import pandas as pd
import numpy as np
import datetime


def rebase_ind(df, col_nos=[0], replace_cols=False):  # make t=0 = 100 for a value series or index
    # df.dropna(inplace=True)
    col_names = df.columns
    for cn, name in zip(col_nos, col_names):
        new_nme = f"{name}_rebased" if not replace_cols else name
        df[new_nme] = df.iloc[:, cn] * 100 / df.iloc[0, cn]
    return df


def create_ind(df, col_nos=[0], inplace=True, divisor=100):  # create index from rates
    df.dropna(inplace=True)
    for col_no in col_nos:
        ind_arr = np.zeros(len(df.index))
        ind_arr[0] = 100
        for r, _ in enumerate(df.index[1:], start=1):
            per = (df.index[r] - df.index[r - 1]) / pd.Timedelta(1, "D")
            ind_arr[r] = ind_arr[r - 1] * (1 + (df.iloc[r, col_no] / divisor)) ** (
                per / 365
            )
        if inplace:
            df[df.columns[col_no]] = ind_arr
        else:
            i_col_name = f"{df.columns[col_no]}_Index"
            df[i_col_name] = ind_arr
    return df


def to_day_ind(df, start=False, end=False):
    if start == False:
        start = df.index[0]
    if end == False:
        end = datetime.datetime.now()
    elif end == "last":
        end = df.index[-1]
    ind = pd.date_range(start, end)
    ind = pd.DatetimeIndex(ind)
    df = df.reindex(ind)
    df.interpolate(inplace=True)
    return df


