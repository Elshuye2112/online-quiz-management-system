from rest_framework import generics, viewsets, permissions
from .models import Quiz, Question, QuizAttempt
from .serializers import QuizSerializer, QuestionSerializer, QuizAttemptSerializer

# Admin APIs
class QuizViewSet(viewsets.ModelViewSet):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAdminUser]

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all()
    serializer_class = QuestionSerializer
    permission_classes = [permissions.IsAdminUser]

# User APIs
class QuizListView(generics.ListAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

class QuizDetailView(generics.RetrieveAPIView):
    queryset = Quiz.objects.all()
    serializer_class = QuizSerializer
    permission_classes = [permissions.IsAuthenticated]

class TakeQuizView(generics.CreateAPIView):
    serializer_class = QuizAttemptSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        quiz_id = self.kwargs['pk']  # get quiz ID from URL
        quiz = Quiz.objects.get(pk=quiz_id)
        serializer.save(user=self.request.user, quiz=quiz)
