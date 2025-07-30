import os
from datetime import datetime, timedelta

from dotenv import load_dotenv

from domain.appointment import Appointment
from infrastructure.service_factory import ServiceFactory

# Carga variables de entorno
load_dotenv()

# 1) Obtén el repositorio desde la factory
repo = ServiceFactory.get_repository()

# 2) Crea una cita de ejemplo
appt = Appointment(
    id="test-1",
    user_id="whatsapp:+573001234567",
    title="Prueba de reunión",
    datetime=datetime.now() + timedelta(minutes=1),
    notes="Esta es una nota de prueba"
)

# 3) Agrégala (indexa)
repo.add(appt)
print("✅ Agregada cita:", appt.to_dict())

# 4) Recupérala por ID
fetched = repo.get("test-1")
print("🔍 Recuperada cita:", fetched.to_dict() if fetched else None)

# 5) Lista todas las citas (debería incluir la recién agregada)
all_appts = repo.list_all()
print(f"📋 Total citas en Qdrant: {len(all_appts)}")
for a in all_appts:
    print("  -", a.to_dict())
