from datetime import date
from typing import List, Optional
from uuid import UUID, uuid4

from api.models import ApiEcoindex
from ecoindex.models import Result
from sqlalchemy import func
from sqlalchemy.sql.expression import asc
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from db.database import engine


async def save_ecoindex_result_db(
    session: AsyncSession, ecoindex_result: Result, version: Optional[int] = 1
) -> ApiEcoindex:
    db_ecoindex = ApiEcoindex(
        id=str(uuid4()),
        date=ecoindex_result.date,
        url=ecoindex_result.url,
        host=ecoindex_result.url.host,
        width=ecoindex_result.width,
        height=ecoindex_result.height,
        size=ecoindex_result.size,
        nodes=ecoindex_result.nodes,
        requests=ecoindex_result.requests,
        grade=ecoindex_result.grade,
        score=ecoindex_result.score,
        ges=ecoindex_result.ges,
        water=ecoindex_result.water,
        page_type=ecoindex_result.page_type,
        version=version,
    )
    session.add(db_ecoindex)
    await session.commit()
    await session.refresh(db_ecoindex)

    return db_ecoindex


async def get_ecoindex_result_list_db(
    session: AsyncSession,
    version: Optional[int] = 1,
    host: Optional[str] = None,
    date_from: Optional[date] = None,
    date_to: Optional[date] = None,
) -> List[ApiEcoindex]:
    statement = select(ApiEcoindex).where(ApiEcoindex.version == version)

    if host:
        statement = statement.where(ApiEcoindex.host == host)

    if date_from:
        statement = statement.where(ApiEcoindex.date >= date_from)

    if date_to:
        statement = statement.where(ApiEcoindex.date <= date_to)

    ecoindexes = await session.execute(statement.order_by(asc("date")))

    return ecoindexes.scalars().all()


async def get_ecoindex_result_by_id_db(
    session: AsyncSession, id: UUID, version: Optional[int] = 1
) -> ApiEcoindex:
    statement = (
        select(ApiEcoindex)
        .where(ApiEcoindex.id == id)
        .where(ApiEcoindex.version == version)
    )
    ecoindex = await session.execute(statement)

    return ecoindex.scalar_one_or_none()


async def get_host_list_db(
    session: AsyncSession, version: Optional[int] = 1, q: Optional[str] = None
) -> List[str]:
    statement = select(ApiEcoindex.host).where(ApiEcoindex.version == version)

    if q:
        statement = statement.filter(ApiEcoindex.host.like(f"%{q}%"))

    statement = statement.group_by(ApiEcoindex.host).order_by(ApiEcoindex.host)

    hosts = await session.execute(statement)

    return hosts.scalars().all()


async def get_count_daily_request_per_host(session: AsyncSession, host: str) -> int:
    statement = select(ApiEcoindex).where(
        func.date(ApiEcoindex.date) == date.today(), ApiEcoindex.host == host
    )
    results = await session.execute(statement)
    return len(results.all())
