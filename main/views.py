from collections import defaultdict

from django.db.models import Avg
from django.http import HttpResponse
from django.shortcuts import render, redirect

from main.models import Answer, Questions, Prepod


def questionnaire(request):
    questions = Questions.objects.all()
    prepod_id = request.GET.get('prepod')
    prepod = Prepod.objects.get(pk=prepod_id)
    context = {'prepod': prepod, 'questions': questions}
    return render(request, 'questionnaire.html', context)

def submit_ratings(request):
    if request.method == 'POST':
        # Сохраняем рейтинги для каждого вопроса
        questions = Questions.objects.all()
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

    return render(request, 'result.html', {'result': result, 'prepod_name': prepod_name, 'prepod': prepod})



def home(request):
    prepods = Prepod.objects.all()
    return render(request, 'home.html', {'prepods': prepods})
