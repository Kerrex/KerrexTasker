from django.conf.urls import url, include

from taskbackend.views import AuthView, ProjectsView

urlpatterns = [
    url(r'auth', AuthView.as_view()),
    url(r'projects', ProjectsView.as_view({'get': 'list'})),
]