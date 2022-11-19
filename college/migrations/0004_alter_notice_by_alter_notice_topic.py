# Generated by Django 4.1.3 on 2022-11-19 07:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("college", "0003_notice_topic"),
    ]

    operations = [
        migrations.AlterField(
            model_name="notice",
            name="by",
            field=models.CharField(blank=True, default="college", max_length=20),
        ),
        migrations.AlterField(
            model_name="notice",
            name="topic",
            field=models.CharField(blank=True, max_length=100),
        ),
    ]
