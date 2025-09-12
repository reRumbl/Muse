import pytest
from httpx import AsyncClient
from tests.conftest import (
    test_async_client, create_company_factory, create_composition_factory,
    create_musician_factory,create_ensemble_factory, create_performance_factory, 
    add_record_to_performance_factory, create_record_factory
)


class TestRecord:
    @pytest.mark.asyncio
    async def test_create_and_update_record(
        self,
        test_async_client: AsyncClient,
        create_company_factory
    ):
        company = await create_company_factory()
        
        # --- Тест создания записи ---
        create_data = {
            'title': 'Test Record',
            'manufacturer_id': str(company.id)
        }
        
        response_create = await test_async_client.post('/records/', json=create_data)
        assert response_create.status_code == 200
        created_record = response_create.json()
        assert created_record['title'] == 'Test Record'
        assert created_record['manufacturer_id'] == str(company.id)
        record_id = created_record['id']

        # --- Тест обновления записи ---
        update_data = {
            'title': 'Updated Record Title'
        }
        
        response_update = await test_async_client.put(f'/records/{record_id}/update', json=update_data)
        assert response_update.status_code == 200
        updated_record = response_update.json()
        assert updated_record['title'] == 'Updated Record Title'
        
        # --- Проверка, что данные действительно обновились ---
        response_get = await test_async_client.get(f'/records/{record_id}')
        assert response_get.status_code == 200
        assert response_get.json()['title'] == 'Updated Record Title'
    
    @pytest.mark.asyncio
    async def test_get_top_selling_records(
        self,
        test_async_client: AsyncClient,
        create_company_factory,
        create_record_factory,
        create_release_factory
    ):
        # --- Сценарий 1: Нет записей, возвращается пустой список ---
        response_this_year = await test_async_client.get('/records/top-selling/this-year')
        assert response_this_year.status_code == 200
        assert response_this_year.json() == []

        response_last_year = await test_async_client.get('/records/top-selling/last-year')
        assert response_last_year.status_code == 200
        assert response_last_year.json() == []

        # --- Сценарий 2: Создание записей и релизов с разными продажами ---
        company = await create_company_factory()
        
        # Запись 1: больше продаж в этом году
        record = await create_record_factory(company.id, title='Record 1')
        await create_release_factory(record.id, company.id, this_year_sold=200, last_year_sold=50)

        # Запись 2: больше продаж в прошлом году
        record_2 = await create_record_factory(company.id, title='Record 2')
        await create_release_factory(record_2.id, company.id, this_year_sold=50, last_year_sold=200)

        # Запись 3: средние продажи
        record_3 = await create_record_factory(company.id, title='Record 3')
        await create_release_factory(record_3.id, company.id, this_year_sold=125, last_year_sold=125)

        # --- Тестирование эндпоинта 'this-year' ---
        response_this_year = await test_async_client.get('/records/top-selling/this-year')
        assert response_this_year.status_code == 200
        data_this_year = response_this_year.json()
        assert len(data_this_year) == 3
        # Проверка порядка: record1 (200), record3 (125), record2 (50)
        ids_this_year = [rec['id'] for rec in data_this_year]
        assert ids_this_year == [str(record.id), str(record_3.id), str(record_2.id)]

        # --- Тестирование эндпоинта 'last-year' ---
        response_last_year = await test_async_client.get('/records/top-selling/last-year')
        assert response_last_year.status_code == 200
        data_last_year = response_last_year.json()
        assert len(data_last_year) == 3
        # Проверка порядка: record2 (200), record3 (125), record1 (50)
        ids_last_year = [rec['id'] for rec in data_last_year]
        assert ids_last_year == [str(record_2.id), str(record_3.id), str(record.id)]

        # --- Сценарий 3: Тестирование параметра `limit` ---
        response_limit = await test_async_client.get('/records/top-selling/this-year?limit=1')
        assert response_limit.status_code == 200
        data_limit = response_limit.json()
        assert len(data_limit) == 1
        assert data_limit[0]['id'] == str(record.id)

        # --- Сценарий 4: Запись без релиза не должна появляться в списке ---
        record_no_release = await create_record_factory(company.id, title='No Release Record')
        
        response_this_year_after_new = await test_async_client.get('/records/top-selling/this-year')
        assert response_this_year_after_new.status_code == 200
        data_after_new = response_this_year_after_new.json()
        assert len(data_after_new) == 3
        ids_after_new = [rec['id'] for rec in data_after_new]
        assert str(record_no_release.id) not in ids_after_new
