# Generated by Django 2.2 on 2019-04-15 08:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='comment',
            options={'verbose_name': '댓글', 'verbose_name_plural': '댓글 목록'},
        ),
        migrations.AlterModelOptions(
            name='hashtag',
            options={'verbose_name': '해시태그', 'verbose_name_plural': '해시태그 목록'},
        ),
        migrations.AlterModelOptions(
            name='post',
            options={'verbose_name': '포스트', 'verbose_name_plural': '포스트 목록'},
        ),
        migrations.AlterField(
            model_name='comment',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.User', verbose_name='작성자'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='content',
            field=models.TextField(verbose_name='댓글 내용'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='post',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='posts.Post', verbose_name='포스트'),
        ),
        migrations.AlterField(
            model_name='comment',
            name='tags',
            field=models.ManyToManyField(blank=True, to='posts.HashTag', verbose_name='해시태그 목록'),
        ),
        migrations.AlterField(
            model_name='hashtag',
            name='name',
            field=models.CharField(max_length=100, verbose_name='태그명'),
        ),
        migrations.AlterField(
            model_name='post',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='members.User', verbose_name='작성자'),
        ),
        migrations.AlterField(
            model_name='post',
            name='photo',
            field=models.ImageField(upload_to='post', verbose_name='사진'),
        ),
    ]