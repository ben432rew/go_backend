from django.conf.urls import url, patterns

from game_logic import views


urlpatterns = patterns(
    '',
    url(r'^new/$', views.NewGameView.as_view()),
)
