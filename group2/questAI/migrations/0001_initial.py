# Generated by Django 2.1.5 on 2024-03-06 15:59

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
                ('basketId', models.AutoField(primary_key=True, serialize=False)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('quantity', models.IntegerField(default=1)),
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
                ('productId', models.AutoField(primary_key=True, serialize=False)),
                ('productName', models.CharField(max_length=64, unique=True)),
                ('productDescription', models.CharField(max_length=500)),
                ('price', models.DecimalField(decimal_places=2, max_digits=6)),
                ('category', models.CharField(max_length=64)),
                ('image', models.ImageField(upload_to='product_images/')),
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
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('address', models.CharField(max_length=512)),
                ('postcode', models.CharField(max_length=32)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
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