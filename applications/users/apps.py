from django.apps import AppConfig


class UsersConfig(AppConfig):
    name = 'applications.users'

    def ready(self):
        import applications.users.signals
