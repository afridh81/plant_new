# Generated by Django 3.2.9 on 2021-11-29 10:44

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('plant_disease_app', '0002_predicted_label'),
    ]

    operations = [
        migrations.AlterField(
            model_name='predicted_label',
            name='photo',
            field=models.ImageField(upload_to='Pred'),
        ),
        migrations.CreateModel(
            name='Last_login_user',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]