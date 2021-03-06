# Generated by Django 3.2.8 on 2021-10-26 20:55

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=100)),
                ('url', models.URLField(blank=True)),
                ('picture', models.ImageField(blank=True, upload_to='')),
                ('width', models.IntegerField(default=128)),
                ('height', models.IntegerField(default=128)),
            ],
        ),
        migrations.CreateModel(
            name='ConvertedImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='')),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parent', to='images.image')),
            ],
        ),
    ]
