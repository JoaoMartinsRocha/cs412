# Generated by Django 5.1.5 on 2025-02-14 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0002_alter_article_author_alter_article_text_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='image_url',
            field=models.URLField(blank=True),
        ),
    ]
