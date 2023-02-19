from django.urls import path, include
from payment.views import PaymentView
from rest_framework import routers
from courses.views import ( 
    CategoryDetailView, 
    CategoryView, 
    CourseDetailView, 
    CoursesView,
    ReviewDetailView,
    ReviewsView, 
    SectionLessonsView,
    LessonView
)

from users.views import UserView

router = routers.DefaultRouter()
router.register(r'users', UserView, basename='user')


urlpatterns = [
    path('', include(router.urls)),
    path('courses-categories/', CategoryView.as_view(), name='courses-categories'),
    path('courses-categories/<int:id>', CategoryDetailView.as_view(), name='courses-category-detail'),
    path('courses/', CoursesView.as_view(), name='courses'),
    path('courses/<int:id>/', CourseDetailView.as_view(), name='course-detail'),
    path('courses/<int:course_id>/<int:section_id>/', SectionLessonsView.as_view(), name='section-lessons'),
    path('courses/<int:course_id>/<int:section_id>/<int:lesson_id>', LessonView.as_view(), name='lesson'),
    path('reviews/', ReviewsView.as_view(), name='reviews'),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view(), name='reviews-detail'),     
    path('payment/', PaymentView.as_view(), name='payment'),                           
]

