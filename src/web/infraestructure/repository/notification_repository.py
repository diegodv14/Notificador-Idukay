import os
from typing import List
import requests
from src.web.domain.interfaces.notification_repository import INotificationRepository
import polars as pl

class NotificationRepository(INotificationRepository):
    def __init__(self):
        super().__init__()
        
    def send_notification(self, data: pl.DataFrame) -> bool:
        try:
            
            message: List[str] = []
            
            for row in data.iter_rows(named=True):
                    message.append(f"{row['Estudiante']} tiene una nota baja en {row['Materia']}: {row['Nota']}") 
        
            url = 'https://textbelt.com/text'
            data = {
                'phone': (os.getenv('NOTIFICATION_CELLPHONE')),
                'message': "\n".join(message),
                'key': (os.getenv("SMS_API_KEY")),
            }
            response = requests.post(url, data=data)
            return response.json()
        except Exception as e:
            print(f"Error enviando la notificacion al representante. {e}")
            return False