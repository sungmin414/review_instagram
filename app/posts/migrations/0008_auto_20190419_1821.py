# Generated by Django 2.2 on 2019-04-19 09:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0007_comment__html'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comment',
            name='_html',
            field=models.TextField(blank=True, verbose_name='태그가 HTML화된 댓글 내용'),
        ),
    ]
