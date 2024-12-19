from collections import defaultdict

from django.db.models import Avg
from django.shortcuts import render

from main.models import Answer


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