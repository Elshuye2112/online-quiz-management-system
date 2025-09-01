from rest_framework import generics, viewsets, permissions
from .models import Quiz, Question, QuizAttempt,Answer
from .serializers import QuizSerializer, QuestionSerializer, QuizAttemptSerializer
    
from django.views.generic import ListView, DetailView, TemplateView
from django.shortcuts import get_object_or_404, redirect
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

    def get_serializer_context(self):
        context = super().get_serializer_context()
        quiz = Quiz.objects.get(pk=self.kwargs['pk'])
        context['quiz'] = quiz
        return context
# Web interface views
class QuizListTemplateView(ListView):
    model = Quiz
    template_name = "quizzes/quiz_list.html"

class QuizDetailTemplateView(DetailView):
    model = Quiz
    template_name = "quizzes/quiz_detail.html"

class TakeQuizTemplateView(TemplateView):
    template_name = "quizzes/take_quiz.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        quiz = get_object_or_404(Quiz, pk=self.kwargs['pk'])
        context["quiz"] = quiz
        return context

    def post(self, request, *args, **kwargs):
        quiz = get_object_or_404(Quiz, pk=kwargs['pk'])
        attempt = QuizAttempt.objects.create(user=request.user, quiz=quiz, score=0)

        score = 0
        for question in quiz.questions.all():
            selected = request.POST.get(f"question_{question.id}")
            if selected:
                Answer.objects.create(
                    attempt=attempt,
                    question=question,
                    selected_option=selected
                )
                if selected == question.correct_option:
                    score += 1

        attempt.score = score
        attempt.save()
        return redirect("quiz_detail", pk=quiz.pk)
