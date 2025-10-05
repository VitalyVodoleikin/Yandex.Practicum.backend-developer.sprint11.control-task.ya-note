# Задание

# В файле test_routes.py:
# + Главная страница доступна анонимному пользователю.
# + Аутентифицированному пользователю доступна страница со списком заметок notes/,
# страница успешного добавления заметки done/, страница добавления новой заметки add/.
# + Страницы отдельной заметки, удаления и редактирования заметки доступны только автору заметки.
# Если на эти страницы попытается зайти другой пользователь — вернётся ошибка 404.
# + При попытке перейти на страницу списка заметок, страницу успешного добавления записи,
# страницу добавления заметки, отдельной заметки, редактирования или удаления заметки анонимный
# пользователь перенаправляется на страницу логина.
# + Страницы регистрации пользователей, входа в учётную запись и выхода из
# неё доступны всем пользователям.


from django.contrib.auth.models import User
from django.urls import reverse
from django.test import TestCase, Client
from notes.models import Note


class RouteTests(TestCase):
    def setUp(self):
        # Создаём тестового пользователя
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        self.note = Note.objects.create(
            title='Test Note',
            text='Content of test note',
            author=self.user
        )

    def test_anonymous_access(self):
        # Проверка доступа анонимного пользователя к главной странице
        response = self.client.get(reverse('notes:home'))
        self.assertEqual(response.status_code, 200)

        # Проверка перенаправления на страницу логина для анонимного пользователя
        urls = [
            reverse('notes:list'),
            reverse('notes:success'),
            reverse('notes:add'),
            reverse('notes:detail', args=[self.note.id]),
            reverse('notes:edit', args=[self.note.id]),
            reverse('notes:delete', args=[self.note.id]),
        ]
        for url in urls:
            login_url = reverse('users:login')
            response = self.client.get(url)
            self.assertRedirects(response, f'{login_url}?next={url}')

    def test_authenticated_access(self):
        # Авторизуем пользователя
        self.client.login(username='testuser', password='testpassword')

        # Проверяем доступ к основным страницам
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('notes:success'))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)

        # Проверяем доступ к странице своей заметки
        response = self.client.get(reverse('notes:detail', args=[self.note.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('notes:edit', args=[self.note.slug]))
        self.assertEqual(response.status_code, 200)

        response = self.client.get(reverse('notes:delete', args=[self.note.slug]))
        self.assertEqual(response.status_code, 200)

    def test_public_pages(self):
        # Проверяем доступность публичных страниц для всех пользователей
        public_urls = [
            reverse('users:signup'),
            reverse('users:login'),
            reverse('users:logout'),
        ]
        for url in public_urls:
            if url == reverse('users:logout'):
                response = self.client.post(url)
            else:
                response = self.client.get(url)
            self.assertEqual(response.status_code, 200)







# ==========


# ---------->>>>>>>>>>

    # def test_unauthorized_access_to_note(self):
    #     # Создаём второго пользователя
    #     other_user = User.objects.create_user(
    #         username='otheruser',
    #         password='otherpassword'
    #     )
    #     self.client.login(username=other_user.username, password=other_user.password)

    #     # Проверяем, что другой пользователь получает 404 при доступе к чужой заметке
    #     response = self.client.get(reverse('notes:detail', args=[self.note.slug]))
    #     self.assertEqual(response.status_code, 404)

    #     response = self.client.get(reverse('notes:edit', args=[self.note.slug]))
    #     self.assertEqual(response.status_code, 404)

    #     response = self.client.get(reverse('notes:delete', args=[self.note.slug]))
    #     self.assertEqual(response.status_code, 404)


# if __name__ == '__main__':
#     unittest.main()

# <<<<<<<<<<----------


# ==========


# ---------->>>>>>>>>>

# from http import HTTPStatus
# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from notes.models import Note

# User = get_user_model()


# class TestRoutes(TestCase):

#     @classmethod
#     def setUpTestData(cls):
#         cls.author = User.objects.create(username='Автор заметки')
#         cls.reader = User.objects.create(username='Посторонний пользователь')
#         cls.note = Note.objects.create(
#             title='Заметка',
#             text='Текст заметки',
#             slug='zametka',
#             author=cls.author,
#         )

#     def test_availability_for_note_edit_and_delete(self):
#         """Тест доступности страниц редактирования и удаления заметки."""
#         users_statuses = (
#             (self.author, HTTPStatus.OK),
#             (self.reader, HTTPStatus.NOT_FOUND),
#         )
#         for user, status in users_statuses:
#             self.client.force_login(user)
#             for name in ('notes:edit', 'notes:delete'):  
#                 with self.subTest(user=user, name=name):        
#                     url = reverse(name, args=(self.note.slug,))
#                     response = self.client.get(url)
#                     self.assertEqual(response.status_code, status)

#     def test_redirect_for_anonymous_client(self):
#         """Тест перенаправления на страницу авторизации."""
#         login_url = reverse('users:login')
#         for name in ('notes:edit', 'notes:delete'):
#             with self.subTest(name=name):
#                 url = reverse(name, args=(self.note.slug,))
#                 redirect_url = f'{login_url}?next={url}'
#                 response = self.client.get(url)
#                 self.assertRedirects(response, redirect_url)

# <<<<<<<<<<----------
