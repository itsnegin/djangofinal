

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('rate',models.FloatField(validators=[django.core.validators.MinValueValidator(0), django.core.validators.MaxValueValidator(5)])),
                ('teacher', models.CharField(max_length=70)),
                ('price', models.PositiveIntegerField()),
                ('duration', models.PositiveIntegerField()),
                ('level', models.CharField(choices=[('beginner', 'bgn'), ('intermediate', 'int'), ('advanced', 'adv'), ('comprehensive','comp')], default='beginner', max_length=20)),
                ('certificate', models.BooleanField(default=False)),
                ('prerequisites', models.TextField()),
                ('capacity', models.PositiveIntegerField()),
                ('enrolled_count', models.PositiveIntegerField(default=0)),
                ('start_date', models.DateField()),
                ('date_created', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]