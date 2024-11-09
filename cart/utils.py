from django.core.mail import send_mail, BadHeaderError
from django.core.exceptions import ValidationError
from django.conf import settings
from .models import CartItem


def send_order_notification(order):
    """
    Отправляет уведомление на почту о новом заказе.
    """
    subject = f'Новый заказ #{order.id}'
    message = f'Детали заказа:\n\n' \
              f'Заказ ID: {order.id}\n' \
              f'Общая сумма: {order.total_price}\n' \
              f'Дата создания: {order.created_at}\n'

    recipient_list = ['homelife.site.kg@gmail.com']

    # Проверка на наличие получателей
    if not recipient_list:
        print("Ошибка: Нет получателей для отправки письма.")
        return

    try:
        send_mail(subject, message, settings.EMAIL_HOST_USER, recipient_list)
        print(f"Уведомление о заказе #{order.id} отправлено.")
    except BadHeaderError:
        # Ошибка в заголовках письма
        print("Ошибка в заголовках письма.")
    except ValidationError as ve:
        # Ошибка валидации email
        print(f"Ошибка валидации: {ve}")
    except Exception as e:
        # Другие ошибки при отправке письма
        print(f"Ошибка при отправке письма: {e}")


def remove_zero_quantity_items(cart):
    """
    Удаляет товары из корзины, если их количество равно 0.
    """
    # Удаление товаров с нулевым количеством из корзины
    deleted_count, _ = CartItem.objects.filter(cart=cart, quantity=0).delete()

    # Логирование количества удаленных товаров
    if deleted_count:
        print(f"Удалено {deleted_count} товара(ов) с нулевым количеством из корзины #{cart.id}.")
    else:
        print(f"Нет товаров с нулевым количеством в корзине #{cart.id}.")
