from django.apps import AppConfig


class ThesisConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'thesis'

from django.db.models.signals import post_migrate

def reset_no_of_slots(sender, **kwargs):
    from thesis.models import ProgramSlot
    ProgramSlot.objects.update(no_of_slot=0)
    print("All no_of_slot fields have been reset to 0 on server startup.")

class ThesisConfig(AppConfig):
    name = 'thesis'

    def ready(self):
        post_migrate.connect(reset_no_of_slots, sender=self)
