from asgiref.sync import sync_to_async

from mainapp.models import Product, UserProfile, CartItem


# Получение или создание пользователя
@sync_to_async
def get_or_create_new_user(telegram_id):
    user, created = UserProfile.objects.get_or_create(
        telegram_id=telegram_id,
    )
    return user


# Получение пользователя для смены языка
@sync_to_async
def get_language_user(telegram_id):
    user = UserProfile.objects.filter(
        telegram_id=telegram_id
    ).first()

    return user.language if user else None


# Смена языка
@sync_to_async
def set_lang(telegram_id, language):
    UserProfile.objects.filter(
        telegram_id=telegram_id
    ).update(language=language)