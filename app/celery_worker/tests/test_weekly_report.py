import unittest
from unittest.mock import patch, MagicMock
from datetime import date, timedelta
import json

from app.celery_worker.tasks import weekly_report_for_checkout_statistics


class TestWeeklyReport(unittest.TestCase):
    @patch("app.celery_worker.tasks.SessionLocal")
    @patch("app.celery_worker.tasks.open", create=True)
    @patch("app.celery_worker.tasks.to_dict")
    def test_success(self, mock_to_dict, mock_open, mock_session_local):
        # Mock the session and query execution
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        # Mock User
        mock_user = MagicMock()
        mock_user.id = 1
        mock_user.name = "John Doe"

        # Mock Patron
        mock_patron = MagicMock()
        mock_patron.id = 1
        mock_patron.user_id = 1

        # Mock Book
        mock_book = MagicMock()
        mock_book.id = 1
        mock_book.title = "Sample Book"
        mock_book.checkout_date = date.today() - timedelta(weeks=1)  # 1 week passed

        mock_session.execute.return_value = [(mock_user, mock_patron, mock_book)]

        # Set side effects for the to_dict function based on the input instance
        def mock_to_dict_function(instance):
            if instance == mock_user:
                return {
                    "id": instance.id,
                    "name": instance.name,
                }
            elif instance == mock_patron:
                return {
                    "id": instance.id,
                    "user_id": instance.user_id,
                }
            elif instance == mock_book:
                return {
                    "id": instance.id,
                    "title": instance.title,
                    "checkout_date": instance.checkout_date.isoformat(),
                }
            return {}

        mock_to_dict.side_effect = mock_to_dict_function

        result = weekly_report_for_checkout_statistics()

        # Assert the file was opened and written to
        mock_open.assert_called_once_with(f"reports/report-{date.today()}.txt", "x")
        mock_open.return_value.__enter__().write.assert_called_once()

        # Check the content written to the file
        written_content = json.loads(
            mock_open.return_value.__enter__().write.call_args[0][0]
        )
        expected_content = [
            {
                "book": {
                    "id": 1,
                    "title": "Sample Book",
                    "checkout_date": (date.today() - timedelta(weeks=1)).isoformat(),
                },
                "user": {
                    "id": 1,
                    "name": "John Doe",
                },
                "patron": {
                    "id": 1,
                    "user_id": 1,
                },
            }
        ]
        self.assertEqual(written_content, expected_content)

        # Assert the task returned the correct value
        self.assertEqual(result, expected_content)

        # Assert the bulk insert and commit were called
        mock_session.bulk_insert_mappings.assert_not_called()
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once()

    @patch("app.celery_worker.tasks.SessionLocal")
    def test_failure(self, mock_session_local):
        # Mock the session and query execution
        mock_session = MagicMock()
        mock_session_local.return_value = mock_session

        # Simulate an exception during bulk insert
        mock_session.execute.side_effect = Exception("DB Error")

        with self.assertRaises(Exception) as context:
            weekly_report_for_checkout_statistics()

        self.assertTrue("DB Error" in str(context.exception))

        # Assert the commit was not called and session was closed
        mock_session.commit.assert_not_called()
        mock_session.close.assert_called_once()
