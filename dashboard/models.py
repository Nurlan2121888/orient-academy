from django.db import models
from django.contrib.auth.models import User


class Group(models.Model):
    name = models.CharField(
        max_length=100
    )

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="teaching_groups"
    )

    start_date = models.DateField()

    end_date = models.DateField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name


class Student(models.Model):
    first_name = models.CharField(
        max_length=100
    )

    last_name = models.CharField(
        max_length=100
    )

    email = models.EmailField(
        blank=True
    )

    phone = models.CharField(
        max_length=30,
        blank=True
    )

    groups = models.ManyToManyField(
        Group,
        related_name="students",
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    is_active = models.BooleanField(
        default=True
    )

    class Meta:
        ordering = ["first_name", "last_name"]

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Lesson(models.Model):
    group = models.ForeignKey(
        Group,
        on_delete=models.CASCADE,
        related_name="lessons"
    )

    title = models.CharField(
        max_length=200
    )

    description = models.TextField(
        blank=True
    )

    lesson_date = models.DateField()

    start_time = models.TimeField(
        null=True,
        blank=True
    )

    end_time = models.TimeField(
        null=True,
        blank=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        ordering = ["-lesson_date", "-start_time"]

    def __str__(self):
        return f"{self.group.name} - {self.title}"


class Attendance(models.Model):

    STATUS_CHOICES = [
        ("present", "İştirak edib"),
        ("absent", "İştirak etməyib"),
    ]

    lesson = models.ForeignKey(
        Lesson,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    student = models.ForeignKey(
        Student,
        on_delete=models.CASCADE,
        related_name="attendances"
    )

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default="absent"
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["lesson", "student"],
                name="unique_lesson_student_attendance"
            )
        ]

    def __str__(self):
        return f"{self.student} - {self.lesson}"