import glob
from typing import List
import matplotlib.pylab as plt
import pandas as pd


def make_country_plot(path:str, country: str):

    df = process_covid_data(path)
    df = df.loc[df['Country_Region'] == country, :]

    fig, ax = plt.subplots(figsize=(18,8))
    df.plot(x='Last_Update', y='Daily_Deaths', lw = 3, alpha = 0.6, ax=ax)
    df.plot(x='Last_Update', y='Rolling_Daily_Deaths', lw = 3, alpha = 0.6, ax=ax)
    plt.ylabel('Daily deaths')
    plt.savefig("./data/daily_deaths.png", dpi=150)

    fig, ax2 = plt.subplots(figsize=(18,8))
    df.plot(x='Last_Update', y='Daily_Confirmed', lw = 3, alpha = 0.6, ax=ax2)
    df.plot(x='Last_Update', y='Rolling_Daily_Confirmed', lw = 3, alpha = 0.6, ax=ax2)
    plt.ylabel('Daily confirmed cases')
    plt.savefig("./data/daily_confirmed_cases.png", dpi=150)

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
    make_country_plot("./data/COVID-19/csse_covid_19_data/csse_covid_19_daily_reports", 'Brazil')