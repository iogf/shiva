# Generated by Django 3.0.5 on 2020-05-22 02:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ticket_app', '0005_auto_20200521_0613'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ticket',
            name='city',
            field=models.CharField(blank=True, help_text='Type your city. (Optional)', max_length=60, null=True, verbose_name='City'),
        ),
    ]
