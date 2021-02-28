# Generated by Django 2.2.12 on 2021-01-14 18:28

import address.models
from django.db import migrations, models
import django.db.models.deletion
import lib.cartomancy.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('address', '0003_auto_20200830_1851'),
    ]

    operations = [
        migrations.CreateModel(
            name='Entity',
            fields=[
                ('guid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('slug', models.SlugField(blank=True)),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('updated', models.DateTimeField(auto_now=True)),
                ('data', models.JSONField()),
            ],
        ),
        migrations.CreateModel(
            name='AirBnB',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cartomancy.Entity')),
                ('room_id', models.IntegerField(default=0)),
            ],
            bases=('cartomancy.entity', lib.cartomancy.models.Addressable, lib.cartomancy.models.Contactable),
        ),
        migrations.CreateModel(
            name='Business',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cartomancy.Entity')),
            ],
            bases=('cartomancy.entity', lib.cartomancy.models.Addressable, lib.cartomancy.models.Contactable),
        ),
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cartomancy.Entity')),
                ('card', models.JSONField(verbose_name='Contact Card')),
            ],
            bases=('cartomancy.entity',),
        ),
        migrations.CreateModel(
            name='Location',
            fields=[
                ('entity_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='cartomancy.Entity')),
                ('lat', models.FloatField(blank=True)),
                ('lng', models.FloatField(blank=True)),
                ('plus', models.CharField(blank=True, max_length=20)),
                ('address', address.models.AddressField(blank=True, on_delete=django.db.models.deletion.CASCADE, related_name='+', to='address.Address')),
            ],
            bases=('cartomancy.entity',),
        ),
    ]
