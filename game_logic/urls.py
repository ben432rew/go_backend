from django.conf.urls import url, patterns

from game_logic import views


urlpatterns = patterns(
    '',
    url(r'^/v1/new/$', views.NewGameView.as_view()),
    url(r'^/v1/move/$', views.NewMoveView.as_view()),
)
