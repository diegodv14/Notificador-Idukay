from src.web.domain.interfaces.notification_repository import INotificationRepository

class NotificationRepository(INotificationRepository):
    def __init__(self):
        super().__init__()
        
    def send_notification(self, user_id: str, message: str) -> bool:
        """Send a notification to a user."""
        try:
            # Simulate sending a notification
            print(f"Sending notification to user {user_id}: {message}")
            # Here you would implement the actual logic to send the notification
            return True
        except Exception as e:
            print(f"Failed to send notification: {e}")
            return False