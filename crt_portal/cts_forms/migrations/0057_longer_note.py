# Generated by Django 2.2.11 on 2020-03-13 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cts_forms', '0056_add_CommentAndSummary_fields'),
    ]

    operations = [
        migrations.AlterField(
            model_name='commentandsummary',
            name='note',
            field=models.CharField(max_length=7000),
        ),
    ]
