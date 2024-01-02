from django_extensions.management.jobs import DailyJob


class Job(DailyJob):
    help = "Update soft data from samlab.ws."

    def execute(self):
        from apps.soft.models import update_db

        update_db()
