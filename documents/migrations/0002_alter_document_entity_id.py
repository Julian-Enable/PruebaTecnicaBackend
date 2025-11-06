# Generated manually for changing entity_id from UUID to CharField

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='document',
            name='entity_id',
            field=models.CharField(max_length=255, help_text='Permite IDs flexibles como placas, códigos, etc.'),
        ),
    ]
