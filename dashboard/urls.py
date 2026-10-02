from django.contrib.auth.views import LogoutView
from django.urls import path

from .views import (TeacherLoginView, dashboard_home, group_detail, groups_list, home, lesson_create, lesson_edit,lesson_delete,attendance,profile,contact)


urlpatterns = [

    path("", home, name="home"),
    path("login/", TeacherLoginView.as_view(), name="login"),
    path("dashboard/", dashboard_home, name="dashboard_home"),
    path("groups/", groups_list, name="groups"),
    path("groups/<int:group_id>/", group_detail, name="group_detail"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("groups/<int:group_id>/lessons/create/", lesson_create, name="lesson_create"),
    path("lessons/<int:lesson_id>/edit/", lesson_edit, name="lesson_edit"),
    path("lessons/<int:lesson_id>/delete/", lesson_delete, name="lesson_delete"),
    path("lessons/<int:lesson_id>/attendance/", attendance, name="attendance"),
    path("profile/",profile, name="profile"),
    path("contact/",contact, name="contact"),
]