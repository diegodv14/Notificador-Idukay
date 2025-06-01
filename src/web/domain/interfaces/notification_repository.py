from abc import ABC, abstractmethod
import polars as pl

class INotificationRepository(ABC):
    @abstractmethod
    def send_notification(self, data: pl) -> bool:
        """Send a notification to a the parent when the student have down grades."""
        pass