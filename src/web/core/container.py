from src.web.domain.interfaces.notification_repository import INotificationRepository
from src.web.infraestructure.repository.notification_repository import NotificationRepository

class Container:
    def notification_service(self) -> INotificationRepository:
        return NotificationRepository()
    
container = Container()
        