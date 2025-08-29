from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, QuizListView, QuizDetailView, TakeQuizView

router = DefaultRouter()
router.register(r'admin/quizzes', QuizViewSet)
router.register(r'admin/questions', QuestionViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('quizzes/<int:pk>/attempt/', TakeQuizView.as_view(), name='take-quiz'),
   
]
