# Generated by Django 5.1.1 on 2024-10-11 17:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0006_exercice_date_limite'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HistoriqueConsultation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_consultation', models.DateTimeField(auto_now_add=True)),
                ('matiere', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.matiere')),
                ('utilisateur', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='consultations', to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]