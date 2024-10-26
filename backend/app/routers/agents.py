from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from ..database import get_db
from ..models import Agent
from ..schemas import AgentCreate, AgentUpdate, AgentResponse
from typing import List

router = APIRouter()

@router.post("/", response_model=AgentResponse)
async def create_agent(agent: AgentCreate, db: AsyncSession = Depends(get_db)):
    db_agent = Agent(**agent.dict())
    db.add(db_agent)
    await db.commit()
    await db.refresh(db_agent)
    return db_agent

@router.get("/", response_model=List[AgentResponse])
async def read_agents(skip: int = 0, limit: int = 100, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).offset(skip).limit(limit))
    return result.scalars().all()

@router.get("/{agent_id}", response_model=AgentResponse)
async def read_agent(agent_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).filter(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    return agent

@router.put("/{agent_id}", response_model=AgentResponse)
async def update_agent(agent_id: int, agent: AgentUpdate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).filter(Agent.id == agent_id))
    db_agent = result.scalar_one_or_none()
    if db_agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    for key, value in agent.dict(exclude_unset=True).items():
        setattr(db_agent, key, value)
    
    await db.commit()
    await db.refresh(db_agent)
    return db_agent

@router.delete("/{agent_id}", response_model=AgentResponse)
async def delete_agent(agent_id: int, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(Agent).filter(Agent.id == agent_id))
    agent = result.scalar_one_or_none()
    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")
    await db.delete(agent)
    await db.commit()
    return agent