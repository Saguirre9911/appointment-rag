from abc import ABC, abstractmethod
from datetime import datetime
from typing import List, Optional

from langchain.docstore.document import Document
from langchain.vectorstores import Qdrant

from domain.appointment import Appointment


class AppointmentRepository(ABC):
    @abstractmethod
    def add(self, appointment: Appointment) -> None:
        """Agrega o actualiza una cita en el almacenamiento."""
        pass

    @abstractmethod
    def get(self, appointment_id: str) -> Optional[Appointment]:
        """Recupera una cita por su ID."""
        pass

    @abstractmethod
    def list_all(self) -> List[Appointment]:
        """Lista todas las citas almacenadas."""
        pass


class LangChainAppointmentRepository(AppointmentRepository):
    """
    Implementación de AppointmentRepository usando LangChain + Qdrant.
    """

    def __init__(self, vectorstore: Qdrant):
        """
        vectorstore: instancia de LangChain Qdrant configurada con los embeddings pertinentes.
        """
        self.vectorstore = vectorstore

    def add(self, appointment: Appointment) -> None:
        # Mapea Appointment a Document
        text = appointment.title + (" " + appointment.notes if appointment.notes else "")
        metadata = appointment.to_dict()
        doc = Document(page_content=text, metadata=metadata)
        # Upsert usando LangChain
        self.vectorstore.add_documents([doc])

    def get(self, appointment_id: str) -> Optional[Appointment]:
        # Recupera usando scroll con filtro por metadata id
        client = self.vectorstore._client
        collection = self.vectorstore.collection_name
        scroll_resp = client.scroll(
            collection_name=collection,
            filter={
                "must": [
                    {"key": "id", "match": {"value": appointment_id}}
                ]
            },
            limit=1
        )
        if not scroll_resp.points:
            return None
        payload = scroll_resp.points[0].payload
        return Appointment(
            id=payload["id"],
            user_id=payload["user_id"],
            title=payload["title"],
            datetime=datetime.fromisoformat(payload["datetime"]),
            notes=payload.get("notes", "")
        )

    def list_all(self) -> List[Appointment]:
        # Recupera todos los puntos en la colección
        client = self.vectorstore._client
        collection = self.vectorstore.collection_name
        scroll_resp = client.scroll(
            collection_name=collection,
            limit=1000
        )
        appointments: List[Appointment] = []
        for point in scroll_resp.points:
            payload = point.payload
            appointments.append(
                Appointment(
                    id=payload["id"],
                    user_id=payload["user_id"],
                    title=payload["title"],
                    datetime=datetime.fromisoformat(payload["datetime"]),
                    notes=payload.get("notes", "")
                )
            )
        return appointments
