from django.test import TestCase
from django.urls import reverse
from django.contrib.auth import get_user_model
from notes.models import Note

User = get_user_model()


class TestHomePage(TestCase):
    NOTES_URL = reverse('notes:list')

    @classmethod
    def setUpTestData(cls):
        """Создание списка заметок."""
        NOTES_COUNT_ON_NOTES_PAGE = 10
        cls.author = User.objects.create(username='Автор заметки')
        all_notes = [
            Note(
                title=f'Заметка {index}',
                text=f'Текст заметки {index}.',
                slug=f'zametka_{index}',
                author=cls.author,
            )
            for index in range(NOTES_COUNT_ON_NOTES_PAGE + 1)
        ]
        Note.objects.bulk_create(all_notes)

    def test_notes_order(self):
        """Тест расположения заметок: старые - вверху списка, новые - внизу."""
        # Авторизуем пользователя
        self.client.force_login(self.author)
        response = self.client.get(self.NOTES_URL)
        object_list = response.context['object_list']
        # Получаем id заметок в порядке их отображения
        displayed_ids = [note.id for note in object_list]
        # Получаем все заметки, отсортированные по возрастанию id
        expected_ids = list(Note.objects.all().order_by('id').values_list('id', flat=True))
        # Сравниваем порядок id
        self.assertEqual(displayed_ids, expected_ids)
