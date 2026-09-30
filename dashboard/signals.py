from django.conf import settings
from django.core.mail import send_mail
from django.db.models.signals import post_delete, post_save
from django.dispatch import receiver


@receiver(
    post_save,
    sender=settings.AUTH_USER_MODEL
)
def send_user_registration_email(
    sender,
    instance,
    created,
    **kwargs
):

    print("SIGNAL ISLEYIR")
    print("CREATED:", created)
    print("EMAIL:", instance.email)

    if not created:
        return

    if not instance.email:
        return

    result = send_mail(
    subject="Orient Academy — Hesabınız yaradıldı",
    message=f"""
        Salam, {instance.get_full_name() or instance.username}!

        Sizin üçün Orient Academy müəllim panelində yeni hesab yaradıldı.

        Hesab məlumatınız:

        İstifadəçi adı: {instance.username}

        Artıq müəllim panelinə daxil olaraq qruplarınızı, tələbələrinizi və dərslərinizi idarə edə bilərsiniz.

        Hesabınıza aid məlumatları təhlükəsiz saxlayın və giriş məlumatlarınızı başqa şəxslərlə paylaşmayın.

        Hörmətlə,
        Orient Academy
        """,
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            instance.email
        ],
        fail_silently=False,
    )

    print("EMAIL SEND RESULT:", result)
    
    print("USER ID:", instance.id)
    
@receiver(
    post_delete,
    sender=settings.AUTH_USER_MODEL
)
def send_user_deleted_email(
    sender,
    instance,
    **kwargs
):

    if not instance.email:
        return

    send_mail(
        subject="Orient Academy — Hesabınız silindi",
        message=f"""
Salam, {instance.get_full_name() or instance.username}!

Sizin Orient Academy müəllim panelindəki hesabınız silinmişdir.

Hesab məlumatınız:

İstifadəçi adı: {instance.username}

Bu hesabla artıq müəllim panelinə daxil olmaq mümkün olmayacaq.

Əgər hesabın silinməsi ilə bağlı sualınız varsa, administratorla əlaqə saxlaya bilərsiniz.

Hörmətlə,
Orient Academy
""",
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[
            instance.email
        ],
        fail_silently=False,
    )