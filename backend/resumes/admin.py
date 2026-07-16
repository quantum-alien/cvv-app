from django.contrib import admin

from .models import Education, Experience, Resume, Skill


class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0


class EducationInline(admin.TabularInline):
    model = Education
    extra = 0


class SkillInline(admin.TabularInline):
    model = Skill
    extra = 0


@admin.register(Resume)
class ResumeAdmin(admin.ModelAdmin):
    list_display = ("title", "full_name", "job_title", "updated_at")
    search_fields = ("title", "full_name", "email")
    inlines = [ExperienceInline, EducationInline, SkillInline]
