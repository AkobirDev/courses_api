# Generated by Django 4.1.7 on 2023-02-17 16:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('courses', '0006_alter_lesson_course_alter_lesson_section'),
    ]

    operations = [
        migrations.AlterField(
            model_name='coursesection',
            name='course',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sections', to='courses.course'),
        ),
    ]
