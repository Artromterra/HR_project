from django.shortcuts import render, get_object_or_404, redirect
from questions.models import Question, Answer, Block, QuestionInBlock, UserProfile
from django.http import HttpResponseRedirect
from django.views.generic import ListView, TemplateView
from .forms import UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.contrib.auth.models import User

# Create your views here.

class HomeView(TemplateView):
	template_name = 'home.html'

@login_required()
def blocks(request):
	user = request.user
	block = Block()
	user_profile = UserProfile.objects.filter(profile_user=user.username)
	allblocks = Block.objects.all()
	block_count = allblocks.count()
	context = {
		'allblocks': allblocks,
		'user_profile': user_profile,
		'user': user,
	}
	if bool(user_profile) is False:
		return render(request, 'blocks.html', context)
	else:
		if user_profile.count() == block_count:
			return render(request, 'end_test.html', context)
		else:
			return render(request, 'blocks.html', context)

@login_required()
def questioninblock(request, block_id):
	blocks = get_object_or_404(Block, pk=block_id)
	questions_in_block = QuestionInBlock.objects.filter(block__title=blocks.title)

	context = {
		'blocks': blocks,
		'questions_in_block': questions_in_block,
	}
	return render(request, 'question_in_block.html', context)

poll_list = []
test_list = []
poll_question_list = []
poll_answer_list = []
test_question_list = []
test_answer_list = []

@login_required()
def answer(request, question_id):
	user = request.user
	u_p = UserProfile()
	users_profiles = UserProfile.objects.filter(profile_user=user.username)
	question = get_object_or_404(Question, pk=question_id)
	block_id = QuestionInBlock.objects.get(id=question_id).block.id
	blocks = get_object_or_404(Block, pk=block_id)
	questions_count = QuestionInBlock.objects.filter(block__id=block_id).count()
	try:
		multiple_answer = question.answer_in_question.filter(id__in=request.POST.getlist('answer'))
		single_answer = question.answer_in_question.get(pk=request.POST['answer'])
	except (KeyError, Answer.DoesNotExist):
		context = {
			'blocks':blocks,
			'question': question,
			'error_message': "Вы не выбрали ответ.",
		}
		return render(request, 'answer.html', context)
	else:
		if blocks.type_block == 'PL': #проверка на тип теста и подсчет отвеченных вопросов
			for i in multiple_answer:
				poll_list.append(i.weight)
				poll_answer_list.append(i)
			poll_question_list.append(question)
		else:
			if single_answer.correct is True:
				question_weight = QuestionInBlock.objects.get(id=question_id).weight
				test_list.append(question_weight)
			test_question_list.append(question)
			test_answer_list.append(single_answer)
		blocks.question_count += 1
		blocks.save()
		sum_poll = sum(poll_list)
		sum_test = sum(test_list)
		if blocks.question_count >= questions_count:#когда отвечены все вопросы в блоке проверяем и сохраняем результаты
			# защита от повторного прохождения теста
			if bool(users_profiles) is True:
				for i in users_profiles:
					if i.block.title == blocks.title:
						break
				else:
					u_p.profile_user = user.username
					u_p.save()
					if blocks.type_block == 'PL': 
						for i in poll_question_list:
							u_p.question.add(i)
						for i in poll_answer_list:
							u_p.answer.add(i)
					else:
						for i in test_question_list:
							u_p.question.add(i)
						for i in test_answer_list:
							u_p.answer.add(i)
					u_p.test_total = sum_test 
					u_p.poll_total = sum_poll
					u_p.block = blocks
					u_p.save()
					poll_list.clear()
					test_list.clear()
					poll_question_list.clear()
					poll_answer_list.clear()
					test_question_list.clear()
					test_answer_list.clear()
					blocks.question_count = 0
					blocks.save()
					return HttpResponseRedirect(reverse('results', args=(user.username,)))
			else:
				u_p.profile_user = user.username
				u_p.save()
				if blocks.type_block == 'PL': 
					for i in poll_question_list:
						u_p.question.add(i)
					for i in poll_answer_list:
						u_p.answer.add(i)
				else:
					for i in test_question_list:
						u_p.question.add(i)
					for i in test_answer_list:
						u_p.answer.add(i)
				u_p.test_total = sum_test 
				u_p.poll_total = sum_poll
				u_p.block = blocks
				u_p.save()
			poll_list.clear()
			test_list.clear()
			poll_question_list.clear()
			poll_answer_list.clear()
			test_question_list.clear()
			test_answer_list.clear()
			blocks.question_count = 0
			blocks.save()
			return HttpResponseRedirect(reverse('results', args=(user.username,)))
		else:
			return redirect('/question_in_block/{}'.format(block_id))

class ResultView(ListView):# view results of passed tests for current user
	context_object_name = 'answer_list'
	template_name = 'results.html'

	def get_queryset(self):
		self.user = get_object_or_404(User, username=self.kwargs['name'])
		return UserProfile.objects.filter(profile_user=self.user.username)

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		context['actual_user'] = self.user
		return context

def register(request):# register a new user
	if request.method == 'POST':
		user_form = UserRegistrationForm(request.POST)
		if user_form.is_valid():
			new_user = user_form.save(commit=False)
			new_user.set_password(user_form.cleaned_data['password'])
			new_user.save()
			return render(request, 'registration/register_done.html', {'new_user': new_user})
	else:
		user_form = UserRegistrationForm()
	return render(request, 'registration/register.html', {'user_form': user_form})


