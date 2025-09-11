from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker
from src.ensemble.models import EnsembleModel, EnsembleMemberModel
from src.ensemble.schemas import EnsembleCreate, EnsembleUpdate, Ensemble
from src.composition.models import CompositionModel
from src.composition.schemas import Composition
from src.performance.models import PerformanceModel


class EnsembleService:
    def __init__(self, session_factory: async_sessionmaker[AsyncSession]):
        self.session_factory = session_factory
    
    async def create(self, ensemble_data: EnsembleCreate) -> Ensemble:
        async with self.session_factory() as session:
            ensemble_db = EnsembleModel(**ensemble_data.model_dump())
            session.add(ensemble_db)
            await session.commit()
            await session.refresh(ensemble_db)
            ensemble_schema = Ensemble.model_validate(ensemble_db)
            return ensemble_schema
    
    async def get(self, ensemble_id: UUID) -> Ensemble:
        async with self.session_factory() as session:
            ensemble_db = await session.get(EnsembleModel, ensemble_id)
            ensemble_schema = Ensemble.model_validate(ensemble_db)
            return ensemble_schema
    
    async def get_all_compositions(self, ensemble_id: UUID) -> list[Composition]:
        async with self.session_factory() as session:
            query = (
                select(CompositionModel)
                .join(
                    PerformanceModel,
                    PerformanceModel.composition_id == CompositionModel.id
                )
                .where(PerformanceModel.ensemble_id == ensemble_id)
                .distinct()
            )
            result = await session.execute(query)
            compositions_db = result.scalars().all()
            return [Composition.model_validate(c) for c in compositions_db]
    
    async def update(self, ensemble_id: UUID, ensemble_data: EnsembleUpdate) -> Ensemble:
        async with self.session_factory() as session:
            ensemble_db = await session.get(EnsembleModel, ensemble_id)
            
            for key, value in ensemble_data.model_dump(exclude_unset=True).items():
                setattr(ensemble_db, key, value)
                
            await session.commit()
            await session.refresh(ensemble_db)
            ensemble_schema = Ensemble.model_validate(ensemble_db)
            return ensemble_schema
    
    async def delete(self, ensemble_id: UUID):
        async with self.session_factory() as session:
            ensemble_db = await session.get(EnsembleModel, ensemble_id)
            await session.delete(ensemble_db)
            await session.commit()
            
    async def add_member_to_ensemble(self, musician_id: UUID, ensemble_id: UUID) -> None:
        async with self.session_factory() as session:
            ensemble_member_db = EnsembleMemberModel(
                musician_id=musician_id,
                ensemble_id=ensemble_id
            )
            session.add(ensemble_member_db)
            await session.commit()
            await session.refresh(ensemble_member_db)
