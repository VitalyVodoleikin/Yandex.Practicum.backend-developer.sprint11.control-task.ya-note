
# Задание

# В файле test_content.py:
# + отдельная заметка передаётся на страницу со списком заметок в списке object_list в словаре context;
# + в список заметок одного пользователя не попадают заметки другого пользователя;
# + на страницы создания и редактирования заметки передаются формы.


# import unittest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client, TestCase
from notes.models import Note


class ContentTests(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(
            username='testuser1',
            password='12345'
        )
        self.user2 = User.objects.create_user(
            username='testuser2',
            password='12345'
        )

        # Создаем тестовые заметки
        self.note1 = Note.objects.create(
            title='Note 1',
            text='Content 1',
            author=self.user1
        )
        self.note2 = Note.objects.create(
            title='Note 2',
            text='Content 2',
            author=self.user2
        )

        # Создаем клиент и авторизуем пользователя
        self.client = Client()
        self.client.force_login(self.user1)

    def test_note_in_list(self):
        """Проверка передачи заметки в context"""
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note1, response.context['object_list'])
        self.assertNotIn(self.note2, response.context['object_list'])

    def test_user_notes_isolation(self):
        """Проверка изоляции заметок разных пользователей"""
        # Проверяем заметки для первого пользователя
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.note1, response.context['object_list'])
        self.assertNotIn(self.note2, response.context['object_list'])

        # Авторизуем второго пользователя и проверяем
        self.client.force_login(self.user2)
        response = self.client.get(reverse('notes:list'))
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(self.note1, response.context['object_list'])
        self.assertIn(self.note2, response.context['object_list'])

    def test_form_in_create_view(self):
        """Проверка передачи формы на страницу создания заметки"""
        response = self.client.get(reverse('notes:add'))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])

    def test_form_in_edit_view(self):
        """Проверка передачи формы на страницу редактирования заметки"""
        response = self.client.get(reverse('notes:edit', args=[self.note1.slug]))
        self.assertEqual(response.status_code, 200)
        self.assertIsNotNone(response.context['form'])












# ---------->>>>>>>>>>

# if __name__ == '__main__':
#     unittest.main()

# <<<<<<<<<<----------


# ==========


# ---------->>>>>>>>>>

# from django.test import TestCase
# from django.urls import reverse
# from django.contrib.auth import get_user_model
# from notes.models import Note

# User = get_user_model()


# class TestHomePage(TestCase):
#     NOTES_URL = reverse('notes:list')

#     @classmethod
#     def setUpTestData(cls):
#         """Создание списка заметок."""
#         NOTES_COUNT_ON_NOTES_PAGE = 10
#         cls.author = User.objects.create(username='Автор заметки')
#         all_notes = [
#             Note(
#                 title=f'Заметка {index}',
#                 text=f'Текст заметки {index}.',
#                 slug=f'zametka_{index}',
#                 author=cls.author,
#             )
#             for index in range(NOTES_COUNT_ON_NOTES_PAGE + 1)
#         ]
#         Note.objects.bulk_create(all_notes)

#     def test_notes_order(self):
#         """Тест расположения заметок: старые - вверху списка, новые - внизу."""
#         # Авторизуем пользователя
#         self.client.force_login(self.author)
#         response = self.client.get(self.NOTES_URL)
#         object_list = response.context['object_list']
#         # Получаем id заметок в порядке их отображения
#         displayed_ids = [note.id for note in object_list]
#         # Получаем все заметки, отсортированные по возрастанию id
#         expected_ids = list(Note.objects.all().order_by('id').values_list('id', flat=True))
#         # Сравниваем порядок id
#         self.assertEqual(displayed_ids, expected_ids)

# <<<<<<<<<<----------
