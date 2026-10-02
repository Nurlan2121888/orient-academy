from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import redirect, render

from .models import (
    Group,
    Student,
    Lesson,
    Attendance,
)
from django.core.mail import send_mail
from django.contrib import messages
from .forms import ContactForm

class TeacherLoginView(LoginView):

    template_name = "login.html"

    redirect_authenticated_user = True

    def get_success_url(self):
        return "/dashboard/"


@login_required
def dashboard_home(request):

    teacher = request.user

    groups = Group.objects.filter(
        teacher=teacher
    )

    students = Student.objects.filter(
        groups__teacher=teacher
    ).distinct()

    lessons = Lesson.objects.filter(
        group__teacher=teacher
    )

    context = {
        "groups": groups,
        "students": students,
        "lessons": lessons,

        "group_count": groups.filter(
            is_active=True
        ).count(),

        "student_count": students.filter(
            is_active=True
        ).count(),

        "lesson_count": lessons.count(),
    }

    return render(
        request,
        "dashboard.html",
        context
    )


@login_required
def groups_list(request):

    groups = Group.objects.filter(
        teacher=request.user
    ).prefetch_related(
        "students"
    )

    return render(
        request,
        "groups.html",
        {
            "groups": groups
        }
    )


@login_required
def group_detail(request, group_id):

    group = Group.objects.filter(
        id=group_id,
        teacher=request.user
    ).prefetch_related(
        "students",
        "lessons__attendances"
    ).first()

    if group is None:
        return redirect("groups")

    students = group.students.all()
    lessons = group.lessons.all()

    for lesson in lessons:

        lesson.total_students = students.count()

        lesson.present_count = lesson.attendances.filter(
            status="present"
        ).count()

        lesson.absent_count = lesson.attendances.filter(
            status="absent"
        ).count()

    return render(
        request,
        "group_detail.html",
        {
            "group": group,
            "students": students,
            "lessons": lessons,
        }
    )


@login_required
def lesson_create(request, group_id):

    group = Group.objects.filter(
        id=group_id,
        teacher=request.user
    ).first()

    if group is None:
        return redirect("groups")

    if request.method == "POST":

        title = request.POST.get("title")
        description = request.POST.get("description")
        lesson_date = request.POST.get("lesson_date")
        start_time = request.POST.get("start_time")
        end_time = request.POST.get("end_time")

        Lesson.objects.create(
            group=group,
            title=title,
            description=description,
            lesson_date=lesson_date,
            start_time=start_time or None,
            end_time=end_time or None,
        )

        return redirect(
            "group_detail",
            group_id=group.id
        )

    return render(
        request,
        "lesson_create.html",
        {
            "group": group
        }
    )


@login_required
def lesson_edit(request, lesson_id):

    lesson = Lesson.objects.filter(
        id=lesson_id,
        group__teacher=request.user
    ).first()

    if lesson is None:
        return redirect("groups")

    if request.method == "POST":

        lesson.title = request.POST.get("title")

        lesson.description = request.POST.get(
            "description"
        )

        lesson.lesson_date = request.POST.get(
            "lesson_date"
        )

        lesson.start_time = request.POST.get(
            "start_time"
        ) or None

        lesson.end_time = request.POST.get(
            "end_time"
        ) or None

        lesson.save()

        return redirect(
            "group_detail",
            group_id=lesson.group.id
        )

    return render(
        request,
        "lesson_edit.html",
        {
            "lesson": lesson,
            "group": lesson.group,
        }
    )


@login_required
def lesson_delete(request, lesson_id):

    lesson = Lesson.objects.filter(
        id=lesson_id,
        group__teacher=request.user
    ).first()

    if lesson is None:
        return redirect("groups")

    if request.method == "POST":

        group_id = lesson.group.id

        lesson.delete()

        return redirect(
            "group_detail",
            group_id=group_id
        )

    return render(
        request,
        "lesson_delete.html",
        {
            "lesson": lesson,
            "group": lesson.group,
        }
    )


@login_required
def attendance(request, lesson_id):

    lesson = Lesson.objects.filter(
        id=lesson_id,
        group__teacher=request.user
    ).first()

    if lesson is None:
        return redirect("groups")

    students = lesson.group.students.all()

    attendance_records = {
        record.student_id: record.status
        for record in lesson.attendances.all()
    }

    for student in students:

        student.attendance_status = attendance_records.get(
            student.id,
            "absent"
        )

    if request.method == "POST":

        for student in students:

            is_present = request.POST.get(
                f"student_{student.id}"
            )

            status = (
                "present"
                if is_present
                else "absent"
            )

            Attendance.objects.update_or_create(
                lesson=lesson,
                student=student,
                defaults={
                    "status": status
                }
            )

        return redirect(
            "attendance",
            lesson_id=lesson.id
        )

    return render(
        request,
        "attendance.html",
        {
            "lesson": lesson,
            "group": lesson.group,
            "students": students,
        }
    )

@login_required
def profile(request):

    user = request.user

    if request.method == "POST":

        first_name = request.POST.get(
            "first_name"
        )

        last_name = request.POST.get(
            "last_name"
        )

        email = request.POST.get(
            "email"
        )

        password = request.POST.get(
            "password"
        )

        password_confirm = request.POST.get(
            "password_confirm"
        )

        user.first_name = first_name
        user.last_name = last_name
        user.email = email

        user.save()

        if password:

            if password == password_confirm:

                user.set_password(password)

                user.save()

                return redirect("login")

        return redirect("profile")

    return render(
        request,
        "profile.html",
        {
            "profile_user": user
        }
    )

def home(request):

    if request.user.is_authenticated:
        return redirect("dashboard_home")

    return redirect("login")

def contact(request):

    if request.method == "POST":

        form = ContactForm(request.POST)

        if form.is_valid():

            name = form.cleaned_data["name"]
            email = form.cleaned_data["email"]
            message = form.cleaned_data["message"]

            send_mail(
                subject=f"Orient Academy Contact - {name}",

                message=f"""
Name: {name}
Email: {email}

Message:
{message}
""",

                from_email=None,

                recipient_list=[
                    "SƏNİN_EMAILİN"
                ],

                reply_to=[
                    email
                ],
            )

            messages.success(
                request,
                "Your message has been sent successfully!"
            )

            return redirect("contact")

    else:
        form = ContactForm()

    return render(
        request,
        "contact.html",
        {
            "form": form
        }
    )