# Generated by Django 4.0.3 on 2022-11-02 15:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_coffeeshop_numrates_coffeeshop_rating'),
    ]

    operations = [
        migrations.CreateModel(
            name='Info',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shop_id', models.IntegerField(default=0)),
                ('info', models.CharField(default=None, max_length=255)),
            ],
        ),
    ]
