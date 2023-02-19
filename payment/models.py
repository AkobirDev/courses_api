from django.db import models
from django.contrib.auth import get_user_model

from courses.models import Enrollment
# Create your models here.

User = get_user_model()

PAYMENT_METHOD = (
    ('CASH', 'CASH'),
    ('CART', 'CART'),
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    payment_method = models.CharField(choices=PAYMENT_METHOD, default='CASH', max_length=5)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def get_enrolled_courses(self):
        enrolls = [enroll.course.title for enroll in self.user.paid_course.all()]
        return enrolls
    
    def get_total_price(self):
        courses = self.user.paid_course.all()
        # courses = self.user.get_paid_courses()
        amount = [c.course.price for c in courses]
        return sum(amount)
    
    def __str__(self):
        return f'{self.user} paid'

