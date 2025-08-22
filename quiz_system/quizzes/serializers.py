from rest_framework import serializers
from .models import Quiz, Question, QuizAttempt, Answer
from django.contrib.auth import get_user_model

User = get_user_model()

class QuestionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Question
        fields = '__all__'

class QuizSerializer(serializers.ModelSerializer):
    questions = QuestionSerializer(many=True, read_only=True)
    class Meta:
        model = Quiz
        fields = '__all__'

class AnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Answer
        fields = ['question', 'selected_option']

class QuizAttemptSerializer(serializers.ModelSerializer):
    answers = AnswerSerializer(many=True)

    class Meta:
        model = QuizAttempt
        fields = ['quiz','score','answers']

    def create(self, validated_data):
        answers_data = validated_data.pop('answers')
        attempt = QuizAttempt.objects.create(**validated_data)
        score = 0
        for answer_data in answers_data:
            question = answer_data['question']
            selected_option = answer_data['selected_option']
            Answer.objects.create(attempt=attempt, question=question, selected_option=selected_option)
            if question.correct_option == selected_option:
                score += 1
        attempt.score = score
        attempt.save()
        return attempt
