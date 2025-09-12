from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.ensemble.models import EnsembleModel, EnsembleMemberModel
from src.ensemble.schemas import EnsembleCreate, EnsembleUpdate, Ensemble
from src.composition.models import CompositionModel
from src.composition.schemas import Composition
from src.performance.models import PerformanceModel
from src.record.models import RecordModel, RecordPerformanceModel
from src.record.schemas import Record


class EnsembleService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def create(self, ensemble_data: EnsembleCreate) -> Ensemble:
        ensemble_db = EnsembleModel(**ensemble_data.model_dump())
        self.session.add(ensemble_db)
        await self.session.commit()
        await self.session.refresh(ensemble_db)
        ensemble_schema = Ensemble.model_validate(ensemble_db)
        return ensemble_schema
    
    async def add_member_to_ensemble(self, musician_id: UUID, ensemble_id: UUID) -> None:
        ensemble_member_db = EnsembleMemberModel(
            musician_id=musician_id,
            ensemble_id=ensemble_id
        )
        self.session.add(ensemble_member_db)
        await self.session.commit()
        await self.session.refresh(ensemble_member_db)
    
    async def get(self, ensemble_id: UUID) -> Ensemble:
        ensemble_db = await self.session.get(EnsembleModel, ensemble_id)
        ensemble_schema = Ensemble.model_validate(ensemble_db)
        return ensemble_schema
    
    async def get_all_compositions(self, ensemble_id: UUID) -> list[Composition]:
        query = (
            select(CompositionModel)
            .join(
                PerformanceModel,
                PerformanceModel.composition_id == CompositionModel.id
            )
            .where(PerformanceModel.ensemble_id == ensemble_id)
            .distinct()
        )
        result = await self.session.execute(query)
        compositions_db = result.scalars().all()
        return [Composition.model_validate(c) for c in compositions_db]
    
    async def get_all_records(self, ensemble_id: UUID) -> list[Record]:
        query = (
            select(RecordModel)
            .join(RecordPerformanceModel, RecordModel.id == RecordPerformanceModel.record_id)
            .join(PerformanceModel, RecordPerformanceModel.performance_id == PerformanceModel.id)
            .where(PerformanceModel.ensemble_id == ensemble_id)
            .distinct()
        )
        result = await self.session.execute(query)
        records_db = result.scalars().all()
        return [Record.model_validate(r) for r in records_db]
        
    async def update(self, ensemble_id: UUID, ensemble_data: EnsembleUpdate) -> Ensemble:
        ensemble_db = await self.session.get(EnsembleModel, ensemble_id)
        
        for key, value in ensemble_data.model_dump(exclude_unset=True).items():
            setattr(ensemble_db, key, value)
            
        await self.session.commit()
        await self.session.refresh(ensemble_db)
        ensemble_schema = Ensemble.model_validate(ensemble_db)
        return ensemble_schema
    
    async def delete(self, ensemble_id: UUID):
        ensemble_db = await self.session.get(EnsembleModel, ensemble_id)
        await self.session.delete(ensemble_db)
        await self.session.commit()
