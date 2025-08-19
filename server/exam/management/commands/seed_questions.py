from django.core.management.base import BaseCommand
from exam.models import Question, Option

SAMPLE = [
    ("What is 2+2?", [("3", False), ("4", True), ("22", False), ("5", False)]),
    ("Which is a Python web framework?", [("Flask", True), ("MongoDB", False), ("Redis", False), ("PostgreSQL", False)]),
    ("What does JSON stand for?", [("JavaScript Object Notation", True), ("Java Standard Object Notation", False), ("Just Simple Object Notation", False), ("JS Object Normal", False)]),
    ("Which HTTP status means Not Found?", [("200", False), ("404", True), ("500", False), ("403", False)]),
    ("Which hook is for state in React?", [("useState", True), ("useEffect", False), ("useMemo", False), ("useRef", False)]),
]

class Command(BaseCommand):
    help = "Seed sample questions and options"

    def handle(self, *args, **kwargs):
        if Question.objects.exists():
            self.stdout.write(self.style.WARNING("Questions already present — skipping."))
            return
        for text, opts in SAMPLE:
            q = Question.objects.create(text=text)
            for text_opt, is_correct in opts:
                Option.objects.create(question=q, text=text_opt, is_correct=is_correct)
        self.stdout.write(self.style.SUCCESS("Seeded sample questions."))
