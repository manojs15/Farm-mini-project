# Generated by Django 5.0.2 on 2024-03-02 14:03

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0008_expense_budget'),
    ]

    operations = [
        migrations.AddField(
            model_name='expense',
            name='farm',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='app.farm'),
        ),
    ]
