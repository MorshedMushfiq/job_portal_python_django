# Generated by Django 5.1.1 on 2024-10-01 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0011_jobmodel'),
    ]

    operations = [
        migrations.AlterField(
            model_name='jobmodel',
            name='job_type',
            field=models.CharField(choices=[('full_time', 'Full-time'), ('part_time', 'Part-time'), ('internship', 'Internship'), ('freelance', 'Freelance')], max_length=100, null=True),
        ),
    ]
