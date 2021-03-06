# Generated by Django 3.2.4 on 2021-07-30 16:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Estate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=200)),
                ('price', models.IntegerField(default=0)),
                ('size', models.IntegerField(default=0)),
                ('image', models.CharField(max_length=250)),
                ('rooms', models.IntegerField(default=1)),
                ('location', models.CharField(max_length=200)),
                ('e_type', models.CharField(max_length=40)),
                ('pub_date', models.DateTimeField(verbose_name='date published')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=20)),
                ('password', models.CharField(max_length=100)),
            ],
        ),
        migrations.CreateModel(
            name='Pin',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('views', models.IntegerField(default=0)),
                ('likes', models.IntegerField(default=0)),
                ('estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adverts.estate')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='adverts.user')),
            ],
        ),
    ]
