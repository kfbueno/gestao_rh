# Generated by Django 3.1 on 2020-08-07 22:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('funcionarios', '0002_auto_20200807_1959'),
        ('registro_hora_extra', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='registrohoraextra',
            name='funcionario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to='funcionarios.funcionario'),
            preserve_default=False,
        ),
    ]
