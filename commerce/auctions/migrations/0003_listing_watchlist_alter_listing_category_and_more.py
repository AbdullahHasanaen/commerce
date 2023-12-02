# Generated by Django 4.2.6 on 2023-11-15 19:53

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0002_category_listing'),
    ]

    operations = [
        migrations.AddField(
            model_name='listing',
            name='watchlist',
            field=models.ManyToManyField(blank=True, null=True, related_name='listingWatchlist', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='listing',
            name='category',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='category', to='auctions.category'),
        ),
        migrations.AlterField(
            model_name='listing',
            name='description',
            field=models.CharField(max_length=2560),
        ),
        migrations.AlterField(
            model_name='listing',
            name='imgUrl',
            field=models.CharField(max_length=100000),
        ),
    ]