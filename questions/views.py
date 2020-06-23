from django.shortcuts import render, get_object_or_404, redirect
from questions.models import Question, Answer, Block, QuestionInBlock, UserProfile
from django.http import HttpResponseRedirect, HttpResponse
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
	user_profile = UserProfile.objects.filter(user=user)
	allblocks = Block.objects.all()
	block_count = allblocks.count()
	u_p = UserProfile()
	context = {
		'allblocks': allblocks,
		'user_profile': user_profile,
		'user': user,
	}
	if user_profile.count() < block_count:
		u_p.user = user
		u_p.save()
	else:
		return render(request, 'end_test.html', context)
	if user_profile.count() > block_count:
		return render(request, 'end_test.html', context)
	else:
		return render(request, 'blocks.html', context)

class WrongBlockView(TemplateView):
	template_name = 'wrong_block.html'

@login_required()
def questioninblock(request, block_id):
	user = request.user
	user_profile = UserProfile.objects.filter(user=user)
	blocks = get_object_or_404(Block, pk=block_id)
	block_count = Block.objects.all().count()
	questions_in_block = QuestionInBlock.objects.filter(block__id=blocks.id)
	context = {
		'blocks': blocks,
		'questions_in_block': questions_in_block,
	}
	for i in user_profile: # проверка на повторное прохождение теста
		for a in i.question_in_block.all():
			if a.block.id == block_id and i.question_in_block.all().count() == questions_in_block.count():
				return redirect('wrong_block')
	return render(request, 'question_in_block.html', context)


@login_required()
def answer(request, question_id):
	user = request.user
	question = QuestionInBlock.objects.get(id=question_id) 
	block_id = QuestionInBlock.objects.get(id=question_id).block.id
	blocks = get_object_or_404(Block, pk=block_id)
	users_profiles = UserProfile.objects.filter(user=user)
	questions_count = QuestionInBlock.objects.filter(block__id=block_id).count()
	try:
		multiple_answer = question.question.answer_in_question.filter(id__in=request.POST.getlist('answer'))
		single_answer = question.question.answer_in_question.get(pk=request.POST['answer'])
	except (KeyError, Answer.DoesNotExist):
		context = {
			'blocks':blocks,
			'question': question,
			'error_message': "Вы не выбрали ответ.",
		}
		return render(request, 'answer.html', context)

	for i in users_profiles:
		if i.question_in_block.all().count() != questions_count and i.is_full is False:
			if blocks.type_block == 'PL': #проверка на тип теста и подсчет отвеченных вопросов
				for a in multiple_answer:
					i.answer.add(a)
				i.question_in_block.add(question)
			else:
				i.answer.add(single_answer)
				i.question_in_block.add(question)
	blocks.question_count += 1
	blocks.save()
	if blocks.question_count >= questions_count:#когда отвечены все вопросы в блоке проверяем и сохраняем результаты
		user_data = UserProfile.objects.filter(user=user, question_in_block__block_id=blocks.id)
		for i in user_data:
			if blocks.type_block == 'TS':
				for a in i.answer.all():
					if a.correct:
						i.test_total += a.weight
						i.save()
			else:
				for a in i.answer.all():
					if a.correct is False:
						i.poll_total += a.weight
						i.save()
			i.is_full = True
			i.save()
		
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
		return UserProfile.objects.filter(user=self.user)

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
