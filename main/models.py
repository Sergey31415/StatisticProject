from django.db import models

class Prepod(models.Model):
    name = models.CharField(max_length=100)
    photo = models.ImageField(upload_to='prepod_photos/', null=True, blank=True)

    def __str__(self):
        return self.name

class Questions(models.Model):
    title = models.CharField(max_length=150)

    def __str__(self):
        return self.title

class Answer(models.Model):
    prepod = models.ForeignKey(Prepod, on_delete=models.CASCADE)
    question = models.ForeignKey(Questions, on_delete=models.CASCADE)
    answer = models.IntegerField()

    def __str__(self):
        return f"{self.prepod.name}, {self.question.title}, {self.answer}"