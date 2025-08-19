import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils.timezone import now
from django.views import View

from rest_framework import status, permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Question, Option, ExamAttempt
from .serializers import (
    QuestionSerializer,
    ExamAttemptSerializer,
    UserRegisterSerializer
)
from .forms import RegisterForm, LoginForm

# ---------------------------
# Simple health endpoint
# ---------------------------
@api_view(['GET'])
@permission_classes([permissions.AllowAny])
def health_view(request):
    return Response({"status": "ok"})

# ---------------------------
# Registration API
# ---------------------------
class RegisterView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        serializer = UserRegisterSerializer(data=request.data) if False else UserRegisterSerializer(data=request.data)
        # Use our serializer for DRF register
        serializer = UserRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response({"message": "user created", "username": user.username}, status=status.HTTP_201_CREATED)

# ---------------------------
# API: Start exam
# ---------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_start_exam(request):
    """
    POST /api/exam/start/
    body: { "num_questions": 10 }  (optional)
    response: attempt_id, duration_seconds, questions[]
    """
    num_q = int(request.data.get("num_questions", 10))
    questions = list(Question.objects.prefetch_related('options').all())
    if len(questions) == 0:
        return Response({"error": "no questions available"}, status=status.HTTP_400_BAD_REQUEST)

    # pick random questions
    selected = random.sample(questions, min(num_q, len(questions)))
    ids = [q.id for q in selected]

    attempt = ExamAttempt.objects.create(
        user=request.user,
        total_questions=len(ids),
        duration_seconds=1800,  # default or config in settings
        questions_snapshot={"ids": ids}
    )

    # return questions without is_correct
    q_ser = QuestionSerializer(selected, many=True)
    return Response({
        "attempt_id": attempt.id,
        "duration_seconds": attempt.duration_seconds,
        "questions": q_ser.data
    }, status=status.HTTP_201_CREATED)

# ---------------------------
# API: Submit exam
# ---------------------------
@api_view(['POST'])
@permission_classes([permissions.IsAuthenticated])
def api_submit_exam(request, attempt_id):
    """
    POST /api/exam/<attempt_id>/submit/
    body: { "answers": { "question_id": option_id, ... } }
    """
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    if attempt.submitted_at:
        return Response({"error": "already submitted"}, status=status.HTTP_400_BAD_REQUEST)

    answers = request.data.get("answers", {})
    if not isinstance(answers, dict):
        return Response({"error": "answers must be a JSON object"}, status=status.HTTP_400_BAD_REQUEST)

    score = 0
    # validate answers against snapshot
    snapshot_ids = set(attempt.questions_snapshot.get("ids", []))
    for qid_str, oid in answers.items():
        try:
            qid = int(qid_str)
        except ValueError:
            continue
        if qid not in snapshot_ids:
            continue
        # check option correctness
        try:
            opt = Option.objects.get(id=oid, question_id=qid)
            if opt.is_correct:
                score += 1
        except Option.DoesNotExist:
            continue

    attempt.answers = answers
    attempt.score = score
    attempt.submitted_at = now()
    attempt.save()

    return Response({
        "attempt_id": attempt.id,
        "score": score,
        "total_questions": attempt.total_questions
    })

# ---------------------------
# API: Get result
# ---------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_get_result(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    if not attempt.submitted_at:
        return Response({"error": "result not available, exam not submitted"}, status=status.HTTP_404_NOT_FOUND)
    serializer = ExamAttemptSerializer(attempt)
    return Response(serializer.data)

# ---------------------------
# API: fetch questions (admin or testing)
# ---------------------------
@api_view(['GET'])
@permission_classes([permissions.IsAuthenticated])
def api_get_all_questions(request):
    qs = Question.objects.prefetch_related('options').all()
    serializer = QuestionSerializer(qs, many=True)
    return Response(serializer.data)

# ---------------------------
# TEMPLATE VIEWS (simple HTML pages for validation)
# ---------------------------
def TemplateIndexRedirectView(request):
    # Simple redirect to login page (root path)
    return redirect('exam_login')

def register_view(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data["password"])
            user.save()
            return redirect('exam_login')
    else:
        form = RegisterForm()
    return render(request, "registration.html", {"form": form})

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            user = authenticate(request,
                                username=form.cleaned_data["username"],
                                password=form.cleaned_data["password"])
            if user:
                login(request, user)
                return redirect("exam_start")
            else:
                form.add_error(None, "Invalid credentials")
    else:
        form = LoginForm()
    return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("exam_login")

@login_required
def exam_start_view(request):
    # start and redirect to take page
    if request.method == "POST":
        num_q = int(request.POST.get("num_questions", 10))
        questions = list(Question.objects.all())
        selected = random.sample(questions, min(len(questions), num_q))
        ids = [q.id for q in selected]
        attempt = ExamAttempt.objects.create(user=request.user, total_questions=len(ids), questions_snapshot={"ids": ids})
        return redirect("exam_take", attempt_id=attempt.id)
    return render(request, "exam_start.html")

@login_required
def exam_take_view(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    q_ids = attempt.questions_snapshot.get("ids", [])
    questions = Question.objects.filter(id__in=q_ids).prefetch_related('options')

    if request.method == "POST":
        answers = {}
        score = 0
        for q in questions:
            v = request.POST.get(str(q.id))
            if not v:
                continue
            try:
                opt_id = int(v)
                answers[str(q.id)] = opt_id
                if Option.objects.filter(id=opt_id, question=q, is_correct=True).exists():
                    score += 1
            except ValueError:
                pass
        attempt.answers = answers
        attempt.score = score
        attempt.submitted_at = now()
        attempt.save()
        return redirect("exam_result", attempt_id=attempt.id)

    return render(request, "exam_take.html", {"questions": questions, "attempt": attempt})

@login_required
def exam_result_view(request, attempt_id):
    attempt = get_object_or_404(ExamAttempt, id=attempt_id, user=request.user)
    return render(request, "exam_result.html", {"attempt": attempt})
