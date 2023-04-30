# Generated by Django 4.1.7 on 2023-04-29 07:33

import django.core.serializers.json
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('insurance_contract', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='company',
            name='email',
            field=models.CharField(default='', max_length=256),
        ),
        migrations.AlterField(
            model_name='excessofloss',
            name='reinstatements',
            field=models.JSONField(encoder=django.core.serializers.json.DjangoJSONEncoder),
        ),
    ]