from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from quizzes.models import Quiz, Question

User = get_user_model()

class Command(BaseCommand):
    help = "Seed database with quizzes and questions"

    def handle(self, *args, **kwargs):
        admin_user = User.objects.filter(is_superuser=True).first()
        if not admin_user:
            self.stdout.write(self.style.ERROR("No superuser found. Create one first."))
            return

        quizzes_data = [
            {
                "title": "General Knowledge Quiz",
                "description": "A quiz with 5 general knowledge questions.",
                "time_limit": 15,
                "questions": [
                    {
                        "text": "What is the capital of France?",
                        "option1": "London", "option2": "Paris", "option3": "Rome", "option4": "Berlin",
                        "correct_option": 2
                    },
                    {
                        "text": "What is 2 + 2?",
                        "option1": "3", "option2": "4", "option3": "5", "option4": "6",
                        "correct_option": 2
                    },
                    {
                        "text": "Who wrote 'Hamlet'?",
                        "option1": "Charles Dickens", "option2": "Leo Tolstoy",
                        "option3": "William Shakespeare", "option4": "Mark Twain",
                        "correct_option": 3
                    },
                    {
                        "text": "Largest planet in our solar system?",
                        "option1": "Earth", "option2": "Mars", "option3": "Jupiter", "option4": "Saturn",
                        "correct_option": 3
                    },
                    {
                        "text": "Element with symbol 'O'?",
                        "option1": "Gold", "option2": "Oxygen", "option3": "Silver", "option4": "Iron",
                        "correct_option": 2
                    }
                ]
            },
            # You can duplicate the structure for 4 more quizzes
            {
                "title": "Math Quiz",
                "description": "Basic math questions.",
                "time_limit": 10,
                "questions": [
                    {
                        "text": "What is 5 * 5?", "option1": "10", "option2": "25", "option3": "20", "option4": "15",
                        "correct_option": 2
                    },
                    {
                        "text": "Square root of 16?", "option1": "2", "option2": "4", "option3": "8", "option4": "16",
                        "correct_option": 2
                    },
                    {
                        "text": "10 divided by 2?", "option1": "2", "option2": "5", "option3": "10", "option4": "8",
                        "correct_option": 2
                    },
                    {
                        "text": "7 + 6?", "option1": "12", "option2": "13", "option3": "14", "option4": "15",
                        "correct_option": 2
                    },
                    {
                        "text": "15 - 7?", "option1": "8", "option2": "7", "option3": "9", "option4": "6",
                        "correct_option": 1
                    }
                ]
            }
            # Add 3 more quizzes with 5 questions each in the same way
        ]

        for qz_data in quizzes_data:
            quiz, created = Quiz.objects.get_or_create(
                title=qz_data["title"],
                defaults={
                    "description": qz_data["description"],
                    "time_limit": qz_data["time_limit"],
                    "created_by": admin_user
                }
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created quiz: {quiz.title}"))

            for q_data in qz_data["questions"]:
                question, q_created = Question.objects.get_or_create(
                    quiz=quiz,
                    text=q_data["text"],
                    defaults=q_data
                )
                if q_created:
                    self.stdout.write(self.style.SUCCESS(f"Added question: {question.text}"))
