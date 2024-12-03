from sqlalchemy import Column, Integer, Text, ForeignKey, Boolean
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()


class SpyCat(Base):
    __tablename__ = 'spycat'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    breed = Column(Text)
    exp_years = Column(Integer)
    salary = Column(Integer)

    missions = relationship('Mission', back_populates='spycat')


class Target(Base):
    __tablename__ = 'target'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    country = Column(Text)
    notes = Column(Text)
    mission_id = Column(Integer, ForeignKey('mission.id'), nullable=False)
    is_completed = Column(Boolean, default=False)

    mission = relationship('Mission', back_populates='targets')


class Mission(Base):
    __tablename__ = 'mission'

    id = Column(Integer, primary_key=True)
    name = Column(Text)
    cat_id = Column(Integer, ForeignKey('spycat.id'), nullable=True)
    is_completed = Column(Boolean, default=False)

    spycat = relationship('SpyCat', back_populates='missions')
    targets = relationship('Target', back_populates='mission', cascade='all, delete, delete-orphan')


async def create_tables(engine):
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

