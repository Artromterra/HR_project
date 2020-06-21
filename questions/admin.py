from django.contrib import admin
from .models import Block, Question, Answer, QuestionInBlock, UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    # pass
    list_filter = ('user', 'question_in_block')
    fieldsets = (
        (None, {
            'fields': ('user', 'question_in_block','answer', 'poll_total', 'test_total')
        }),
        # ('Выборка', {
        #     'fields': ('', 'answer')
        # }),
    )

# @admin.register(QuestionInBlock)
class QuestionInBlockInline(admin.TabularInline):
    model = QuestionInBlock
    extra = 0

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    fields = ['title', 'type_block', 'description', 'is_passed', 'date_begin', 'question_count']
    inlines = [QuestionInBlockInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'type_variant')
    inlines = [AnswerInline]



