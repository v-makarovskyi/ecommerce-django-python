from django.db import models

from tabnanny import verbose
from django.db import models
from django.conf import settings
from django.urls import reverse
from mptt.models import MPTTModel, TreeForeignKey


class Category(MPTTModel):
    class Meta:
        verbose_name = 'категория'
        verbose_name_plural = 'категории'

    name = models.CharField('название', max_length=255, help_text='* обязательно уникальное название')
    slug = models.SlugField(max_length=255, unique=True)
    parent = TreeForeignKey('self', on_delete=models.SET_NULL, blank=True, null=True, related_name='children')
    is_active = models.BooleanField(default=True)

    class MPTTMeta:
        order_insertion_by = ['name']
    
    def get_absolute_url(self):
        return reverse('catalogue:category_list', args=[self.slug])
    
    def __str__(self) -> str:
        return self.name


class ProductType(models.Model):
    """
    will provide a list of the different types
    of products that are for sale
    """
    name = models.CharField(
        'Тип товара', help_text='Обязательное поле', max_length=255, unique=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = 'Тип продукта'
        verbose_name_plural = 'Типы продуктов'

    def __str__(self):
        return self.name


class ProductBrand(models.Model):
    title = models.CharField('бренд', max_length=50)

    class Meta:
        verbose_name = 'бренд'
        verbose_name_plural = 'бренды'
    
    def __str__(self) -> str:
        return self.title
    


class ProductSpecific(models.Model):
    """
    Table of technical characteristics and features of goods
    """
    product_type = models.ForeignKey(ProductType, on_delete=models.RESTRICT)
    name = models.CharField(verbose_name='Название характеристики типа товара',
                            help_text='Обязательное поле', max_length=255)

    class Meta:
        verbose_name = 'Спецификафия товара'
        verbose_name_plural = 'Спецификафии товаров'

    def __str__(self):
        return self.name


class Product(models.Model):
    """
    Table containing all data about a unit of goods
    """
    category = models.ForeignKey(
        Category, verbose_name='Категория', on_delete=models.RESTRICT)
    product_type = models.ForeignKey(
        ProductType, verbose_name='Тип товара', on_delete=models.RESTRICT)
    product_brand = models.ForeignKey(ProductBrand, on_delete=models.RESTRICT, verbose_name='бренд')
    title = models.CharField('Название', max_length=255,
                             help_text='Обязательное поле')
    description = models.TextField(
        'описание', help_text='необязательно', blank=True)
    slug = models.SlugField(max_length=255)
    regular_price = models.DecimalField(
        'стандартная цена', help_text='max 99999.99 грн', max_digits=7, decimal_places=2, error_messages={'name': {
            'max_lenght': 'Цена должна быть в диапазоне от 0 до 99999.99 грн'
        }},)
    is_active = models.BooleanField(
        'доступность продукта', help_text='выберите доступность продукта', default=True)
    created_at = models.DateTimeField(
        'создан', auto_now_add=True, editable=False)
    update_at = models.DateTimeField('обновлен', auto_now=True)
    users_wishlist = models.ManyToManyField(settings.AUTH_USER_MODEL)

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Товар'
        verbose_name_plural = 'Товары'

    def get_absolute_url(self):
        return reverse('catalogue:product_detail', args=[self.slug])

    def __str__(self):
        return self.title


class ProductSpecificValue(models.Model):
    """
    The table of product specification values contains the individual features of the product and its technical characteristics
    """
    product = models.ForeignKey(
        Product, verbose_name='товар', on_delete=models.CASCADE)
    specification = models.ForeignKey(
        ProductSpecific, verbose_name='выберите из списка', on_delete=models.RESTRICT)
    value = models.CharField('описание характеристик', max_length=100)

    class Meta:
        verbose_name_plural = 'описание характеристик товара'

    def __str__(self):
        return ('выберите из списка')


class ProductImage(models.Model):
    """
    The Product Image table.
    """
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name='product_image')
    title = models.CharField('название', help_text='введите название', max_length=100, )
    image = models.ImageField(
        'изображение', help_text='добавьте изображение товара', upload_to='images/')
    alt_text = models.CharField('альтернативный текст', max_length=150,
                                help_text='введите альтернативный текст', null=True, blank=True)
    is_feature = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True, editable=False)
    update_at = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name_plural = 'изображения товара'
    
    def __str__(self) -> str:
        return self.title
    
