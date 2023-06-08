from django.shortcuts import render, get_object_or_404
import requests
import json
import os
from web.models import News
from datetime import datetime, timedelta

RapidAPI_Key = "890e7119aamsh564b05f8bc48a80p1aa915jsn6c1e8035d087"
# RapidAPI_Key
# 10390e0b6emsh1ed8839eaea9d6ap13dc42jsn0cd0d981d20b
# 890e7119aamsh564b05f8bc48a80p1aa915jsn6c1e8035d087
# 3447632fb2msh27c9a035d5686f2p14352fjsnb45025d241c2
# 023dd78b62msh8af8ac27cad9a22p1fa4e6jsne3cc4ab352a9
# d588852505mshc605681e18ef5a2p1e1595jsnc9e8d5c89413
# 2e761ceebfmshfa7f126f0846910p127709jsn68b5181f44a8


def homepage(request, league_id):
    try:
        league_id = int(league_id)
    except ValueError:
        league_id = 39
    today = datetime.now().strftime("%Y-%m-%d")
    end_date = (datetime.now() + timedelta(days=7)).strftime("%Y-%m-%d")
    season = "2022"
    standings_url = f"https://api-football-beta.p.rapidapi.com/standings?season={season}&league={league_id}"
    topscorers_url = f"https://api-football-beta.p.rapidapi.com/players/topscorers?season={season}&league={league_id}"
    fixtures_url = (
        f"https://api-football-beta.p.rapidapi.com/fixtures?live=all&season={season}"
    )
    upComings_url = f"https://api-football-beta.p.rapidapi.com/fixtures?season={season}&league={league_id}&from={today}&to={end_date}&timezone=Asia/Ho_Chi_Minh"

    headers = {"X-RapidAPI-Key": RapidAPI_Key}

    standings_response = requests.get(standings_url, headers=headers)
    topscorers_response = requests.get(topscorers_url, headers=headers)
    fixtures_response = requests.get(fixtures_url, headers=headers)
    upComings_response = requests.get(upComings_url, headers=headers)

    standings_data = standings_response.json()
    topscorers_data = topscorers_response.json()
    fixtures_data = fixtures_response.json()
    upComings_data = upComings_response.json()

    if standings_data and standings_data.get("response"):
        standings = standings_data["response"][0]["league"]["standings"][0]
    else:
        standings = None

    if topscorers_data and topscorers_data.get("response"):
        topscorers = topscorers_data["response"]
    else:
        topscorers = []

    if fixtures_data and fixtures_data.get("response"):
        fixtures = fixtures_data["response"]
    else:
        fixtures = []

    if upComings_data and upComings_data.get("response"):
        upComings = upComings_data["response"]
    else:
        upComings = []

    news_list = News.objects.all()

    context = {
        "standings": standings,
        "topscorers": topscorers,
        "fixtures": fixtures,
        "upComings": upComings,
        "selected_league": league_id,
        "news_list": news_list,
    }

    return render(request, "web/homepage.html", context)


def standings(request, league_id="39"):
    season = "2022"
    url = f"https://api-football-beta.p.rapidapi.com/standings?season={season}&league={league_id}"
    headers = {
        "X-RapidAPI-Key": RapidAPI_Key,
        "X-RapidAPI-Host": "api-football-beta.p.rapidapi.com",
    }
    response = requests.get(url, headers=headers)
    standings_data = response.json()
    if standings_data and standings_data.get("response"):
        standings = standings_data["response"][0]["league"]["standings"][0]
    else:
        standings = None
    context = {"standings": standings, "selected_league": league_id}
    return render(request, "web/standings.html", context)


def predict(request):
    exportMetaDataFilePath = (
        os.path.abspath(os.path.dirname(__name__)) + "/../exportedModels/metaData.json"
    )

    exportMetaData = {
        "home_teams": {},
        "away_teams": {},
    }
    if os.path.isfile(exportMetaDataFilePath):
        with open(exportMetaDataFilePath, "r") as f:
            exportMetaData = json.load(f)

    context = {
        "home_teams": exportMetaData["home_teams"],
        "away_teams": exportMetaData["away_teams"],
    }
    return render(request, "web/predict.html", context)


def predict_fixture(request, fixture_id):
    url = "https://api-football-beta.p.rapidapi.com/fixtures"
    querystring = {"id": fixture_id}
    headers = {"X-RapidAPI-Key": RapidAPI_Key}
    response = requests.get(url, headers=headers, params=querystring)
    fixture_data = response.json()["response"][0]

    exportMetaDataFilePath = (
        os.path.abspath(os.path.dirname(__name__)) + "/../exportedModels/metaData.json"
    )

    exportMetaData = {
        "home_teams": {},
        "away_teams": {},
    }
    if os.path.isfile(exportMetaDataFilePath):
        with open(exportMetaDataFilePath, "r") as f:
            exportMetaData = json.load(f)

    context = {
        "home_teams": exportMetaData["home_teams"],
        "away_teams": exportMetaData["away_teams"],
        "home_teams_selected": fixture_data["teams"]["home"]["name"],
        "away_teams_selected": fixture_data["teams"]["away"]["name"],
        "home_goals": fixture_data["goals"]["home"],
        "away_goals": fixture_data["goals"]["away"],
    }

    return render(request, "web/predict.html", context)


def players(request, league_id):
    url = "https://api-football-beta.p.rapidapi.com/players"
    querystring = {"season": "2022", "league": league_id}
    headers = {"X-RapidAPI-Key": RapidAPI_Key}
    response = requests.get(url, headers=headers, params=querystring)
    players_data = response.json()["response"]
    context = {"players_data": players_data}
    return render(request, "web/players.html", context)


def news_list(request):
    news_list = News.objects.all()
    context = {"news_list": news_list}
    return render(request, "web/news_list.html", context)


def news_detail(request, pk):
    news = get_object_or_404(News, pk=pk)
    context = {"news": news}
    return render(request, "web/news_detail.html", context)


def policy(request):
    return render(request, "web/policy.html")
