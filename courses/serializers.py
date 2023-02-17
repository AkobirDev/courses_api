from rest_framework import serializers

from courses.models import Category, Course, CourseSection, Enrollment, Lesson

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'

class CourseSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    class Meta:
        model = Course
        fields = ('id', 'title', 'category', 'slug', 'thumbnail', 'description',
                   'price', 'discount', 'level', 'language', 'instructor',
                    'get_course_avg_rating', 'is_free', 'get_price', 'created_at')

class CourseSectionSerializer(serializers.ModelSerializer):
    class Meta:
        model = CourseSection
        fields = ('id', 'title', 'description', 'order',
                   'course', 'get_section_avg_rating', 'created_at')

class LessonSerializer(serializers.ModelSerializer):
    reviews = serializers.StringRelatedField(many=True)
    class Meta:
        model = Lesson
        fields = ('id', 'title', 'slug', 'description', 'video',
                  'duration', 'order', 'course', 'section', 'reviews', 'get_lesson_average_rating',  'created_at')

class EnrollmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Enrollment
        fields = '__all__'

class ReviewSerializer(serializers.ModelSerializer):
    class Meta:
        fields = '__all__'