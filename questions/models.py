from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from tinymce import models as tinymce_models
from datetime import datetime, date, time
from django.utils import timezone

# Create your models here.

class Question(models.Model):
	RADIO = 'RO'
	CHECKBOX = 'CX'
	TYPE_VARIANT_CHOICES = [
		(RADIO, 'Радиокнопка'),
		(CHECKBOX, 'Чекбокс'),
	]
	title = models.CharField("Вопрос", max_length=264, null=True, blank=True)
	image = models.ImageField("Картинка", blank=True, upload_to='media')
	type_variant = models.CharField("Выбор варианта", max_length=2, choices=TYPE_VARIANT_CHOICES, default=RADIO)

	class Meta:
		verbose_name = 'Вопрос'
		verbose_name_plural = 'Вопросы'
	
	def __str__(self):
		return f'id={self.id} -  {self.title}'

class Answer(models.Model):
	title = models.CharField("Ответ", max_length=128, null=True, blank=True)
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answer_in_question', verbose_name='Вопрос', null=True)
	correct = models.BooleanField(default=True,  help_text = 'Ставим галочку, если необходимо учесть вес ответа')
	weight = models.SmallIntegerField("Вес ответа в опроснике", editable=True, default=0)
	
	
	class Meta:
		verbose_name = 'Ответ'
		verbose_name_plural = 'Ответы'

	def __str__(self):
		return f'{self.title} - вес: {self.weight}'

class Block(models.Model):
	POLL = 'PL'
	TEST = 'TS'
	TYPE_BLOCK_CHOICES = [
		(POLL, 'Опросник'),
		(TEST, 'Тест'),
	]
	type_block = models.CharField("Тип тестов", max_length=2, choices=TYPE_BLOCK_CHOICES, default=TEST)
	title = models.CharField("Название", max_length=128, null=True, blank=True)
	description = tinymce_models.HTMLField("Описание", blank=True)
	question_count = models.SmallIntegerField("Question count", help_text = 'Поле не заполнять', default=0)
	is_passed = models.BooleanField("Сделать тест недоступным", default=False, help_text='Поставте галочку, для деактивации теста')
	date_begin = models.DateTimeField('Дата начала теста', default=timezone.now)

	class Meta:
		verbose_name = 'Блок тестов'
		verbose_name_plural = 'Блоки тестов'

	def __str__(self):
		return self.title


class QuestionInBlock(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='question', null=True, verbose_name='Вопрос')
	block = models.ForeignKey(Block, on_delete=models.CASCADE, related_name='block', verbose_name='Блок')

	class Meta:
		verbose_name = 'Вопрос в блоке'
		verbose_name_plural = 'Вопросы в блоке'

	def __str__(self):
		return str(f'{self.block} || {self.question}')	

class UserProfile(models.Model):
	user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь', blank=True, null=True)
	question_in_block = models.ManyToManyField(QuestionInBlock, related_name='question_in_block', verbose_name='Вопросы в блоке', default='', blank=True)
	answer = models.ManyToManyField(Answer, related_name='user_answer', verbose_name='Ответы', default='', blank=True)
	poll_total = models.SmallIntegerField("Сумма ответов опросника", editable=True, default=0)
	test_total = models.SmallIntegerField("Сумма ответов в тесте", editable=True, default=0)
	is_full = models.BooleanField("Проверка заполненности", default=False)
	
	class Meta:
		verbose_name = 'Статистика пользователя'
		verbose_name_plural = 'Статистика пользователей'

	def __str__(self):
		return str(self.user)
