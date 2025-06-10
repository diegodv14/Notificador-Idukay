import os
from typing import List
import requests
from src.web.domain.interfaces.notification_repository import INotificationRepository
import polars as pl
import os
import requests
import polars as pl
from typing import List

class NotificationRepository(INotificationRepository):
    def __init__(self):
        super().__init__()

    def send_notification(self, data: pl.DataFrame) -> bool:
        try:
            message: List[str] = []
            if not data.is_empty():
                for row in data.iter_rows(named=True):
                    message.append(f"{row['Estudiante']} tiene una nota baja en {row['Materia']}: {row['Nota']}") 
            
                cellphone = os.getenv("NOTIFICATION_CELLPHONE")
                api_key = os.getenv("SMS_API_KEY")

                if not cellphone or not api_key:
                    print("Celular o API Key no configurados.")
                    return False
                message = "\n".join(message[:2])
                
            else:
                message = "Las niñas no tienen malas notas."

            payload = {
                'phone': cellphone,
                'message': message,
                'key': api_key,
            }

            response = requests.post('https://textbelt.com/text', data=payload)
            response_data = response.json()

            if response_data.get("success"):
                print("Notificación enviada correctamente al representante.")
                return True
            else:
                print(f"Fallo al enviar la notificación: {response_data}")
                return False

        except Exception as e:
            print(f"Error enviando la notificación al representante: {e}")
            return False
