from django.apps import AppConfig


class BorrowingConfig(AppConfig):
    default_auto_field = "django.db.models.BigAutoField"
    name = "borrowing"

    def ready(self):
        """
        Imports the signals module to register
        the signal handlers for the Borrowing app.
        """
        import borrowing.signals
