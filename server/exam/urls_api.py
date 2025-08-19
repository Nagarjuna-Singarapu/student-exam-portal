from django.urls import path
from .views import (
    api_start_exam,
    api_submit_exam,
    api_get_result,
    api_get_all_questions,
)

urlpatterns = [
    path("start/", api_start_exam, name="api_start_exam"),
    path("<int:attempt_id>/submit/", api_submit_exam, name="api_submit_exam"),
    path("<int:attempt_id>/result/", api_get_result, name="api_get_result"),
    path("questions/", api_get_all_questions, name="api_get_all_questions"),
]
