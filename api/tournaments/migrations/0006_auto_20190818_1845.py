# Generated by Django 2.2.3 on 2019-08-18 18:45

from django.db import migrations
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('tournaments', '0005_auto_20190817_1508'),
    ]

    operations = [
        migrations.AlterField(
            model_name='game',
            name='slug',
            field=django_extensions.db.fields.AutoSlugField(blank=True, editable=False, max_length=255, populate_from=['tournament', 'phase'], unique=True, verbose_name='slug'),
        ),
    ]
