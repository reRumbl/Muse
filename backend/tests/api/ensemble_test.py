import pytest
from httpx import AsyncClient


@pytest.mark.asyncio
async def test_get_ensemble_compositions_count(test_async_client: AsyncClient):
    # Случай 1: У нового ансамбля нет произведений
    ensemble_data = {'name': 'Test Ensemble 1', 'type': 'group'}
    response = await test_async_client.post('/ensembles/', json=ensemble_data)
    assert response.status_code == 200
    ensemble_id = response.json()['id']

    response = await test_async_client.get(f'/ensembles/{ensemble_id}/compositions/count')
    assert response.status_code == 200
    assert response.json()['count'] == 0

    # Случай 2: Одно произведение
    # Подготовка: создаем композитора, произведение и исполнение
    composer_data = {'name': 'Test', 'surname': 'Composer', 'type': 'composer'}
    response = await test_async_client.post('/musicians/', json=composer_data)
    assert response.status_code == 200
    composer_id = response.json()['id']

    composition_data = {'title': 'Test Composition 1', 'composer_id': composer_id}
    response = await test_async_client.post('/compositions/', json=composition_data)
    assert response.status_code == 200
    composition_id = response.json()['id']

    performance_data = {'composition_id': composition_id, 'ensemble_id': ensemble_id}
    response = await test_async_client.post('/performances/', json=performance_data)
    assert response.status_code == 200

    # Тест: получаем количество
    response = await test_async_client.get(f'/ensembles/{ensemble_id}/compositions/count')
    assert response.status_code == 200
    assert response.json()['count'] == 1

    # Случай 3: Два разных произведения
    composition_2_data = {'title': 'Test Composition 2', 'composer_id': composer_id}
    response = await test_async_client.post('/compositions/', json=composition_2_data)
    assert response.status_code == 200
    composition_2_id = response.json()['id']

    performance_2_data = {
        'composition_id': composition_2_id,
        'ensemble_id': ensemble_id,
    }
    response = await test_async_client.post('/performances/', json=performance_2_data)
    assert response.status_code == 200

    # Тест: получаем количество
    response = await test_async_client.get(f'/ensembles/{ensemble_id}/compositions/count')
    assert response.status_code == 200
    assert response.json()['count'] == 2

    # Случай 4: Несколько исполнений одного и того же произведения не должны увеличивать счетчик
    performance_3_data = {
        'composition_id': composition_id,
        'ensemble_id': ensemble_id,
    }
    response = await test_async_client.post('/performances/', json=performance_3_data)
    assert response.status_code == 200

    # Тест: получаем количество
    response = await test_async_client.get(f'/ensembles/{ensemble_id}/compositions/count')
    assert response.status_code == 200
    assert response.json()['count'] == 2
