# Generated by Django 4.2 on 2023-05-16 06:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('web', '0003_news_image'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='news',
            name='image',
        ),
        migrations.AddField(
            model_name='news',
            name='image_url',
            field=models.URLField(blank=True, default='https://nhadepso.com/wp-content/uploads/2023/03/loa-mat-voi-nhung-hinh-anh-co-viet-nam-tuyet-dep-lam-hinh-nen_1.jpg', null=True),
        ),
    ]
