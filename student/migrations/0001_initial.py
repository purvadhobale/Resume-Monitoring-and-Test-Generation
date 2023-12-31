# Generated by Django 4.0.6 on 2023-05-16 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Application_Student',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=122)),
                ('email', models.EmailField(max_length=125)),
                ('date', models.DateField(auto_now_add=True)),
                ('gender', models.CharField(max_length=10)),
                ('phone', models.CharField(max_length=12)),
                ('strengths', models.CharField(max_length=100)),
                ('weakness', models.CharField(max_length=100)),
                ('resume', models.FileField(upload_to='uploads/')),
                ('skills', models.CharField(default='none', max_length=150)),
            ],
        ),
        migrations.CreateModel(
            name='Student_Register',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=122)),
                ('email', models.CharField(max_length=122)),
                ('phone', models.CharField(max_length=12)),
                ('password', models.CharField(max_length=20)),
            ],
        ),
    ]
