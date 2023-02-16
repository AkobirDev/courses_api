from django.contrib import admin

from courses.models import Category, Course, CourseSection, Enrollment, Lesson

# Register your models here.
admin.site.register(Category)

@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = ('title', 'instructor')

@admin.register(CourseSection)
class SectionAdmin(admin.ModelAdmin):
    list_display = ('title', 'course', 'order')

@admin.register(Lesson)
class LessonAdmin(admin.ModelAdmin):
    list_display = ('title', 'order', 'section')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('user', 'course')