# from django.test import TestCase
# from unittest.mock import patch
# from notifications.tasks import send_attendance_reminder
# from celery.result import AsyncResult
#
# class CeleryTaskTests(TestCase):
#
#     @patch('notifications.tasks.send_mail')
#     @patch('celery.Celery.connection')
#     def test_send_attendance_reminder(self, mock_connection, mock_send_mail):
#         """Test that the Celery task is triggered correctly."""
#         # Mock Redis connection to prevent actual network interaction
#         mock_connection.return_value = True
#
#         # Call the task asynchronously
#         result = send_attendance_reminder.delay()  # Use delay() to run the task asynchronously
#
#         # Wait for the task to finish
#         result.get(timeout=10)  # Timeout to prevent the test from hanging indefinitely
#
#         # Check if the task was successful and completed
#         self.assertTrue(result.ready())
#
#         # Assert that the send_mail method was called once
#         mock_send_mail.assert_called_once()
#
#         # Optionally, check the email parameters to ensure it's sending to the correct address
#         args, kwargs = mock_send_mail.call_args
#         self.assertIn('Hi', args[1])  # Checking the body of the email
#         self.assertIn('Please remember to mark your attendance', args[1])  # Specific message check
#         self.assertTrue(kwargs['recipient_list'])  # Ensure recipient list is not empty
