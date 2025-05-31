from abc import ABC, abstractmethod

class INotificationRepository(ABC):
    @abstractmethod
    def send_notification(self,) -> bool:
        """Send a notification to a user."""
        pass