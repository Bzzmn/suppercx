import sys
import os
import asyncio
from sqlalchemy import delete

# Añade el directorio padre al path de Python
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from app.database import AsyncSessionLocal, engine
from app.models import (
    Base,
    User,
    Agent,
    Ticket,
    TicketMessage,
    AgentType,
    TicketState,
    Origin,
)
import datetime


async def get_or_create_user(db: AsyncSession, **kwargs):
    result = await db.execute(select(User).filter_by(mail=kwargs['mail']))
    user = result.scalars().first()
    if not user:
        user = User(**kwargs)
        db.add(user)
        await db.flush()
    return user


async def seed_data():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    async with AsyncSessionLocal() as db:
        try:
            # Crear o obtener usuarios
            users = [
                await get_or_create_user(db,
                    first_name="John",
                    last_name="Doe",
                    mail="john@example.com",
                    username="johndoe",
                    number="1234567890",
                ),
                await get_or_create_user(db,
                    first_name="Jane",
                    last_name="Smith",
                    mail="jane@example.com",
                    username="janesmith",
                    number="0987654321",
                ),
                await get_or_create_user(db,
                    first_name="Alice",
                    last_name="Johnson",
                    mail="alice@example.com",
                    username="alicej",
                    number="1122334455",
                ),
            ]

            # Crear agentes si no existen
            result = await db.execute(select(Agent))
            existing_agents = result.scalars().all()
            if not existing_agents:
                agents = [Agent(type=AgentType.human), Agent(type=AgentType.ia_agent)]
                db.add_all(agents)
                await db.flush()
            else:
                agents = existing_agents

            # Eliminar tickets y mensajes existentes
            await db.execute(delete(TicketMessage))
            await db.execute(delete(Ticket))
            await db.flush()

            # Crear nuevos tickets
            tickets = [
                Ticket(
                    title="Problema con el login",
                    description="El usuario no puede acceder a su cuenta. Necesita asistencia para recuperar el acceso.",
                    original_language="Spanish",
                    state=TicketState.open,
                    origin=Origin.email,
                    user_id=users[0].id,
                    agent_id=agents[0].id,
                ),
                Ticket(
                    title="Consulta sobre facturación",
                    description="El usuario tiene preguntas sobre los cargos en su última factura y necesita una explicación detallada.",
                    original_language="Spanish",
                    state=TicketState.pending,
                    origin=Origin.whatsapp,
                    user_id=users[1].id,
                    agent_id=agents[1].id,
                ),
                Ticket(
                    title="Solicitud de nueva funcionalidad",
                    description="El usuario sugiere implementar una función de chat en tiempo real en la aplicación para mejorar la comunicación.",
                    original_language="Spanish",
                    state=TicketState.new,
                    origin=Origin.email,
                    user_id=users[2].id,
                    agent_id=agents[0].id,
                ),
            ]
            db.add_all(tickets)
            await db.flush()

            # Crear nuevos mensajes de tickets
            ticket_messages = [
                TicketMessage(
                    ticket_id=tickets[0].id,
                    sender="John Doe",
                    email="john@example.com",
                    body="No puedo acceder a mi cuenta. ¿Pueden ayudarme?",
                    sent_date_time=datetime.datetime.utcnow(),
                ),
                TicketMessage(
                    ticket_id=tickets[0].id,
                    sender="Support Agent",
                    email="support@example.com",
                    body="Por supuesto, vamos a verificar su cuenta. ¿Puede proporcionarme su nombre de usuario?",
                    sent_date_time=datetime.datetime.utcnow(),
                ),
                TicketMessage(
                    ticket_id=tickets[1].id,
                    sender="Jane Smith",
                    email="jane@example.com",
                    body="Tengo una pregunta sobre mi última factura.",
                    sent_date_time=datetime.datetime.utcnow(),
                ),
                TicketMessage(
                    ticket_id=tickets[1].id,
                    sender="Billing Support",
                    email="billing@example.com",
                    body="Claro, estaré encantado de ayudarle con su consulta sobre la factura. ¿Puede proporcionar más detalles?",
                    sent_date_time=datetime.datetime.utcnow(),
                ),
                TicketMessage(
                    ticket_id=tickets[2].id,
                    sender="Alice Johnson",
                    email="alice@example.com",
                    body="Me gustaría sugerir una nueva característica para la aplicación.",
                    sent_date_time=datetime.datetime.utcnow(),
                ),
            ]
            db.add_all(ticket_messages)

            await db.commit()
            print("Datos de muestra cargados exitosamente.")

        except Exception as e:
            print(f"Ocurrió un error al cargar los datos de muestra: {e}")
            await db.rollback()


if __name__ == "__main__":
    asyncio.run(seed_data())
