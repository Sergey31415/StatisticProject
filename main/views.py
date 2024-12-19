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

        # Перенаправляем пользователя после отправки
        return HttpResponse("Спасибо за ваши ответы!")
    return redirect('result')  # Или какая-то другая страница

def result(request):
    # Получаем среднее арифметическое по каждому вопросу для преподавателя с ID 1, используя заголовок (title) вопроса
    average_answers = Answer.objects.filter(prepod_id=request.GET.get('prepod')) \
        .values('question__title')  # Получаем заголовок вопросов (question__title)

    # Аггрегируем среднее значение для каждого вопроса
    average_answers = average_answers.annotate(avg_answer=Avg('answer'))

    result = []
    # Выводим результат
    for group in average_answers:
        question_text = group['question__title']
        avg_answer = group['avg_answer']
        ounded_avg_answer = round(avg_answer, 1)
        result.append([f"{question_text}, {ounded_avg_answer}"])

    return render(request, 'result.html', {'text': result})