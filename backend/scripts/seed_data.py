import sys
import os
import asyncio

# Añade el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from app.database import AsyncSessionLocal, engine
from app.models import Base, User, Agent, Ticket, TicketMessage, AgentType, TicketState, Origin
import datetime

async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        try:
            # Crear usuarios
            users = [
                User(first_name="John", last_name="Doe", mail="john@example.com", username="johndoe", number="1234567890"),
                User(first_name="Jane", last_name="Smith", mail="jane@example.com", username="janesmith", number="0987654321"),
                User(first_name="Alice", last_name="Johnson", mail="alice@example.com", username="alicej", number="1122334455")
            ]
            db.add_all(users)
            await db.commit()

            # Crear agentes
            agents = [
                Agent(type=AgentType.human),
                Agent(type=AgentType.ia_agent)
            ]
            db.add_all(agents)
            await db.commit()

            # Crear tickets
            tickets = [
                Ticket(title="Problema con el login", state=TicketState.open, origin=Origin.email, user_id=users[0].id, agent_id=agents[0].id),
                Ticket(title="Consulta sobre facturación", state=TicketState.pending, origin=Origin.whatsapp, user_id=users[1].id, agent_id=agents[1].id),
                Ticket(title="Solicitud de nueva funcionalidad", state=TicketState.new, origin=Origin.email, user_id=users[2].id, agent_id=agents[0].id)
            ]
            db.add_all(tickets)
            await db.commit()

            # Crear mensajes de tickets
            ticket_messages = [
                TicketMessage(ticket_id=tickets[0].id, conversation="No puedo acceder a mi cuenta. ¿Pueden ayudarme?"),
                TicketMessage(ticket_id=tickets[0].id, conversation="Por supuesto, vamos a verificar su cuenta. ¿Puede proporcionarme su nombre de usuario?"),
                TicketMessage(ticket_id=tickets[1].id, conversation="Tengo una pregunta sobre mi última factura."),
                TicketMessage(ticket_id=tickets[1].id, conversation="Claro, estaré encantado de ayudarle con su consulta sobre la factura. ¿Puede proporcionar más detalles?"),
                TicketMessage(ticket_id=tickets[2].id, conversation="Me gustaría sugerir una nueva característica para la aplicación.")
            ]
            db.add_all(ticket_messages)
            await db.commit()

            print("Datos de muestra cargados exitosamente.")

        except Exception as e:
            print(f"Ocurrió un error al cargar los datos de muestra: {e}")
            await db.rollback()

if __name__ == "__main__":
    asyncio.run(seed_data())
