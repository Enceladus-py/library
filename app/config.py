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

beat_schedule_filename = "app/celerybeat-schedule"
beat_schedule = {
    # Executes daily at 13.30
    "send-reminder-email-daily": {
        "task": "app.tasks.send_daily_reminder_overdue_books",
        "schedule": crontab(hour=13, minute=30),
    },
}
