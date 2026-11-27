

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('sematec', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='level',
            field=models.CharField(choices=[('beginner', 'Beginner'), ('intermediate', 'Intermediate'), ('advanced', 'Advanced'),('comprehensive', 'Comprehensive')], default='beginner', max_length=20),
        ),
    ]