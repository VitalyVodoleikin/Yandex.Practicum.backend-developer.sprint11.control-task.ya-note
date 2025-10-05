
# Задание
# 
# В файле test_logic.py:
# + Залогиненный пользователь может создать заметку, а анонимный — не может.
# + Невозможно создать две заметки с одинаковым slug.
# + Если при создании заметки не заполнен slug, то он формируется автоматически, с помощью функции pytils.translit.slugify.
# + Пользователь может редактировать и удалять свои заметки, но не может редактировать или удалять чужие.


# import unittest
from django.urls import reverse
from django.contrib.auth.models import User
from django.test import Client, TestCase
from notes.models import Note
from pytils.translit import slugify


class NoteLogicTests(TestCase):
    def setUp(self):
        # Создаем тестовых пользователей
        self.user1 = User.objects.create_user(username='testuser1', password='12345')
        self.user2 = User.objects.create_user(username='testuser2', password='12345')
        
        # Создаем клиента и авторизуем пользователя
        self.client = Client()
        self.client.force_login(self.user1)
        
        # Создаем тестовую заметку
        self.note = Note.objects.create(
            title='Тест',
            text='Содержание теста',
            author=self.user1
        )

    # Тест на создание заметки авторизованным пользователем
    def test_create_note_authenticated(self):

        # Проверяем начальное количество заметок
        self.assertEqual(Note.objects.count(), 1)

        response = self.client.post(reverse('notes:add'), data={
            'title': 'Новая заметка',
            'text': 'Содержание новой заметки'
        }, 
            # follow=True  # Добавляем follow для отслеживания редиректов
        )
        # self.assertEqual(response.status_code, 200)  # После follow статус будет 200
        self.assertEqual(response.status_code, 302)  # После перенаправленя статус будет 302
        self.assertEqual(Note.objects.count(), 2)  # Одна заметка уже создана в setUp

        # Проверяем создание новой заметки
        new_note = Note.objects.last()
        self.assertEqual(new_note.title, 'Новая заметка')
        self.assertEqual(new_note.text, 'Содержание новой заметки')
        self.assertEqual(new_note.author, self.user1)
        # print('Good')

    # Тест на невозможность создания заметки анонимным пользователем
    def test_create_note_anonymous(self):
        anon_client = Client()
        response = anon_client.post(reverse('notes:add'), {
            'title': 'Новая заметка',
            'text': 'Содержание новой заметки'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление на страницу входа
        self.assertEqual(Note.objects.count(), 1)  # Количество заметок не изменилось

    # Тест на уникальность slug
    def test_unique_slug(self):
        # Попытка создать заметку с тем же slug
        with self.assertRaises(Exception):
            Note.objects.create(
                title=self.note.title,
                text='Другое содержание',
                author=self.user1,
                slug=self.note.slug
            )

    # Тест на автоматическое формирование slug
    def test_auto_slug(self):
        response = self.client.post(reverse('notes:add'), {
            'title': 'Тестовая заметка',
            'text': 'Содержание'
        })
        self.assertEqual(response.status_code, 302)  # Перенаправление
        new_note = Note.objects.last()
        self.assertEqual(new_note.slug, slugify('тестовая-заметка'))

    # Тест на редактирование своей заметки
    def test_edit_own_note(self):
        response = self.client.post(reverse('notes:edit', args=[self.note.slug]), {
            'title': 'Измененная заметка',
            'text': 'Новое содержание'
        })
        self.assertEqual(response.status_code, 302)  # Успешное редактирование
        self.note.refresh_from_db()
        self.assertEqual(self.note.title, 'Измененная заметка')

    # Тест на невозможность редактирования чужой заметки
    def test_edit_foreign_note(self):
        # Создаем заметку для второго пользователя
        foreign_note = Note.objects.create(
            title='Чужая заметка',
            text='Содержание чужой заметки',
            author=self.user2
        )
        
        response = self.client.post(reverse('notes:edit', args=[foreign_note.slug]), {
            'title': 'Попытка изменения'
        })
        self.assertEqual(response.status_code, 404)  # Запрещено

    # Тест на удаление своей заметки
    def test_delete_own_note(self):
        response = self.client.post(reverse('notes:delete', args=[self.note.slug]))
        self.assertEqual(response.status_code, 302)  # Успешное удаление
        self.assertEqual(Note.objects.count(), 0)

    def test_delete_foreign_note(self):
       
        # Создаем заметку для второго пользователя
        foreign_note = Note.objects.create(
            title='Чужая заметка',
            text='Содержание чужой заметки',
            author=self.user2  # Указываем автора заметки
        )
        
        # Авторизуем первого пользователя
        self.client.force_login(self.user1)
        
        # Пытаемся удалить чужую заметку
        response = self.client.post(
            reverse('notes:delete', args=[foreign_note.id]),
            follow=True
        )
        
        # Проверяем, что заметка не была удалена
        self.assertEqual(response.status_code, 404)  # Или 403, в зависимости от реализации
        self.assertTrue(Note.objects.filter(id=foreign_note.id).exists())
