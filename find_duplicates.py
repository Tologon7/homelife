import os
import django

# Настройка окружения Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')  # Убедитесь, что указано правильно
django.setup()

from product.models import Category
from django.db.models import Count

# Получение дубликатов
duplicates = Category.objects.values('value').annotate(count=Count('id')).filter(count__gt=1)

for duplicate in duplicates:
    value = duplicate['value']
    label = 'холодник'  # Здесь вы можете установить нужное значение для label
    print(f'value: "{value}", label: "{label}"')
