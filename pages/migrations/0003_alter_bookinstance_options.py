# Generated by Django 5.1 on 2024-09-03 14:31

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0002_bookinstance_borrower'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='bookinstance',
            options={'ordering': ['due_back'], 'permissions': (('can_mark_returned', 'Set book as returned'),)},
        ),
    ]
