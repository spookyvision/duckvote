# Generated by Django 4.1.3 on 2022-11-11 01:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0006_alter_voteevent_description"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="Choice",
            new_name="ChoiceOption",
        ),
    ]
