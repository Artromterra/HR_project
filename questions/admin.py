from django.contrib import admin
from .models import Block, Question, Answer, QuestionInBlock, UserProfile

# Register your models here.

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_filter = ('profile_user', 'block')
    fieldsets = (
        (None, {
            'fields': ('profile_user', 'block', 'poll_total', 'test_total')
        }),
        ('Выборка', {
            'fields': ('question', 'answer')
        }),
    )

# @admin.register(QuestionInBlock)
class QuestionInBlockInline(admin.TabularInline):
    model = QuestionInBlock
    extra = 0

@admin.register(Block)
class BlockAdmin(admin.ModelAdmin):
    list_display = ('title', 'type_block')
    inlines = [QuestionInBlockInline]

class AnswerInline(admin.TabularInline):
    model = Answer
    extra = 0

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = ('title', 'image', 'type_variant')
    inlines = [AnswerInline]



