# Library FastAPI Project

This is the repository for `Library FastAPI` project.


To run the server simply type:
```
docker compose up
```
This code will build the required images and start the API server. 

You can access the swagger UI from [localhost:8000/docs]()

## Used technologies
- FastAPI
- celery, celery-beat
- Docker
- PostreSQL
- SQLAlchemy
- Redis

## Authentication
To authenticate, the user should register first with a username, email and a password. After that, a patron can be created with that related user to return or checkout from the API. JWT tokens are used to get current user info.

## Celery configuration

To schedule the tasks `celery` and `celery-beat` is used. There are 2 tasks. One is for daily reminder and other one is for generating weekly reports. You can access the schedule parameters from `config.py`.
```
beat_schedule = {
    "send-reminder-email-daily": {
        "task": "app.celery_worker.tasks.send_daily_reminder_overdue_books",
        "schedule": crontab(hour=13, minute=30),
    },
    "checkout-weekly-report": {
        "task": "app.celery_worker.tasks.weekly_report_for_checkout_statistics",
        "schedule": crontab(hour=12, minute=0, day_of_week="mon"),
    },
}
```

- First one is scheduled for every day at 13.30

- Second one is scheduled for every monday at 12.00

## Testing
To test the celery, `MagicMock` from the `unittest` library is mainly used. Success and failure tests exist for both tasks. You can check the result of the test from `app/` directory with:
```
python3 -m unittest discover celery_worker.tests
```

## Linting
For styling the code and fixing errors, `ruff` package is used with the following command:
```
ruff check --fix
ruff format
```