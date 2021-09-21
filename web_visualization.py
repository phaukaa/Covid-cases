import pandas as pd
import altair as alt
from datetime import datetime
from flask import Flask, render_template, request


def plot_reported_cases(county=None, startDate=None, endDate=None):
    """
    Method for plotting reported Covid-19 cases in Norway
    optional param1: county (string), the county for which you want to display stats of reported cases. Default is the whole coutry
    optional param2: startDate (string on format: YYYY-MM-DD), the date you want to start showing stats from. Default is frsom the first reported case on 2020-02-21
    optional param2: endDate (string on format: YYYY-MM-DD), the date you want to end your graph. Default is as far as the stats go
    """
    if county:
        df = pd.read_csv(f"covid_cases/antall-meldte-covid-19-{county}.csv", sep=";", parse_dates=["Dato"], dayfirst=True)
    else:
        df = pd.read_csv("covid_cases/antall-meldte-covid-19-alle.csv", sep=";", parse_dates=["Dato"], dayfirst=True)

    if startDate:
        df = df[df['Dato'].dt.date > pd.to_datetime(startDate)]
    if endDate:
        df = df[df['Dato'] < pd.to_datetime(endDate)]
    
    chart = alt.Chart(df).mark_bar().encode(
        x='Dato', 
        y='Nye tilfeller',
        tooltip=['Nye tilfeller', 'Dato']
    ).interactive().properties(
        title="Rapportert antall smittede"
    )

    return chart
    

def plot_cumulative_cases(county=None, startDate=None, endDate=None):
    """
    Method for plotting cumulative Covid-19 cases in Norway
    optional param1: county (string), the county for which you want to display stats of reported cases. Default is the whole coutry
    optional param2: startDate (string on format: YYYY-MM-DD), the date you want to start showing stats from. Default is frsom the first reported case on 2020-02-21
    optional param2: endDate (string on format: YYYY-MM-DD), the date you want to end your graph. Default is as far as the stats go
    """
    if county:
        df = pd.read_csv(
            f"covid_cases/antall-meldte-covid-19-{county}.csv", sep=";", parse_dates=["Dato"], dayfirst=True)
    else:
        df = pd.read_csv("covid_cases/antall-meldte-covid-19-alle.csv",
                         sep=";", parse_dates=["Dato"], dayfirst=True)

    if startDate:
        df = df[df['Dato'].dt.date > pd.to_datetime(startDate)]
    if endDate:
        df = df[df['Dato'] < pd.to_datetime(endDate)]

    chart = alt.Chart(df).mark_line(stroke='#57A44C').encode(
        x='Dato',
        y='Kumulativt antall',
        tooltip=['Kumulativt antall', 'Dato']
    ).interactive().properties(
        title="Kumulativt antall smittede"
    )
    return chart


def plot_both(county=None, startDate=None, endDate=None):
    """
    Method for plotting both reported and cumulative Covid-19 cases in Norway
    optional param1: county (string), the county for which you want to display stats of reported cases. Default is the whole coutry
    optional param2: startDate (string on format: YYYY-MM-DD), the date you want to start showing stats from. Default is frsom the first reported case on 2020-02-21
    optional param2: endDate (string on format: YYYY-MM-DD), the date you want to end your graph. Default is as far as the stats go
    """
    reported = plot_reported_cases(county, startDate, endDate)
    cumulative = plot_cumulative_cases(county, startDate, endDate)
    chart = alt.layer(reported, cumulative).resolve_scale(y='independent').properties(
        title="Rapportert antall smittede vs. Kumulativt antall smittede"
    )

    return chart


counties = {
    'Alle fylker': 'alle',
    'Agder': 'agder',
    'Innlandet': 'innlandet',
    'Møre og Romsdal': 'moreogromsdal',
    'Nordland': 'nordland',
    'Oslo': 'oslo',
    'Rogaland': 'rogaland',
    'Troms og Finnmark': 'tromsogfinnmark',
    'Trøndelag': 'trondelag',
    'Vestfold og Telemark': 'vestfoldogtelemark',
    'Vestland': 'vestland',
    'Viken': 'viken'
}

app = Flask(__name__)
@app.route("/", methods=["GET", "POST"])
def root():

    bar = plot_reported_cases().to_json()
    line = plot_cumulative_cases().to_json()
    both = plot_both().to_json()

    return render_template('index.html', counties=counties, bar=bar, line=line, both=both, county="Alle fylker", start="2020-02-21", end="2020-11-09")

@app.route("/inputs", methods=["POST"])
def inputs():

    county = request.form["county"]
    startDate = request.form["startDate"]
    endDate = request.form["endDate"]

    if not startDate:
        startDate = "2020-02-21"
    if not endDate:
        endDate = "2020-11-09"

    bar = plot_reported_cases(county=county, startDate=startDate, endDate=endDate).to_json()
    line = plot_cumulative_cases(county=county, startDate=startDate, endDate=endDate).to_json()
    both = plot_both(county=county, startDate=startDate, endDate=endDate).to_json()

    curCounty = "Alle fylker"

    for key, value in counties.items():
        if value == county:
            curCounty = key

    return render_template('index.html', counties=counties, bar=bar, line=line, both=both, county=curCounty, start=startDate, end=endDate)


if __name__=="__main__":
    app.run(debug=True)
