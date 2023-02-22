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
    path('courses-categories/', CategoryView.as_view() ),
    path('courses-categories/<int:id>', CategoryDetailView.as_view() ),
    path('courses/', CoursesView.as_view() ),
    path('courses/<int:id>/', CourseDetailView.as_view() ),
    path('courses/<int:course_id>/<int:section_id>/', SectionLessonsView.as_view() ),
    path('courses/<int:course_id>/<int:section_id>/<int:lesson_id>', LessonView.as_view() ),
    path('reviews/', ReviewsView.as_view() ),
    path('reviews/<int:review_id>/', ReviewDetailView.as_view()),     
    path('payment/', PaymentView.as_view() ),                           
]

