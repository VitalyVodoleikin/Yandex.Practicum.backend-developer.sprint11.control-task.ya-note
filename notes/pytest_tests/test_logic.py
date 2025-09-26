# Тестирование логики приложения
# ----------

# В тестах надо отправить POST-запрос на создание
# заметки от имени залогиненного и анонимного
# пользователей; но дальнейшие проверки будут сильно отличаться:
# 1) залогиненного пользователя должно переадресовать
# на страницу успешного создания заметки; нужно
# проверить, что заметка добавлена в БД и что значения
# её полей соответствуют ожиданиям;
# 2) с анонимным пользователем всё иначе: после POST-запроса
# его должно переадресовать на страницу логина, а в базе не
# должно появиться новых заметок.
# В такой ситуации будет проще написать два отдельных теста.
# ----------


# test_logic.py
from pytest_django.asserts import assertRedirects

from django.urls import reverse

from notes.models import Note

import pytest

# Импортируем функции для проверки редиректа и ошибки формы:
from pytest_django.asserts import assertRedirects, assertFormError

# Импортируем из модуля forms сообщение об ошибке:
from notes.forms import WARNING


# # ---------->
# # Тест: залогиненного пользователя должно переадресовать
# # на страницу успешного создания заметки

# # Указываем фикстуру form_data в параметрах теста.
# def test_user_can_create_note(author_client, author, form_data):
#     url = reverse('notes:add')
#     # В POST-запросе отправляем данные, полученные из фикстуры form_data:
#     response = author_client.post(url, data=form_data)
#     # Проверяем, что был выполнен редирект на страницу успешного добавления заметки:
#     assertRedirects(response, reverse('notes:success'))
#     # Считаем общее количество заметок в БД, ожидаем 1 заметку.
#     assert Note.objects.count() == 1
#     # Чтобы проверить значения полей заметки - 
#     # получаем её из базы при помощи метода get():
#     new_note = Note.objects.get()
#     # Сверяем атрибуты объекта с ожидаемыми.
#     assert new_note.title == form_data['title']
#     assert new_note.text == form_data['text']
#     assert new_note.slug == form_data['slug']
#     assert new_note.author == author
#     # Вроде бы здесь нарушен принцип "один тест - одна проверка";
#     # но если хоть одна из этих проверок провалится - 
#     # весь тест можно признать провалившимся, а последующие невыполненные проверки
#     # не внесли бы в отчёт о тесте ничего принципиально важного.

# # Следующий тест — проверка утверждения «анонимный пользователь не может создать заметку».

# # Добавляем маркер, который обеспечит доступ к базе данных:
# @pytest.mark.django_db
# def test_anonymous_user_cant_create_note(client, form_data):
#     url = reverse('notes:add')
#     # Через анонимный клиент пытаемся создать заметку:
#     response = client.post(url, data=form_data)
#     login_url = reverse('users:login')
#     expected_url = f'{login_url}?next={url}'
#     # Проверяем, что произошла переадресация на страницу логина:
#     assertRedirects(response, expected_url)
#     # Считаем количество заметок в БД, ожидаем 0 заметок.
#     assert Note.objects.count() == 0
# # <----------





# # ---------->
# # Тестирование логики slug

# # Указываем фикстуру form_data в параметрах теста.
# def test_user_can_create_note(author_client, author, form_data):
#     url = reverse('notes:add')
#     # В POST-запросе отправляем данные, полученные из фикстуры form_data:
#     response = author_client.post(url, data=form_data)
#     # Проверяем, что был выполнен редирект на страницу успешного добавления заметки:
#     assertRedirects(response, reverse('notes:success'))
#     # Считаем общее количество заметок в БД, ожидаем 1 заметку.
#     assert Note.objects.count() == 1
#     # Чтобы проверить значения полей заметки - 
#     # получаем её из базы при помощи метода get():
#     new_note = Note.objects.get()
#     # Сверяем атрибуты объекта с ожидаемыми.
#     assert new_note.title == form_data['title']
#     assert new_note.text == form_data['text']
#     assert new_note.slug == form_data['slug']
#     assert new_note.author == author
#     # Вроде бы здесь нарушен принцип "один тест - одна проверка";
#     # но если хоть одна из этих проверок провалится - 
#     # весь тест можно признать провалившимся, а последующие невыполненные проверки
#     # не внесли бы в отчёт о тесте ничего принципиально важного.

