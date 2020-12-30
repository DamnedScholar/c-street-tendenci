# Generated by Django 2.2.12 on 2020-12-02 10:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('document_viewer', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ViewCountLog',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('target', models.ForeignKey(on_delete=None, to='document_viewer.ViewCountTarget')),
            ],
        ),
    ]