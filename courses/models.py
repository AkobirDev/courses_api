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

    def __str__(self):
        return self.title

    class Meta:
        ordering = ('-created_at',)


class Course(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
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

    @property
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
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)   

    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ('order',)


class Lesson(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='lessons')
    section = models.ForeignKey(CourseSection, on_delete=models.CASCADE)
    video = models.URLField(unique=True)
    duration = models.PositiveIntegerField(help_text='Duration the lessons must be in minutes')
    order = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        return super().save(*args, **kwargs)
        

class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('user', 'course')

    def __str__(self):
        return f'{self.user} --> {self.course}'