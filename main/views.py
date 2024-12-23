from collections import defaultdict

from django.db.models import Q


from django.http import HttpResponse
from django.shortcuts import render, redirect

from main import models
from main.models import Answer, Question, Prepod, QuestionCategory

from django.db.models import Q



def questionnaire(request):
    questions = Question.objects.all()
    prepod_id = request.GET.get('prepod')
    prepod = Prepod.objects.get(pk=prepod_id)
    context = {'prepod': prepod, 'questions': questions}
    return render(request, 'questionnaire.html', context)

def submit_ratings(request):
    if request.method == 'POST':
        # Сохраняем рейтинги для каждого вопроса
        questions = Question.objects.all()
        for question in questions:
            rating = request.POST.get(f'rating_{question.id}')
            prepod = Prepod.objects.get(id=request.POST.get('prepod_id'))
            Answer.objects.create(question=question, prepod=prepod, answer=int(rating))
            print(f"Rating for {question.id}: {rating}")

    return redirect('home')  # Или какая-то другая страница


from django.db.models import Count, Avg


def result(request):
    # Получаем среднее арифметическое по каждому вопросу для преподавателя с ID из запроса
    average_answers = Answer.objects.filter(prepod_id=request.GET.get('prepod')) \
        .values('question__title', 'question_id')  # Получаем заголовок вопросов и их ID

    # Аггрегируем среднее значение для каждого вопроса
    average_answers = average_answers.annotate(
        avg_answer=Avg('answer'),  # Средний рейтинг для каждого вопроса
    )

    prepod = Prepod.objects.get(id=request.GET.get('prepod'))  # Получаем объект преподавателя
    prepod_name = prepod.name
    result = []

    # Выводим результат, включая количество проголосовавших
    for group in average_answers:
        question_text = group['question__title']
        question_id = group['question_id']  # ID вопроса
        avg_answer = group['avg_answer']
        rounded_avg_answer = round(avg_answer, 1)

        # Подсчитываем количество проголосовавших для данного вопроса
        voters_count = Answer.objects.filter(question_id=question_id).count()

        result.append({
            "question_title": question_text,
            "average_rating": rounded_avg_answer,
            "voters_count": voters_count,  # Добавляем количество проголосовавших для каждого вопроса
        })


    # Фильтруем категории с учетом только ответов данного преподавателя
    categories_with_avg = QuestionCategory.objects.annotate(
        average_score=Avg(
            'question__answer__answer',
            filter=Q(question__answer__prepod=prepod)  # Исправлено на Q
        )
    ).filter(
        question__answer__prepod=prepod
    ).distinct()

    # Преобразуем QuerySet в список словарей
    categories_data = list(categories_with_avg.values('title', 'average_score'))


    return render(request, 'result.html', {'result': result, 'prepod_name': prepod_name, 'prepod': prepod, 'categories_data': categories_data})



def home(request):
    prepods = Prepod.objects.all()
    return render(request, 'home.html', {'prepods': prepods})
