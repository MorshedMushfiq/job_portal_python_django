# Generated by Django 5.1.1 on 2024-09-27 15:24

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0007_alter_institutenamemodel_unique_together'),
    ]

    operations = [
        migrations.RenameField(
            model_name='educationmodel',
            old_name='instituion_name',
            new_name='institution_name',
        ),
    ]
