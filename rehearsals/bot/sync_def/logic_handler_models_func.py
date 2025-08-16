from asgiref.sync import sync_to_async

from mainapp.models import Product, UserProfile, Purchase, CartItem


# Получение или создание пользователя
@sync_to_async
def get_or_create_new_user(telegram_id):
    user, created = UserProfile.objects.get_or_create(
        telegram_id=telegram_id,
    )
    return user


# Получение продукта
@sync_to_async
def get_product(product_id):
    return Product.objects.get(
        id=product_id
    )


# Добавление блюда в корзину
@sync_to_async
def add_to_cart(user, product):
    if CartItem.objects.filter(
            user=user,
            product=product
    ).exists():
        return False

    CartItem.objects.create(
        user=user,
        product=product
    )
    return True


# Удаления блюда из  корзины
@sync_to_async
def remove_from_cart(user, product):
    deleted, _ = CartItem.objects.filter(user=user, product=product).delete()
    return deleted > 0


#Получение корзины
@sync_to_async
def get_basket_items(telegram_id):
    return list(CartItem.objects.filter(
        user__telegram_id=telegram_id
    ).select_related("product"))


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


# Получение блюд по категории + пагинация
@sync_to_async
def get_products_by_category(category, offset=0, limit=3):
    return list(Product.objects.filter(
        category=category
    )[offset:offset+limit])


@sync_to_async
def get_products_count(category):
    return Product.objects.filter(
        category=category
    ).count()