# Generated by Django 4.0.4 on 2022-06-15 15:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0006_alter_project_phase'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='phase',
            field=models.CharField(choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5'), (6, '6'), (7, '7'), (8, '8'), (9, '9'), (10, '10')], max_length=100, null=True),
        ),
    ]