# # Следующий тест — проверка утверждения «анонимный пользователь не может создать заметку».

# # Добавляем маркер, который обеспечит доступ к базе данных:
# @pytest.mark.django_db
# def test_anonymous_user_cant_create_note(client, form_data):
#     url = reverse('notes:add')
#     # Через анонимный клиент пытаемся создать заметку:
#     response = client.post(url, data=form_data)
#     login_url = reverse('users:login')
#     expected_url = f'{login_url}?next={url}'
#     # Проверяем, что произошла переадресация на страницу логина:
#     assertRedirects(response, expected_url)
#     # Считаем количество заметок в БД, ожидаем 0 заметок.
#     assert Note.objects.count() == 0


# # Вызываем фикстуру отдельной заметки, чтобы в базе появилась запись.
# def test_not_unique_slug(author_client, note, form_data):
#     url = reverse('notes:add')
#     # Подменяем slug новой заметки на slug уже существующей записи:
#     form_data['slug'] = note.slug
#     # Пытаемся создать новую заметку:
#     response = author_client.post(url, data=form_data)
#     # Проверяем, что в ответе содержится ошибка формы для поля slug:
#     assertFormError(response.context['form'], 'slug', errors=(note.slug + WARNING))
#     # Убеждаемся, что количество заметок в базе осталось равным 1:
#     assert Note.objects.count() == 1

# # Следующий тест: если при создании заметки оставить поле slug пустым — то
# # содержимое этого поля будет сформировано автоматически, из содержимого
# # поля title.

# # Дополнительно импортируем функцию slugify.
# from pytils.translit import slugify


# def test_empty_slug(author_client, form_data):
#     url = reverse('notes:add')
#     # Убираем поле slug из словаря:
#     form_data.pop('slug')
#     response = author_client.post(url, data=form_data)
#     # Проверяем, что даже без slug заметка была создана:
#     assertRedirects(response, reverse('notes:success'))
#     assert Note.objects.count() == 1
#     # Получаем созданную заметку из базы:
#     new_note = Note.objects.get()
#     # Формируем ожидаемый slug:
#     expected_slug = slugify(form_data['title'])
#     # Проверяем, что slug заметки соответствует ожидаемому:
#     assert new_note.slug == expected_slug
# # <----------





# ---------->
# Тестирование редактирования и удаления заметки

# Указываем фикстуру form_data в параметрах теста.
def test_user_can_create_note(author_client, author, form_data):
    url = reverse('notes:add')
    # В POST-запросе отправляем данные, полученные из фикстуры form_data:
    response = author_client.post(url, data=form_data)
    # Проверяем, что был выполнен редирект на страницу успешного добавления заметки:
    assertRedirects(response, reverse('notes:success'))
    # Считаем общее количество заметок в БД, ожидаем 1 заметку.
    assert Note.objects.count() == 1
    # Чтобы проверить значения полей заметки - 
    # получаем её из базы при помощи метода get():
    new_note = Note.objects.get()
    # Сверяем атрибуты объекта с ожидаемыми.
    assert new_note.title == form_data['title']
    assert new_note.text == form_data['text']
    assert new_note.slug == form_data['slug']
    assert new_note.author == author
    # Вроде бы здесь нарушен принцип "один тест - одна проверка";
    # но если хоть одна из этих проверок провалится - 
    # весь тест можно признать провалившимся, а последующие невыполненные проверки
    # не внесли бы в отчёт о тесте ничего принципиально важного.

# Следующий тест — проверка утверждения «анонимный пользователь не может создать заметку».

