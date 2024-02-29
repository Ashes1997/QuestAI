# Generated by Django 2.1.5 on 2024-02-29 08:55

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Baskets',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('basketId', models.IntegerField(unique=True)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.ImageField(default=1, upload_to='')),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('commentId', models.IntegerField(unique=True)),
                ('commenttext', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Products',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('productId', models.IntegerField(unique=True)),
                ('productName', models.CharField(max_length=64)),
                ('productDescription', models.CharField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('category', models.CharField(max_length=64)),
                ('image_path', models.URLField()),
            ],
        ),
        migrations.CreateModel(
            name='Reviews',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reviewId', models.ImageField(unique=True, upload_to='')),
                ('rating', models.IntegerField(default=1)),
                ('productId', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questAI.Products')),
                ('username', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='comments',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questAI.Products'),
        ),
        migrations.AddField(
            model_name='comments',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='baskets',
            name='productId',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questAI.Products'),
        ),
        migrations.AddField(
            model_name='baskets',
            name='username',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]