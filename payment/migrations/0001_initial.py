# Generated by Django 4.2.3 on 2024-08-30 09:39

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Payment_deposit',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deposit_balance', models.IntegerField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Payment_withdrwable',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('withdraable_balance', models.IntegerField(blank=True, null=True)),
            ],
        ),
    ]
