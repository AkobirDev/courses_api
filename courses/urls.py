from django.urls import path

from courses.views import CourseListView, CourseDetailView, LessonDetailView

app_name = 'courses'
urlpatterns = [
    path('', CourseListView.as_view(), name='courses'),
    path('<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('<int:course_id>/lessons/<int:lesson_id>/', LessonDetailView.as_view(), name='lesson'),
]