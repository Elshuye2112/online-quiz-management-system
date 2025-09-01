from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import QuizViewSet, QuestionViewSet, QuizListView, QuizDetailView, TakeQuizView,QuizListTemplateView, QuizDetailTemplateView, TakeQuizTemplateView

router = DefaultRouter()
router.register(r'admin/quizzes', QuizViewSet)
router.register(r'admin/questions', QuestionViewSet)

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/quizzes/', QuizListView.as_view(), name='quiz-list'),
    path('api/quizzes/<int:pk>/', QuizDetailView.as_view(), name='quiz-detail'),
    path('api/quizzes/<int:pk>/attempt/', TakeQuizView.as_view(), name='take-quiz'),
     # Web interface
    path('quizzes/', QuizListTemplateView.as_view(), name='quiz_list'),
    path('quizzes/<int:pk>/', QuizDetailTemplateView.as_view(), name='quiz_detail'),
    path('quizzes/<int:pk>/take/', TakeQuizTemplateView.as_view(), name='take_quiz')
   
]
