# Generated by Django 4.0.1 on 2022-01-22 14:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('certifyapi', '0007_certificates_event_certificates_events'),
    ]

    operations = [
        migrations.RenameField(
            model_name='events',
            old_name='content',
            new_name='certificate_default_content',
        ),
        migrations.AddField(
            model_name='events',
            name='event_name',
            field=models.TextField(default=0),
            preserve_default=False,
        ),
    ]
