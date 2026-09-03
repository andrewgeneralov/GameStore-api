from django.db import models


class Developer(models.Model):
    name = models.CharField(max_length=150, unique=True)
    country = models.CharField(max_length=100)
    website = models.URLField(blank=True)
    established_year = models.PositiveIntegerField()

    class Meta:
        db_table = 'developers'

    def __str__(self):
        return self.name


class Game(models.Model):
    GENRE_CHOICES = [
        ('action', 'Экшен'),
        ('rpg', 'RPG'),
        ('strategy', 'Стратегия'),
        ('sports', 'Спорт'),
        ('simulation', 'Симулятор'),
    ]

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    release_date = models.DateField()
    developer = models.ForeignKey(Developer, on_delete=models.CASCADE, related_name='games', db_column='developer_id')
    is_available = models.BooleanField(default=True)

    class Meta:
        db_table = 'games'

    def __str__(self):
        return self.title


class Order(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Ожидание'),
        ('completed', 'Завершен'),
        ('cancelled', 'Отменен'),
    ]

    customer_email = models.EmailField()
    game = models.ForeignKey(Game, on_delete=models.CASCADE, related_name='orders', db_column='game_id')
    order_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    quantity = models.PositiveIntegerField(default=1)

    class Meta:
        db_table = 'orders'

    def __str__(self):
        return f"Order #{self.id} - {self.customer_email}"