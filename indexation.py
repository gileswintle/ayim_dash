import pandasdmx as pdm
import pandas as pd
import plotly.express as px
from time_series_utils import rebase_ind

pd.set_option("display.max_rows", None)
pd.set_option("display.max_columns", None)
pd.set_option("display.width", None)
pd.set_option("display.max_colwidth", -1)


def get_indices():
    insee = pdm.Request("INSEE")
    request = insee.data(resource_id="ILC-ILAT-ICC")
    request2 = insee.data(resource_id="CPI")

    df_inds = request.to_pandas()
    df_cpi = request2.to_pandas()

    df_inds = df_inds.reset_index()
    df_cpi = df_cpi.reset_index()

    # set number of record to longest for ILAT
    records = len(
        df_inds[(df_inds["INDICATEUR"] == "ILAT") & (df_inds["NATURE"] == "INDICE")][
            "value"
        ].to_list()
    )

    df = pd.DataFrame()
    ind = df_inds[df_inds["INDICATEUR"] == "ICC"]["TIME_PERIOD"][-records:]
    df.index = pd.to_datetime(ind) + pd.offsets.QuarterEnd(0)
    df["ICC"] = df_inds[
        (df_inds["INDICATEUR"] == "ICC") & (df_inds["NATURE"] == "INDICE")
    ]["value"][-records:].to_list()
    df["ILC"] = df_inds[
        (df_inds["INDICATEUR"] == "ILC") & (df_inds["NATURE"] == "INDICE")
    ]["value"][-records:].to_list()
    df["ILAT"] = df_inds[
        (df_inds["INDICATEUR"] == "ILAT") & (df_inds["NATURE"] == "INDICE")
    ]["value"][-records:].to_list()

    # cpi df
    df_c = pd.DataFrame()
    ind = df_cpi["TIME_PERIOD"]
    df_c.index = pd.to_datetime(ind)
    df_c["CPI"] = df_cpi["value"].to_list()

    # find matching last value
    last_val = df.index[-1]
    last_val_cpi = df_c.index[-1]
    for i in df_c.index[::-1]:
        if last_val < last_val_cpi and last_val > i:
            last_val_cpi = i
            break
        else:
            last_val_cpi = i

    cpi = df_c.loc[:last_val_cpi, "CPI"].to_list()
    df["CPI"] = cpi[-records:]

    df = rebase_ind(df, col_nos=[0, 1, 2, 3], replace_cols=True)

    return df


def index_chart():
    df = get_indices()
    fig = px.line(df, render_mode="svg")
    fig.update_layout(
        title="French indexation",
        xaxis_title="",
        yaxis_title="",
        legend_title="",
        yaxis_tickformat=",.0f",
    )

    return fig


if __name__ =="__main__":
	print(get_indices())