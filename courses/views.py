from django.shortcuts import render
from rest_framework.generics import ListAPIView, ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated

from courses.models import Category, Course, CourseSection, Lesson
from courses.permissions import IsUser, ReadOnly
from courses.serializers import CategorySerializer, CourseSectionSerializer, CourseSerializer, LessonSerializer


class CategoryView(ListAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    permission_classes = [IsUser | ReadOnly]

class CategoryDetailView(RetrieveUpdateDestroyAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'id'
    permission_classes = [IsUser | ReadOnly]

class CoursesView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, *args, **kwargs):
        queryset = Course.objects.all()
        serializer = CourseSerializer(queryset, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
    
class CourseDetailView(ListAPIView):
    serializer_class = CourseSectionSerializer
    permission_classes = [IsAuthenticated]
    def get_queryset(self, *args, **kwargs):
        id = self.kwargs['id']
        c = Course.objects.get(id=id)
        queryset = CourseSection.objects.filter(course=c)
        return queryset

class SectionLessonsView(ListAPIView):
    serializer_class = LessonSerializer
    def get_queryset(self):
        id = self.kwargs['course_id']
        c = Course.objects.get(id=id)
        section_id = self.kwargs['section_id']
        section = CourseSection.objects.filter(course=c).get(order=section_id)
        # section = CourseSection.objects.get(id=id)
        queryset = Lesson.objects.filter(section=section)
        return queryset

class LessonView(APIView):
    def get(self, request, course_id, section_id, lesson_id):
        id = self.kwargs['course_id']
        c = Course.objects.get(id=id)
        section_id = self.kwargs['section_id']
        section = CourseSection.objects.filter(course=c).get(order=section_id)
        lesson_id = self.kwargs['lesson_id']
        queryset = Lesson.objects.filter(section=section).get(order=lesson_id)
        serializer = LessonSerializer(queryset)

        return Response(data=serializer.data, status=status.HTTP_200_OK)

    # def get(self, request, id, *args, **kwargs):
    #     c = Category.objects.get(id=id)
    #     queryset = Course.objects.filter(category=c)
    #     serializer = CourseSerializer(queryset)

    #     return Response(data=serializer.data, status=status.HTTP_200_OK)

