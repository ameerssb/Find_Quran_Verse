# Generated by Django 4.0.5 on 2023-04-07 22:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quran_app', '0002_rename_quran_text_simplee_quran_text_all_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Quran_Suras',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
            ],
        ),
    ]