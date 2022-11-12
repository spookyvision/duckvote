# Generated by Django 4.1.3 on 2022-11-12 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("voting", "0009_choiceoption_description"),
    ]

    operations = [
        migrations.AlterField(
            model_name="ynavote",
            name="choice",
            field=models.CharField(
                choices=[("Y", "Yes"), ("N", "No"), ("A", "Abstain")],
                default=None,
                max_length=1,
            ),
        ),
        migrations.AlterUniqueTogether(
            name="ynavote",
            unique_together={("user", "yna")},
        ),
    ]