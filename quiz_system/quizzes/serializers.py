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
        fields = ['score', 'answers']
        read_only_fields = ['score']   # user should not submit score manually

    def create(self, validated_data):
        request = self.context['request']  # get user from request
        quiz=self.context('quiz')
        answers_data = validated_data.pop('answers')
        # quiz = validated_data['quiz']

        # create attempt for the current user
        attempt = QuizAttempt.objects.create(
            user=request.user,
            quiz=quiz,
            score=0
        )

        score = 0
        for answer_data in answers_data:
            question_id = answer_data['question'].id if isinstance(answer_data['question'], Question) else answer_data['question']
            question = Question.objects.get(id=question_id)

            selected_option = answer_data['selected_option']

            Answer.objects.create(
                attempt=attempt,
                question=question,
                selected_option=selected_option
            )

            if question.correct_option == selected_option:
                score += 1

        attempt.score = score
        attempt.save()
        return attempt
