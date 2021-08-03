import matplotlib.pylab as plt
import pandas as pd


def make_campinas_plot(path:str, local: bool = False):

    df = process_covid_data(path)
    df = df.loc[df['date'] > df['date'].min(), :]

    max_rolling_daily_deaths = int(df["obitos_mm7d"].max())
    max_rolling_daily_confirmed = int(df['casos_mm7d'].max())

    plt.style.use('seaborn')
    fig, ax = plt.subplots(figsize=(18,8))
    plt.hlines(y=max_rolling_daily_deaths, colors='g', alpha=0.6, lw=3, xmin=df['date'].min(), xmax=df['date'].max())
    plt.text(df['date'].min(),
             max_rolling_daily_deaths*1.05,
             f"max {int(round(max_rolling_daily_deaths,0))}",
             fontsize=17)

    df.plot(x='date', y='obitos_novos', lw = 4, alpha = 0.6, ax=ax)
    df.plot(x='date', y='obitos_mm7d', lw = 4, alpha = 1.0, ax=ax)
    plt.ylabel('Daily deaths', fontsize=15)
    plt.xlabel("Date", fontsize=15)
    plt.legend(fontsize=19)
    ax.tick_params(axis='both', which='major', labelsize=12)
    ax.tick_params(axis='both', which='minor', labelsize=10)
    plt.title(f'Daily number of deaths for Campinas', fontsize=15)
    plt.tight_layout()
    if local:
        plt.show()
    else:
        plt.savefig(f"/github/workspace/daily_deaths_campinas.png".replace(' ', '_'), dpi=150)

    fig, ax2 = plt.subplots(figsize=(18,8))
    plt.hlines(y=max_rolling_daily_confirmed,
               colors='r', alpha=0.6, lw=3, 
               xmin=df['date'].min(), 
               xmax=df['date'].max())
    plt.text(df['date'].min(),
             max_rolling_daily_confirmed*1.05,
             f"max {int(round(max_rolling_daily_confirmed,0))}",
             fontsize=17)

    df.plot(x='date', y='casos_novos', lw = 4, alpha = 0.6, ax=ax2)
    df.plot(x='date', y='casos_mm7d', lw = 4, alpha = 1.0, ax=ax2)
    plt.ylabel('Daily confirmed cases', fontsize=15)
    plt.xlabel("Date", fontsize=15)
    plt.title(f'Daily number of confirmed cases for Campinas', fontsize=15)
    plt.legend(fontsize=19)
    ax2.tick_params(axis='both', which='major', labelsize=12)
    ax2.tick_params(axis='both', which='minor', labelsize=10)
    plt.tight_layout()
    if local:
        plt.show()
    else:
        plt.savefig(f"/github/workspace/daily_confirmed_cases_campinas.png".replace(' ', '_'), dpi=150)

    return None

def process_covid_data(path: str):
    df = _compose_df(path)

    df = df.loc[df['nome_munic'] == 'Campinas']
    df['date'] = pd.to_datetime(df['datahora']).dt.date
    df = df.sort_values(by=['date'])

    for i in ['casos_novos', 'obitos_novos', 'casos_mm7d', 'obitos_mm7d']:
        df[i] = pd.to_numeric(df[i].astype(str).str.strip().str.replace(',', '.', regex=False))      

    return df

def _compose_df(path: str):
    return pd.read_csv(path, sep=';')
