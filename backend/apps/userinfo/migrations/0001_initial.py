# Generated by Django 3.2.7 on 2021-10-05 02:01

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('profile_is_completed', models.BooleanField(default=False)),
                ('first_name', models.CharField(max_length=30)),
                ('last_name', models.CharField(max_length=30)),
                ('email', models.EmailField(max_length=254)),
                ('nb_services_received', models.PositiveIntegerField()),
                ('nb_services_given', models.PositiveIntegerField()),
                ('avg_rating_as_employee', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('nb_rating_as_employe', models.PositiveIntegerField(default=0)),
                ('avg_rating_as_employer', models.DecimalField(decimal_places=2, default=0, max_digits=3)),
                ('nb_rating_as_employer', models.PositiveIntegerField(default=0)),
                ('user_id', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]