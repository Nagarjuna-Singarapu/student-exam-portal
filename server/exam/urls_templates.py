from django.urls import path
from .views import register_view, login_view, logout_view, exam_start_view, exam_take_view, exam_result_view, TemplateIndexRedirectView

urlpatterns = [
    path("", TemplateIndexRedirectView, name="index_redirect"),
    path("register/", register_view, name="exam_register"),
    path("login/", login_view, name="exam_login"),
    path("logout/", logout_view, name="exam_logout"),
    path("exam/start/", exam_start_view, name="exam_start"),
    path("exam/<int:attempt_id>/", exam_take_view, name="exam_take"),
    path("exam/<int:attempt_id>/result/", exam_result_view, name="exam_result"),
]
