<<<<<<< HEAD
# Generated by Django 4.0.2 on 2022-03-12 01:42
=======
# Generated by Django 4.0.2 on 2022-03-14 09:33
>>>>>>> 0f277551f46bb7d33cd5d5a5e6c3cfaf6273b726

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='SentTelegramMessage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('chat_id', models.CharField(blank=True, max_length=20, null=True, verbose_name='Chat ID')),
                ('chat_type', models.CharField(blank=True, max_length=10, null=True, verbose_name='Type')),
                ('chat_title', models.CharField(blank=True, max_length=100, null=True, verbose_name='Chat Title')),
                ('chat_message_id', models.BigIntegerField(blank=True, null=True, verbose_name='Message ID')),
                ('chat_date', models.DateTimeField(auto_now_add=True, null=True, verbose_name='날짜')),
                ('chat_text', models.TextField(blank=True, null=True, verbose_name='내용')),
                ('is_del', models.BooleanField(default=False, verbose_name='회수여부')),
            ],
            options={
                'verbose_name': '텔레그램 메시지',
                'verbose_name_plural': '텔레그램 메시지',
            },
        ),
    ]