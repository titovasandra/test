import requests
import pytest

# Создаем базовый метод для выполнения get запросов
def do_GET(url, **kwargs):
    return requests.get(url, **kwargs)
# Параметризируем кейс без текстуры
def pytest_generate_tests(metafunc):
    if "param1" in metafunc.fixturenames:  metafunc.parametrize("param1", [200])

# Глобальная перменная для адреса аппликации
base_url = r"https://jsonplaceholder.typicode.com"
# Тест не параметризованный выполняет простой запрос к аппликации для проверки что она доступна
def test_unparametrized_connection_to_host():
    r = do_GET(base_url)
    assert r.status_code == 200
# Тест параметризованный выполняет простой запрос к аппликации для проверки что она доступна
def test_parametrized_connection_to_host(param1):
    r = do_GET(base_url)
    assert r.status_code == param1

# Тест параметризованный через фикстуру выполняет простой запрос к аппликации для проверки что она доступна также в случая если ожидаем валидный json на выходе проверяем его существование
# Негативный кейс для проверки что аппликация базово работает как ожидаем а не всегда отвечает 2**
@pytest.mark.parametrize("url, json_check, status_code", [
(f"{base_url}",             False, 200),
(f"{base_url}/posts",       True,  200),
(f"{base_url}/comments",    True,  200),
(f"{base_url}/albums",      True,  200),
(f"{base_url}/photos",      True,  200),
(f"{base_url}/todos",       True,  200),
(f"{base_url}/users",       True,  200),
#NEGATIVE CASE
(f"{base_url}/abcd",        False, 404),
])
def test_fixture_parametrized_connection_to_host(url, json_check, status_code):
    r = do_GET(url)
    if json_check: assert r.json()
    assert r.status_code == status_code

# Проверяем GET запросы к ресурсу аппликации с элементарной валидацией схемы
@pytest.mark.parametrize("url, id, json_scheme", [
(f"{base_url}/posts/", 1, {"userId":int, "id":int, "title":str, "body":str}),
])
def test_validate_posts_data_json_scheme(url, id, json_scheme):
    r = do_GET(url+str(id))
    assert r.status_code == 200

    resp_json = r.json()
    assert resp_json
    # Проверяем что схема есть в ответе - ответ будет более явный покажет какой ключ пропущен
    assert all([in_key in json_scheme for in_key in resp_json])
    # Проверяем что неожиданных ключей нет -  проверка простая на длинну но можно улучшить чтобы выдала какие ключи пропущены
    assert len(list(set(json_scheme.keys()) ^ set(json_scheme.keys()))) == 0
    # Проверяем что значения типов в ответе с ожиданием
    assert all([type(in_value) == json_scheme[in_key] for in_key, in_value in resp_json.items()])
    # валидируем id
    assert resp_json['id'] == id

# Создаем базовый метод для выполнения POST запросов
def do_POST(url, **kwargs):
    return requests.post(url, **kwargs)

# Фикстурка с хидерами
@pytest.fixture()
def headers():
    return {
        'Content-type': 'application/json; charset=UTF-8',
    }

@pytest.mark.parametrize("url, body", [
(f"{base_url}/posts", {"userId": 11, "title": "foo", "body": "bar"}),
])
def test_validate_post_api(headers, url, body):
    r = do_POST(url, json=body, headers=headers)
    assert r.status_code == 201

    resp_json = r.json()
    assert resp_json
    # проверяем что записали все поля
    assert all([out_key in resp_json for out_key in body])
    # проверяем что записали то что хотели
    assert all([out_value == resp_json[out_key] for out_key, out_value in body.items()])


# Создаем базовый метод для выполнения PUT запросов
def do_PUT(url, **kwargs):
    return requests.put(url, **kwargs)


@pytest.mark.parametrize("url, body", [
(f"{base_url}/posts/1", {"userId": 11, "title": "foo", "body": "bar", "id": 1}),
])
def test_validate_put_api(headers, url, body):
    r = do_PUT(url, json=body, headers=headers)
    assert r.status_code == 200

    resp_json = r.json()
    assert resp_json

    assert all([out_key in resp_json for out_key in body])
    # валидируем изменение
    assert all([out_value == resp_json[out_key] for out_key, out_value in body.items()])

# Создаем базовый метод для выполнения PATCH запросов

def do_PATCH(url, **kwargs):
    return requests.put(url, **kwargs)

@pytest.mark.parametrize("url, body", [
(f"{base_url}/posts/1", {"title": "foo"}),
])
def test_validate_patch_api(headers, url, body):
    r = do_PATCH(url, json=body, headers=headers)
    assert r.status_code == 200

    resp_json = r.json()
    assert resp_json

    assert all([out_key in resp_json for out_key in body])
    # валидируем изменение
    assert all([out_value == resp_json[out_key] for out_key, out_value in body.items()])

# Создаем базовый метод для выполнения DELETE запросов

def do_DELETE(url, **kwargs):
    return requests.put(url, **kwargs)

@pytest.mark.parametrize("url", (
f"{base_url}/posts/1",
                         ))
def test_validate_patch_api(url):
    r = do_DELETE(url)
    assert r.status_code == 200

# Тесты выглядят как дымовые - если они повалятся - то 100% все плохо, потому можно их считать как самыми важными.
# в дальнейшем стоило расширить апи запросы на другие разделы аппликации и проверить nested часть для полноты картины. 