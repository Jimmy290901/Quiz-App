from django.urls import path
from .views import addMCQ, attempt, addTextual, listQuizzes, pastQuizzes, liveQuizzes, upQuizzes, showQuestions, createQuiz

urlpatterns = [
    path('',listQuizzes),
    path('past',pastQuizzes),
    path('live',liveQuizzes),
    path('upcoming',upQuizzes),
    path('<int:quiz_id>/questions',showQuestions),
    path('create', createQuiz),
    path('<int:quiz_id>/addMCQ', addMCQ),
    path('<int:quiz_id>/addTextual', addTextual),
    path('<int:quiz_id>/attempt', attempt),
]
