from django.apps import AppConfig


class TaskifyConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'Taskify'

    def ready(self):
        import Taskify.signals
