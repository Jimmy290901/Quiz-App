from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from .models import Quiz, Score
from questions.models import MCQ, Textual
from .serializers import QuizSerializer
from questions.serializers import MCQSerializer, TextualSerializer
from django.utils import timezone
from django.contrib.auth.models import User

# Create your views here.

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def listQuizzes(request):
    if request.method == 'GET':
        quizzesList = Quiz.objects.all()
        serializer = QuizSerializer(quizzesList, many=True)
        return Response(serializer.data,status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def pastQuizzes(request):
    if request.method == 'GET':
        pastQuizzesList = Quiz.objects.filter(end_time__lt = timezone.now())
        serializer = QuizSerializer(pastQuizzesList, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def liveQuizzes(request):
    if request.method == 'GET':
        liveQuizzesList = Quiz.objects.filter(start_time__lte = timezone.now(), end_time__gte = timezone.now())
        serializer = QuizSerializer(liveQuizzesList, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def upQuizzes(request):
    if request.method == 'GET':
        upQuizzesList = Quiz.objects.filter(start_time__gt = timezone.now())
        serializer = QuizSerializer(upQuizzesList, many = True)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['GET'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def showQuestions(request, quiz_id):
    if request.method == 'GET':
        mcqs = MCQ.objects.filter(quiz = quiz_id)
        serializer_mcq = MCQSerializer(mcqs, many = True)
        textual = Textual.objects.filter(quiz = quiz_id)
        serializer_textual = TextualSerializer(textual, many = True)
        questionsList = {'MCQ':serializer_mcq.data, 'Textual': serializer_textual.data}
        return Response(questionsList, status = status.HTTP_200_OK)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def createQuiz(request):
    if request.method == 'POST':

        requestData = request.data
        if requestData['start_time'] >= requestData['end_time']:
            message = {'message':'Invalid Quiz'}
            return Response(message, status = status.HTTP_400_BAD_REQUEST)

        serializer = QuizSerializer(data = request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data,status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def addMCQ(request, quiz_id):
    if request.method == 'POST':
        requestData = request.data
        # print(requestData)
        # for i in range(len(requestData)):
        #     # requestData[i]['quiz'] = quiz_id
        #     requestData[i].update({'quiz':quiz_id})
        #     if requestData[i]['total_options'] not in range(2,5) or requestData[i]['correct_option_number'] not in range(1,5):
        #         message = {'message': str(i+1) + ' MCQ details are not proper'}
        #         return Response(message, status = status.HTTP_400_BAD_REQUEST)
        
        requestData['quiz'] = quiz_id
        if int(requestData['total_options']) not in range(2,5) or int(requestData['correct_option_number']) not in range(1,5):
            message = {'message': 'MCQ details are not proper'}
            return Response(message, status = status.HTTP_400_BAD_REQUEST)

        serializer = MCQSerializer(data=requestData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAdminUser])
def addTextual(request, quiz_id):
    if request.method == 'POST':
        requestData = request.data
        # for i in range(len(requestData)):
        #     requestData[i]['quiz'] = quiz_id
        requestData['quiz'] = quiz_id
        serializer = TextualSerializer(data=requestData)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status = status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'POST'])
@authentication_classes([BasicAuthentication])
@permission_classes([IsAuthenticated])
def attempt(request, quiz_id):

    #Checking if quiz is live or not
    quiz = get_object_or_404(Quiz, quiz_id = quiz_id)
    if quiz.end_time < timezone.now() or quiz.start_time > timezone.now():
        message = {'message':'Quiz not available'}
        return Response(message, status = status.HTTP_403_FORBIDDEN)
    
    #Checking if user has already attempted the quiz
    user = get_object_or_404(User, username = request.user.username)
    obj = Score.objects.filter(username = request.user.id, quiz_id = quiz_id)
    if obj.exists():
        scoreObj = Score.objects.get(username = request.user.id, quiz_id = quiz_id)
        if scoreObj.submitted == True:
            message = {'message':'You have already attempted the quiz'}
            return Response(message, status = status.HTTP_403_FORBIDDEN)
    else:
        Score.objects.create(username = user, quiz_id = quiz)

    if request.method == 'GET':
        mcqs = MCQ.objects.filter(quiz = quiz_id)
        serializer_mcq = MCQSerializer(mcqs, many = True)
        textual = Textual.objects.filter(quiz = quiz_id)
        serializer_textual = TextualSerializer(textual, many = True)
        questionsList = {'MCQ':serializer_mcq.data, 'Textual': serializer_textual.data}
        # print(type(serializer_mcq.data))
        return Response(questionsList, status = status.HTTP_200_OK)

    if request.method == 'POST':
        answers = request.data
        mcqAnswers = answers['MCQ']
        textualAnswers = answers['Textual']
        totalScore = 0
        #Evaluating MCQ Answers
        for i in range(len(mcqAnswers)):
            question = get_object_or_404(MCQ, id = mcqAnswers[i]['id'])
            if question.correct_option_number == mcqAnswers[i]['user_answer']:
                totalScore += 1
        #Evaluating Open Text Answers (assuming that such questions are one word or two word, i.e., they match the exact answer provided by author)
        for i in range(len(textualAnswers)):
            question = get_object_or_404(Textual, id = textualAnswers[i]['id'])
            if question.answer_text.lower() == textualAnswers[i]['user_answer'].lower():
                totalScore += 1
        scoreObj = Score.objects.get(username = request.user.id, quiz_id = quiz_id)
        scoreObj.score = totalScore
        scoreObj.submitted = True
        scoreObj.save()
        message = {'score':scoreObj.score}
        return Response(message, status = status.HTTP_200_OK)
        
