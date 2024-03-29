# Generated by Django 2.2.18 on 2021-08-01 19:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Prestamo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prestador', models.CharField(max_length=30)),
                ('objeto', models.TextField()),
                ('recibidor', models.CharField(max_length=30)),
                ('fecha_prestamo', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
        migrations.CreateModel(
            name='Notificacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('contraparte', models.CharField(max_length=30)),
                ('objeto', models.TextField()),
                ('telefono', models.CharField(default=0, max_length=9, null=True)),
                ('oferta_id', models.IntegerField(null=True)),
                ('fecha_notificacion', models.DateTimeField(auto_now_add=True)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='usuarios.Usuario')),
            ],
            options={
                'ordering': ['-id'],
            },
        ),
    ]
