# Generated by Django 3.1.4 on 2020-12-14 15:07

from django.db import migrations
import keygenerator.fields


class Migration(migrations.Migration):

    dependencies = [
        ('keygenerator', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='peer',
            name='address',
            field=keygenerator.fields.IPv4AddressField(unique=True),
        ),
    ]
