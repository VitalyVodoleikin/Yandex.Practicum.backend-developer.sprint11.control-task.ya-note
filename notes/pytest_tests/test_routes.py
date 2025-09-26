# test_routes.py
from http import HTTPStatus
from pytest_lazy_fixtures import lf
import pytest
from pytest_django.asserts import assertRedirects
from django.urls import reverse





# ---------->
# Проверим, что анонимному пользователю доступна главная страница проекта.

# Указываем в фикстурах встроенный клиент.
def test_home_availability_for_anonymous_user(client):
    # Адрес страницы получаем через reverse():
    url = reverse('notes:home')
    response = client.get(url)
    assert response.status_code == HTTPStatus.OK
# <----------





# ---------->
# Внимательно читаем план тестирования: в пункте 5
# упоминается проверка доступности для всех
# пользователей страниц логина, логаута и регистрации.
# Если должно быть доступно всем, значит должно быть
# доступно и анонимному пользователю.
# Напишем один параметризованный тест, в котором
# объединим адреса, доступные для анонимных
# пользователей (добавьте проверку логаута самостоятельно).

# test_routes.py
@pytest.mark.parametrize(
    'name, method, expected_status',  # Имя параметра функции.
    # Значения, которые будут передаваться в name.
    [
        ('notes:home', 'get', HTTPStatus.OK),
        ('users:login', 'get', HTTPStatus.OK),
        ('users:signup', 'get', HTTPStatus.OK),
        ('users:logout', 'post', HTTPStatus.OK)
    ]
)
# Указываем имя изменяемого параметра в сигнатуре теста.
def test_pages_availability_for_anonymous_user(client, name, method, expected_status):
    """
    Тест проверяет доступность страниц для анонимного пользователя
    """
    url = reverse(name)  # Получаем ссылку на нужный адрес.
    # Используем соответствующий метод запроса
    if method == 'get':
        response = client.get(url)
    elif method == 'post':
        response = client.post(url)
    
    assert response.status_code == expected_status
# <----------





# ---------->
# Тестирование доступности страниц для авторизованного пользователя

# Теперь проверим доступность страницы со списком заметок, страницы
# добавления новой записи и страницы успешного добавления записей.
# Для этих проверок сами заметки не нужны: важно проверить лишь
# доступность страниц.

# Сначала перепишем тест доступности страниц для другой
# фикстуры — вместо admin_client укажем not_author_client.

@pytest.mark.parametrize(
    'name',
    ('notes:list', 'notes:add', 'notes:success')
)
def test_pages_availability_for_auth_user(not_author_client, name):
    """
    Тестирование доступности страниц для неавторизованного пользователя чужой заметки
    """
    url = reverse(name)
    response = not_author_client.get(url)
    assert response.status_code == HTTPStatus.OK

# Параметризуем тестирующую функцию:
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
def test_pages_availability_for_author(author_client, name, note):
    """
    Тестирование доступности страниц для авторизованного пользователя своей заметки
    """
    url = reverse(name, args=(note.slug,))
    response = author_client.get(url)
    assert response.status_code == HTTPStatus.OK
# <----------





# ---------->
# Следующий этап — проверить, что пользователю, залогиненному в
# клиенте not_author_client (не автору заметки), при запросе к
# страницам 'notes:detail', 'notes:edit' и 'notes:delete' возвращается
# ошибка 404.
# Набор страниц - тот же, что и в тесте test_pages_availability_for_author(),
# задача — та же: отправить запрос к странице и сравнить её ответ с
# ожидаемым (только на этот раз ожидаем ответ 404). 
# Получается, нужно параметризовать тест test_pages_availability_for_author()
# так, чтобы запросы можно было отправлять и от имени author_client, и от
# имени not_author_client — и проверять, что для одного клиента всегда
# приходит ответ 200, а для другого — всегда 404.

# Сформулируем задачу:
# - нужно перебрать три страницы;
# - к каждой из этих страниц отправить два запроса:
# - - один запрос отправить от имени автора заметки (это уже описано в тесте),
# - - второй запрос отправить от имени другого пользователя — не автора.
# После обращения к каждой странице нужно сравнить её ответ с ожидаемым: 
# - запрос от имени автора заметки всегда должен возвращать 200;
# - запрос от имени другого пользователя всегда должен возвращать 404.

# Добавляем к тесту ещё один декоратор parametrize; в его параметры
# нужно передать фикстуры-клиенты и ожидаемый код ответа для каждого клиента.
@pytest.mark.parametrize(
    # parametrized_client - название параметра, 
    # в который будут передаваться фикстуры;
    # Параметр expected_status - ожидаемый статус ответа.
    'parametrized_client, expected_status',
    # В кортеже с кортежами передаём значения для параметров:
    (
        (lf('not_author_client'), HTTPStatus.NOT_FOUND),
        (lf('author_client'), HTTPStatus.OK)
    ),
)
# Этот декоратор оставляем таким же, как в предыдущем тесте.
@pytest.mark.parametrize(
    'name',
    ('notes:detail', 'notes:edit', 'notes:delete'),
)
# В параметры теста добавляем имена parametrized_client и expected_status.
def test_pages_availability_for_different_users(
        parametrized_client, name, note, expected_status
):
    url = reverse(name, args=(note.slug,))
    # Делаем запрос от имени клиента parametrized_client:
    response = parametrized_client.get(url)
    # Ожидаем ответ страницы, указанный в expected_status:
    assert response.status_code == expected_status
# <----------





# ---------->
# Тестирование редиректов

@pytest.mark.parametrize(
    'name, args',
    (
        ('notes:detail', lf('slug_for_args')),
        ('notes:edit', lf('slug_for_args')),
        ('notes:delete', lf('slug_for_args')),
        ('notes:add', None),
        ('notes:success', None),
        ('notes:list', None),
    ),
)
# Передаём в тест анонимный клиент, name проверяемых страниц и args:
def test_redirects(client, name, args):
    login_url = reverse('users:login')
    # Теперь не надо писать никаких if и можно обойтись одним выражением.
    url = reverse(name, args=args)
    expected_url = f'{login_url}?next={url}'
    response = client.get(url)
    assertRedirects(response, expected_url)
# <----------
