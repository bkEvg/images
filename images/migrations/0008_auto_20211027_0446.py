# Generated by Django 3.2.8 on 2021-10-26 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('images', '0007_alter_convertedimage_parent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='image',
            name='picture',
            field=models.ImageField(blank=True, null=True, upload_to=''),
        ),
        migrations.AlterField(
            model_name='image',
            name='url',
            field=models.URLField(blank=True, null=True),
        ),
    ]