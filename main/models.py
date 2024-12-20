from django.db import models

class Prepod(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='prepod_photos/', null=True, blank=True)

    # Добавим поля для более детального описания
    bio = models.TextField(null=True, blank=True)  # Биография преподавателя
    department = models.CharField(max_length=100, null=True, blank=True)  # Отдел или кафедра

    def __str__(self):
        return self.name


class QuestionCategory(models.Model):
    title = models.CharField(max_length=100)
    description = models.TextField(null=True, blank=True)

    def __str__(self):
        return self.title

class Question(models.Model):
    title = models.CharField(max_length=150)
    category = models.ForeignKey(QuestionCategory, on_delete=models.CASCADE)  # Для какой категории

    def __str__(self):
        return self.title

class Answer(models.Model):
    prepod = models.ForeignKey(Prepod, on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return f"{self.prepod.name}, {self.question.title}, {self.answer}"