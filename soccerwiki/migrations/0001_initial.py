# Generated by Django 3.2.25 on 2024-03-27 12:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
                ('description', models.TextField(max_length=200)),
            ],
        ),
        migrations.CreateModel(
            name='League',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=10)),
                ('country', models.CharField(max_length=10)),
                ('rank', models.IntegerField(max_length=10)),
            ],
        ),
        migrations.CreateModel(
            name='PlayerDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date_of_birth', models.DateTimeField()),
                ('team', models.CharField(max_length=255)),
                ('age', models.IntegerField(max_length=20)),
                ('league', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soccerwiki.league')),
            ],
        ),
        migrations.CreateModel(
            name='AchievementDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=20)),
                ('number', models.IntegerField(max_length=10)),
                ('year_won', models.IntegerField(null=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='soccerwiki.playerdetails')),
            ],
        ),
    ]