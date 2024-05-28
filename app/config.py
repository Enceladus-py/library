from celery.schedules import crontab

# jwt token config
SECRET_KEY = "e26ceed4fed28c0ae3615ae41294a0f7d7c06cbbbdcbbd6f33b505f4f72d92e3"
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

# celery config
broker_url = "redis://redis:6379/0"
result_backend = "redis://redis:6379/0"

broker_connection_retry_on_startup = True

task_serializer = "json"
result_serializer = "json"
accept_content = ["json"]

timezone = "Europe/Istanbul"
enable_utc = True

beat_schedule_filename = "celery_worker/celerybeat-schedule"
beat_schedule = {
    # Executes daily at 13.30
    "send-reminder-email-daily": {
        "task": "app.celery_worker.tasks.send_daily_reminder_overdue_books",
        "schedule": crontab(hour=13, minute=30),
    },
    # at every monday 12.00
    "checkout-weekly-report": {
        "task": "app.celery_worker.tasks.weekly_report_for_checkout_statistics",
        "schedule": crontab(hour=12, minute=0, day_of_week="mon"),
    },
}
