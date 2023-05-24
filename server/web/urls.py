from django.urls import path
from . import views

urlpatterns = [
    path("", views.homepage, name="homepage", kwargs={"league_id": 39}),
    path("<str:league_id>", views.homepage, name="homepage-league"),
    path("standings/<int:league_id>", views.standings, name="standings"),
    path("predict/", views.predict, name="predict"),
    path("predict/<int:fixture_id>", views.predict_fixture, name="predict-fixture"),
    path("news/", views.news_list, name="news_list"),
    path("news/<int:pk>", views.news_detail, name="news_detail"),
    path("players/<int:league_id>", views.players, name="players"),
    path("policy/", views.policy, name="policy"),
]
