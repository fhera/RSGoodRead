# Generated by Django 2.2.6 on 2020-01-22 17:32

import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Libro',
            fields=[
                ('idLibro', models.IntegerField(primary_key=True, serialize=False)),
                ('Titulo', models.CharField(max_length=100)),
                ('Autor', models.CharField(max_length=30)),
                ('Isbn', models.IntegerField()),
                ('Idioma', models.CharField(max_length=30)),
                ('NumPuntuaciones1', models.PositiveIntegerField()),
                ('NumPuntuaciones2', models.PositiveIntegerField()),
                ('NumPuntuaciones3', models.PositiveIntegerField()),
                ('NumPuntuaciones4', models.PositiveIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('idUsuario', models.IntegerField(primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Puntuacion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Puntuacion', models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)])),
                ('idLibro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GoodReads.Libro')),
                ('idUsuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='GoodReads.Usuario')),
            ],
        ),
    ]