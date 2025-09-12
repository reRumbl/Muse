import pytest
from httpx import AsyncClient
from tests.conftest import (
    test_async_client, create_company_factory, create_composition_factory,
    create_musician_factory,create_ensemble_factory, create_performance_factory, 
    add_record_to_performance_factory, create_record_factory
)


class TestEnsemble:
    @pytest.mark.asyncio
    async def test_create_ensemble(self, test_async_client: AsyncClient):
        ensemble_data = {
            'name': 'Test Ensamble',
            'type': 'group'
        }
        
        response = await test_async_client.post('/ensembles/', json=ensemble_data)
        
        assert response.status_code == 200
        created_ensemble = response.json()
        assert created_ensemble['name'] == 'Test Ensamble'
        assert created_ensemble['type'] == 'group'
        assert 'id' in created_ensemble
    
    @pytest.mark.asyncio
    async def test_get_ensemble_compositions_count(
        self,
        test_async_client: AsyncClient,
        create_composition_factory,
        create_ensemble_factory,
        create_musician_factory,
        create_performance_factory
    ):
        # --- Сценарий 1: У нового ансамбля нет произведений ---
        ensemble = await create_ensemble_factory()

        response = await test_async_client.get(f'/ensembles/{ensemble.id}/compositions/count')
        assert response.status_code == 200
        assert response.json()['count'] == 0

        # --- Сценарий 2: Одно произведение ---
        composer = await create_musician_factory()
        composition = await create_composition_factory(composer.id)
        performance = await create_performance_factory(composition.id, ensemble.id)

        response = await test_async_client.get(f'/ensembles/{ensemble.id}/compositions/count')
        assert response.status_code == 200
        assert response.json()['count'] == 1

        # --- Сценарий 3: Два разных произведения ---
        composition_2 = await create_composition_factory(composer.id)
        performance_2 = await create_performance_factory(composition_2.id, ensemble.id)

        response = await test_async_client.get(f'/ensembles/{ensemble.id}/compositions/count')
        assert response.status_code == 200
        assert response.json()['count'] == 2

        # --- Сценарий 4: Несколько исполнений одного и того же произведения не должны увеличивать счетчик ---
        performance_3 = await create_performance_factory(composition_2.id, ensemble.id)

        response = await test_async_client.get(f'/ensembles/{ensemble.id}/compositions/count')
        assert response.status_code == 200
        assert response.json()['count'] == 2
        

    @pytest.mark.asyncio
    async def test_get_ensemble_records(
        self,
        test_async_client: AsyncClient,
        create_company_factory,
        create_composition_factory,
        create_ensemble_factory,
        create_musician_factory,
        create_performance_factory,
        add_record_to_performance_factory,
        create_record_factory
    ):
        # --- Сценарий 1: У нового ансамбля нет дисков ---
        ensemble = await create_ensemble_factory()
        
        response = await test_async_client.get(f'/ensembles/{ensemble.id}/records')
        assert response.status_code == 200
        assert response.json() == []
        
        # --- Сценарий 2: Один диск ---
        composer = await create_musician_factory()
        composition = await create_composition_factory(composer.id)
        performance = await create_performance_factory(composition.id, ensemble.id)
        company = await create_company_factory()
        record = await create_record_factory(company.id)
        await add_record_to_performance_factory(record.id, performance.id)
        
        response = await test_async_client.get(f'/ensembles/{ensemble.id}/records')
        assert response.status_code == 200
        ids = [rec['id'] for rec in response.json()]
        assert str(record.id) in ids
        
        # --- Сценарий 3: Два разных диска ---
        composition_2 = await create_composition_factory(composer.id)
        performance_2 = await create_performance_factory(composition_2.id, ensemble.id)
        record_2 = await create_record_factory(company.id)
        await add_record_to_performance_factory(record_2.id, performance_2.id)
        
        response = await test_async_client.get(f'/ensembles/{ensemble.id}/records')
        assert response.status_code == 200
        ids = [rec['id'] for rec in response.json()]
        assert str(record.id) in ids
        assert str(record_2.id) in ids
        
        # --- Сценарий 4: Добавление нового диска существующего произведения должно учитываться ---
        record_3 = await create_record_factory(company.id)
        await add_record_to_performance_factory(record_3.id, performance_2.id)
        
        response = await test_async_client.get(f'/ensembles/{ensemble.id}/records')
        assert response.status_code == 200
        ids = [rec['id'] for rec in response.json()]
        assert str(record.id) in ids
        assert str(record_2.id) in ids
        assert str(record_3.id) in ids
