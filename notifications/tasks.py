from celery import shared_task

@shared_task
def send_email_notification(email, subject, message):
    # Example email-sending task
    print(f"Sending email to {email} with subject '{subject}'")
