# Generated by Django 2.2.12 on 2020-07-01 13:15

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AirBnBData',
            fields=[
                ('room_id', models.IntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=30)),
                ('timestamp', models.DateTimeField()),
                ('lat', models.FloatField()),
                ('lng', models.FloatField()),
                ('avg_rating', models.FloatField()),
                ('reviews_count', models.IntegerField()),
                ('rate', models.FloatField()),
                ('rate_type', models.CharField(max_length=30)),
                ('verified', models.BooleanField(default=False)),
                ('superhost', models.BooleanField(default=False)),
                ('guests', models.CharField(blank=True, max_length=30)),
                ('baths', models.CharField(blank=True, max_length=30)),
                ('bedrooms', models.CharField(blank=True, max_length=30)),
                ('beds', models.CharField(blank=True, max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='ScrapedImage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
                ('image', models.ImageField(upload_to='addons/drone-hangar/scrapy/storage')),
                ('timestamp', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='ArchivedScrapedImage',
            fields=[
                ('scrapedimage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drone_hangar.ScrapedImage')),
                ('archive_time', models.DateTimeField()),
            ],
            bases=('drone_hangar.scrapedimage',),
        ),
        migrations.CreateModel(
            name='AirBnBImage',
            fields=[
                ('scrapedimage_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='drone_hangar.ScrapedImage')),
                ('room', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='drone_hangar.AirBnBData')),
            ],
            bases=('drone_hangar.scrapedimage',),
        ),
        migrations.AddField(
            model_name='airbnbdata',
            name='primary_picture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='drone_hangar.AirBnBImage'),
        ),
        migrations.AddField(
            model_name='airbnbdata',
            name='profile_picture',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to='drone_hangar.AirBnBImage'),
        ),
    ]