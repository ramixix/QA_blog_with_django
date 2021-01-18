from django.apps import AppConfig


class UserConfig(AppConfig):
    name = 'user'

    # after adding signal.py and write propper funtions to handel the singals we need to import that here according to django configuration page 
    def ready(self):
        import user.signals