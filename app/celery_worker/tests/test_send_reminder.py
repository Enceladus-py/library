import unittest
from unittest.mock import patch, MagicMock
from datetime import date

from app.celery_worker.tasks import send_daily_reminder_overdue_books
from app.models.email import Email


class TestSendReminder(unittest.TestCase):
    @patch("app.celery_worker.tasks.SessionLocal")
    def test_success(self, mock_session_local):
        # Mock the session and query execution
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        # Mock the query result with User and Patron objects
        patron1 = MagicMock(name="Patron1")
        patron2 = MagicMock(name="Patron2")
        mock_query_result = [
            (MagicMock(email="user1@example.com"), patron1),
            (MagicMock(email="user2@example.com"), patron2),
        ]

        mock_session.execute.return_value = mock_query_result

        result = send_daily_reminder_overdue_books()

        # Assert the emails created
        expected_emails = [
            {
                "email": "user1@example.com",
                "content": f"Dear {patron1.name}, this is a daily reminder for your overdue books. Please return them.",
                "send_date": date.today(),
            },
            {
                "email": "user2@example.com",
                "content": f"Dear {patron2.name}, this is a daily reminder for your overdue books. Please return them.",
                "send_date": date.today(),
            },
        ]
        self.assertEqual(result, expected_emails)

        # Assert the bulk insert and commit were called
        mock_session.bulk_insert_mappings.assert_called_with(Email, expected_emails)
        mock_session.commit.assert_called_once()
        mock_session.close.assert_called_once()

    @patch("app.celery_worker.tasks.SessionLocal")
    def test_failure(self, mock_session_local):
        # Mock the session and query execution
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        # Simulate an exception during bulk insert
        mock_session.bulk_insert_mappings.side_effect = Exception("DB Error")

        with self.assertRaises(Exception) as context:
            send_daily_reminder_overdue_books()

        self.assertTrue("DB Error" in str(context.exception))

        # Assert the commit was not called and session was closed
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once()
