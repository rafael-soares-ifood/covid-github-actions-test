import glob
from typing import List
import matplotlib.pylab as plt
import pandas as pd
from datetime import date

def make_country_plot(path:str, country: str):

    df = process_covid_data(path)
    df = df.loc[(df['Country_Region'] == country) & (df['Last_Update'] >= date(2020, 3, 26)), :]

    max_rolling_daily_deaths = df["Rolling_Daily_Deaths"].max()
    max_rolling_daily_confirmed = df['Rolling_Daily_Confirmed'].max()


    fig, ax = plt.subplots(figsize=(18,8))
    plt.hlines(y=max_rolling_daily_deaths,
               colors='r', alpha=0.6, lw=3,
	       xmin=df['Last_Update'].min(),
               xmax=df['Last_Update'].max())
    plt.text(df['Last_Update'].min(),
             max_rolling_daily_deaths + 30,
             f"max {int(round(max_rolling_daily_deaths,0))}",
             fontsize=17)

    df.plot(x='Last_Update', y='Daily_Deaths', lw = 3, alpha = 0.6, ax=ax)
    df.plot(x='Last_Update', y='Rolling_Daily_Deaths', lw = 3, alpha = 0.6, ax=ax)
    plt.ylabel('Daily deaths', fontsize=15)
    plt.xlabel("Date", fontsize=15)
    plt.legend(fontsize=19)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)
    plt.tight_layout()
    plt.savefig("/github/workspace/daily_deaths.png", dpi=150)

    fig, ax2 = plt.subplots(figsize=(18,8))
    plt.hlines(y=max_rolling_daily_confirmed,
               colors='r', alpha=0.6, lw=3, 
               xmin=df['Last_Update'].min(), 
               xmax=df['Last_Update'].max())
    plt.text(df['Last_Update'].min(),
             max_rolling_daily_confirmed + 300,
             f"max {int(round(max_rolling_daily_confirmed,0))}",
             fontsize=17)

    df.plot(x='Last_Update', y='Daily_Confirmed', lw = 3, alpha = 0.6, ax=ax2)
    df.plot(x='Last_Update', y='Rolling_Daily_Confirmed', lw = 3, alpha = 0.6, ax=ax2)
    plt.ylabel('Daily confirmed cases', fontsize=15)
    plt.xlabel("Date", fontsize=15)
    plt.legend(fontsize=19)
    ax2.tick_params(axis='both', which='major', labelsize=12)
    ax2.tick_params(axis='both', which='minor', labelsize=10)
    plt.tight_layout()
    plt.savefig("/github/workspace/daily_confirmed_cases.png", dpi=150)

    return None

def process_covid_data(path: str):
    df = _compose_df(path)

    df['Last_Update'] = pd.to_datetime(df['Last_Update']).dt.date
    df = df.groupby(by=['Last_Update', 'Country_Region']).agg('sum').reset_index()
    df = df.loc[:, ['Country_Region', 'Last_Update', 'Active', 'Confirmed', 'Deaths']]
    df = df.sort_values(by=['Country_Region', 'Last_Update'])

    diff = df[['Active', 'Confirmed', 'Deaths']].diff()
    diff.columns = ['Daily_' + i for i in diff.columns]
    df = pd.concat([df, diff], axis='columns')

    for i in ['Daily_Active', 'Daily_Confirmed', 'Daily_Deaths']:
        df['Rolling_' + i] = df[i].rolling(7).mean()

    return df

def _compose_df(path: str):
    files_path = _get_csv_files_path(path)
    return pd.concat([pd.read_csv(f) for f in files_path], ignore_index=True)

def _get_csv_files_path(path: str) -> List[str]:
    return glob.glob(f'{path}/*.csv')

if __name__ == '__main__':
    make_country_plot("/github/workspace/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports", 'Brazil')