# Добавляем маркер, который обеспечит доступ к базе данных:
@pytest.mark.django_db
def test_anonymous_user_cant_create_note(client, form_data):
    url = reverse('notes:add')
    # Через анонимный клиент пытаемся создать заметку:
    response = client.post(url, data=form_data)
    login_url = reverse('users:login')
    expected_url = f'{login_url}?next={url}'
    # Проверяем, что произошла переадресация на страницу логина:
    assertRedirects(response, expected_url)
    # Считаем количество заметок в БД, ожидаем 0 заметок.
    assert Note.objects.count() == 0


# Вызываем фикстуру отдельной заметки, чтобы в базе появилась запись.
def test_not_unique_slug(author_client, note, form_data):
    url = reverse('notes:add')
    # Подменяем slug новой заметки на slug уже существующей записи:
    form_data['slug'] = note.slug
    # Пытаемся создать новую заметку:
    response = author_client.post(url, data=form_data)
    # Проверяем, что в ответе содержится ошибка формы для поля slug:
    assertFormError(response.context['form'], 'slug', errors=(note.slug + WARNING))
    # Убеждаемся, что количество заметок в базе осталось равным 1:
    assert Note.objects.count() == 1

# Следующий тест: если при создании заметки оставить поле slug пустым — то
# содержимое этого поля будет сформировано автоматически, из содержимого
# поля title.

# Дополнительно импортируем функцию slugify.
from pytils.translit import slugify


def test_empty_slug(author_client, form_data):
    url = reverse('notes:add')
    # Убираем поле slug из словаря:
    form_data.pop('slug')
    response = author_client.post(url, data=form_data)
    # Проверяем, что даже без slug заметка была создана:
    assertRedirects(response, reverse('notes:success'))
    assert Note.objects.count() == 1
    # Получаем созданную заметку из базы:
    new_note = Note.objects.get()
    # Формируем ожидаемый slug:
    expected_slug = slugify(form_data['title'])
    # Проверяем, что slug заметки соответствует ожидаемому:
    assert new_note.slug == expected_slug

# Проверим, что автор может редактировать заметку
# В параметрах вызвана фикстура note: значит, в БД создана заметка.
def test_author_can_edit_note(author_client, form_data, note):
    # Получаем адрес страницы редактирования заметки:
    url = reverse('notes:edit', args=(note.slug,))
    # В POST-запросе на адрес редактирования заметки
    # отправляем form_data - новые значения для полей заметки:
    response = author_client.post(url, form_data)
    # Проверяем редирект:
    assertRedirects(response, reverse('notes:success'))
    # Обновляем объект заметки note: получаем обновлённые данные из БД:
    note.refresh_from_db()
    # Проверяем, что атрибуты заметки соответствуют обновлённым:
    assert note.title == form_data['title']
    assert note.text == form_data['text']
    assert note.slug == form_data['slug']


# Подобным же образом проверяем, что зарегистрированный пользователь не может
# редактировать чужую заметку
# Допишите импорт класса со статусами HTTP-ответов.
from http import HTTPStatus


def test_other_user_cant_edit_note(not_author_client, form_data, note):
    url = reverse('notes:edit', args=(note.slug,))
    response = not_author_client.post(url, form_data)
    # Проверяем, что страница не найдена:
    assert response.status_code == HTTPStatus.NOT_FOUND
    # Получаем новый объект запросом из БД.
    note_from_db = Note.objects.get(id=note.id)
    # Проверяем, что атрибуты объекта из БД равны атрибутам заметки до запроса.
    assert note.title == note_from_db.title
    assert note.text == note_from_db.text
    assert note.slug == note_from_db.slug 


# Проверка удаления заметок очень похожа на предыдущие тесты.
# Добавьте эти тесты в файл test_logic.py и разберитесь с ними
# самостоятельно; запустите их и проверьте в работе.


def test_author_can_delete_note(author_client, slug_for_args):
    url = reverse('notes:delete', args=slug_for_args)
    response = author_client.post(url)
    assertRedirects(response, reverse('notes:success'))
    assert Note.objects.count() == 0


def test_other_user_cant_delete_note(not_author_client, slug_for_args):
    url = reverse('notes:delete', args=slug_for_args)
    response = not_author_client.post(url)
    assert response.status_code == HTTPStatus.NOT_FOUND
    assert Note.objects.count() == 1
# <----------
