from django.urls import path
from questions import views
from questions.views import ResultView, HomeView, WrongBlockView
from django.contrib.auth.decorators import login_required
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
	path('', HomeView.as_view(), name='home'),
	path('blocks/', views.blocks, name='blocks'),
	path('question_in_block/<int:block_id>', views.questioninblock, name='question_in_block'),
	path('answer/<int:question_id>', views.answer, name='answer'),
	path('results/<name>', login_required(ResultView.as_view()), name='results'),
	path('wrong_block/', WrongBlockView.as_view(), name='wrong_block'),
	path('register/', views.register, name='register'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)