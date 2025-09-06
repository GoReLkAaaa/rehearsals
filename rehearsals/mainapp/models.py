from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager

# Create your models here.


class Product(models.Model):
    # Поля для блюд

    CATEGORY_CHOICES = [
        ('first', 'Первые блюда'),
        ('second', 'Вторые блюда'),
        ('dessert', 'Десерты'),
        ('drink', 'Напитки'),
    ]

    name_ru = models.CharField(
        max_length=255,
        verbose_name='Название блюда на русском'
    )
    name_uz = models.CharField(
        max_length=255,
        verbose_name='Название блюда на узбекском'
    )
    category = models.CharField(
        max_length=10,
        choices=CATEGORY_CHOICES,
        verbose_name='Категория блюда'
    )
    description_ru = models.TextField(
        verbose_name='Описание блюда на русском'
    )
    description_uz = models.TextField(
        verbose_name='Описание блюда на узбекском'
    )
    image = models.ImageField(
        upload_to='products/images/',
        null=True,
        blank=True,
        verbose_name='Картинка блюда',
    )
    video = models.FileField(
        upload_to='products/videos/',
        null=True,
        blank=True,
        verbose_name='Видео блюда',
    )

    # Поля для рецептов блюд
    recipe_text = models.TextField(
        verbose_name='Текст рецепта на русском'
    )
    recipe_text_uz = models.TextField(
        blank=True,
        null=True,
        verbose_name='Текст рецепта на узбекском'
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        verbose_name='Цена рецепта'
    )

    # Дополнительные материалы рецептов
    recipe_image = models.ImageField(
        upload_to='products/recipe_images/',
        null=True,
        blank=True,
        verbose_name='Доп. картинка рецепта'
    )
    recipe_video = models.FileField(
        upload_to='products/recipe_videos/',
        null=True,
        blank=True,
        verbose_name='Доп. видео рецепта'
    )
    recipe_file = models.FileField(
        upload_to='products/files/',
        null=True,
        blank=True,
        verbose_name='Доп. файл рецепта'
    )
    recipe_source_link = models.URLField(
        null=True,
        blank=True,
        verbose_name='Доп. ссылка рецепта'
    )


    def __str__(self):
        return self.name_ru


    class Meta:
        verbose_name = 'Блюдо'
        verbose_name_plural = 'Блюда'


class UserProfileManager(BaseUserManager):
    def create_user(self, telegram_id, password=None, **extra_fields):
        if not telegram_id:
            raise ValueError("У пользователя должен быть telegram_id")

        user = self.model(telegram_id=telegram_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, telegram_id, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Суперпользователь должен иметь is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Суперпользователь должен иметь is_superuser=True.")

        return self.create_user(telegram_id, password, **extra_fields)


class UserProfile(AbstractUser):
    username = None
    telegram_id = models.BigIntegerField(
        unique=True,
        verbose_name='Telegram ID пользователя'
    )
    language = models.CharField(
        max_length=2,
        choices=[
            ('ru', 'Русский'),
            ('uz', 'O‘zbek')
        ],
        default='ru',
        verbose_name='Выбранный язык'
    )

    USERNAME_FIELD = 'telegram_id'
    REQUIRED_FIELDS = []

    objects = UserProfileManager()

    def __str__(self):
        return str(self.telegram_id)


    class Meta:
        verbose_name = 'Профиль пользователя'
        verbose_name_plural = 'Профили пользователей'


class Purchase(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE,
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
    )
    purchase_date = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата покупки'
    )
    receipt = models.FileField(
        upload_to='receipts/',
        null=True,
        blank=True,
        verbose_name='Квитанция'
    )


    def __str__(self):
        return f'{self.user.telegram_id} - {self.product.name}'


    class Meta:
        verbose_name = 'История покупок и квитанции'
        verbose_name_plural = 'Истории покупок и квитанций'


class CartItem(models.Model):
    user = models.ForeignKey(
        UserProfile,
        on_delete=models.CASCADE
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE
    )


    def __str__(self):
        return f'{self.user.telegram_id} - {self.product.name_ru}'


    class Meta:
        unique_together = ('user', 'product')
        verbose_name = 'Корзина'
        verbose_name_plural = 'Корзины'
