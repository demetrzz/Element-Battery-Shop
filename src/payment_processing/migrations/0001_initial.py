# Generated by Django 5.0 on 2023-12-15 10:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('shopping', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('pending', 'Ожидает оплаты'), ('waiting_for_capture', 'Оплачен, ожидает подтверждения'), ('succeeded', 'Оплачен и подтвержден'), ('canceled', 'Отменен')], db_index=True, max_length=20, verbose_name='Статус платежа')),
                ('amount', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Сумма платежа')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='shopping.order', verbose_name='Заказ')),
            ],
        ),
    ]