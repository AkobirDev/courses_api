from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.contrib.auth import get_user_model

from users.models import CustomUser
# Create your models here.

LANGUAGES = (
    ('uz', 'uzbek'),
    ('ru', 'russian'),
    ('eng', 'english'),

)

LEVEL = (
    ('all', 'All'),
    ('beg', 'Beginner'),
    ('int', 'Intermidiate'),
    ('adv', 'Advanced'), 
)

User = get_user_model()


class Category(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def get_courses(self):
        return [course.title for course in self.courses.all()]

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='courses')
    thumbnail = models.ImageField(upload_to='course-images', blank=True)
    description = models.TextField()
    price = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    discount = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    level = models.CharField(max_length=5, choices=LEVEL, default='all')
    language = models.CharField(max_length=3, choices=LANGUAGES, default='uz')
    instructor = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_course_avg_rating(self):
        section_ratings = [section.get_section_avg_rating() for section in self.sections.all() if section.get_section_avg_rating() is not None]
        return round((sum(section_ratings)/len(section_ratings) if len(section_ratings) else 0 ), 2)   
    
    def get_course_length(self):
        length = [section.get_section_length() for section in self.sections.all()]
        return sum(length)
    
    def get_total_lectures(self):
        l = [ls.get_lectures_num() for ls in self.sections.all()]
        return sum(l)

    def get_enrolled_students(self):
        return [e.user.username for e in self.get_course.all()]

    def is_free(self):
        return not self.price
    
    def get_price(self):
        if not self.discount:
            return self.price
        
        return round(self.price * (100 - self.discount) / 100, 2)

    def __str__(self):
        return self.title  
    

class CourseSection(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='sections')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)   

  
    def get_section_avg_rating(self):
        lesson_ratings = [lesson.get_lesson_average_rating() for lesson in self.lessons.all() if lesson.get_lesson_average_rating() is not None]    
        return round((sum(lesson_ratings)/len(lesson_ratings) if len(lesson_ratings) else 0 ), 2)
    

    def get_section_length(self):
        length = [lesson.duration for lesson in self.lessons.all()]
        return sum(length)
    

    def get_lectures_num(self):
        l = [lesson for lesson in self.lessons.all()]
        return len(l)


    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('order',)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE, related_name='lessons')
    video = models.URLField(unique=True)
    duration = models.PositiveIntegerField(help_text='Duration the lessons must be in minutes')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def get_lesson_average_rating(self):
        return round((self.reviews.aggregate(models.Avg('rating'))['rating__avg'] or 0 ) ,2)
        # return self.reviews.aggregate(models.Avg('rating'))['rating_avg']
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='paid_course')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='get_course')
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} --> {self.course}'
    

class Reviews(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='course_reviews')
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE, related_name='reviews')
    rating = models.IntegerField(
        validators=[MinValueValidator(0), MaxValueValidator(5)]
    )
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'lesson')
    
    def __str__(self):
        return f'{self.rating} to {self.lesson} by {self.user}'
    
