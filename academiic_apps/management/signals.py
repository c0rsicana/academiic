from academiic_apps.management.models import AcademicYear, Quarter
from django.db.models.signals import post_save
from django.dispatch import receiver


@receiver(post_save, sender=AcademicYear)
def after_saving_year(sender, created, instance, *args, **kwargs):
    if instance.active is True:
        AcademicYear.objects.exclude(pk=instance.id).update(current=False)


@receiver(post_save, sender=Quarter)
def after_saving_year(sender, created, instance, *args, **kwargs):
    if instance.active is True:
        AcademicYear.objects.exclude(pk=instance.id).update(current=False)