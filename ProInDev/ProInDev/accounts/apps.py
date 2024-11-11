from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'ProInDev.accounts'

    def ready(self):
        from ProInDev.accounts import signals
