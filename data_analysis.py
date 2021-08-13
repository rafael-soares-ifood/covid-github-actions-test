import glob
from typing import List

import matplotlib.pylab as plt
import pandas as pd

from data_analysis_campinas import make_campinas_plot


def make_country_plot(path:str, political_region: str, entity: str, local: bool = False):

    df = process_covid_data(path, political_region)
    df = df.loc[df[political_region] == entity, :]
    df = df.loc[df['Last_Update'] > '2020-04-01', :]

    max_rolling_daily_deaths = df["Rolling_Daily_Deaths"].max()
    max_rolling_daily_confirmed = df['Rolling_Daily_Confirmed'].max()

    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(18,8))
    plt.hlines(y=max_rolling_daily_deaths,
               colors='r', alpha=0.6, lw=4,
	       xmin=df['Last_Update'].min(),
               xmax=df['Last_Update'].max())
    plt.text(df['Last_Update'].min(),
             max_rolling_daily_deaths + 30,
             f"max {int(round(max_rolling_daily_deaths,0))}",
             fontsize=17)

    df.plot(x='Last_Update', y='Daily_Deaths', lw = 4, alpha = 0.6, ax=ax)
    df.plot(x='Last_Update', y='Rolling_Daily_Deaths', lw = 4, alpha = 0.9, ax=ax)
    plt.ylabel('Daily deaths', fontsize=15)
    plt.xlabel("Date", fontsize=15)
    plt.legend(fontsize=19)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)
    plt.title(f'Daily number of deaths for {entity}', fontsize=15)
    plt.tight_layout()
    if local:
        plt.show()
    else:
        plt.savefig(f"/github/workspace/daily_deaths_{entity}.png".replace(' ', '_'), dpi=150)

    fig, ax2 = plt.subplots(figsize=(18,8))
    plt.hlines(y=max_rolling_daily_confirmed,
               colors='r', alpha=0.6, lw=4, 
               xmin=df['Last_Update'].min(), 
               xmax=df['Last_Update'].max())
    plt.text(df['Last_Update'].min(),
             max_rolling_daily_confirmed + 300,
             f"max {int(round(max_rolling_daily_confirmed,0))}",
             fontsize=17)

    df.plot(x='Last_Update', y='Daily_Confirmed', lw = 4, alpha = 0.6, ax=ax2)
    df.plot(x='Last_Update', y='Rolling_Daily_Confirmed', lw = 4, alpha = 0.9, ax=ax2)
    plt.ylabel('Daily confirmed cases', fontsize=15)
    plt.xlabel("Date", fontsize=15)
    plt.title(f'Daily number of confirmed cases for {entity}', fontsize=15)
    plt.legend(fontsize=19)
    ax2.tick_params(axis='both', which='major', labelsize=12)
    ax2.tick_params(axis='both', which='minor', labelsize=10)
    plt.tight_layout()
    if local:
        plt.show()
    else:
        plt.savefig(f"/github/workspace/daily_confirmed_cases_{entity}.png".replace(' ', '_'), dpi=150)

    return None

def process_covid_data(path: str, political_region: str):
    df = _compose_df(path)
    columns = ['Active', 'Confirmed', 'Deaths']

    df['Last_Update'] = pd.to_datetime(df['Last_Update']).dt.date
    df = df.groupby(by=['Last_Update', political_region]).agg('sum').reset_index()
    df = df.loc[:, [political_region, 'Last_Update'] + columns]
    df = df.sort_values(by=[political_region, 'Last_Update'])

    diff = df[columns].diff()
    diff.columns = [f'Daily_{i}' for i in diff.columns]
    df = pd.concat([df, diff], axis='columns')

    for i in columns:
        df[f'Rolling_Daily_{i}'] = df[f'Daily_{i}'].rolling(7).mean()

    return df

def _compose_df(path: str):
    files_path = _get_csv_files_path(path)
    return pd.concat([pd.read_csv(f) for f in files_path], ignore_index=True)

def _get_csv_files_path(path: str) -> List[str]:
    return glob.glob(f'{path}/*.csv')

if __name__ == '__main__':
    make_country_plot("/github/workspace/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports", 'Country_Region', 'Brazil')
    make_country_plot("/github/workspace/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports", 'Province_State', 'Sao Paulo')
    make_campinas_plot('/github/workspace/dados-covid-sp/data/dados_covid_sp.csv')
