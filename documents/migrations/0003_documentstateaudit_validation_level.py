# Generated manually for adding validation_level to DocumentStateAudit

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('documents', '0002_alter_document_entity_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='documentstateaudit',
            name='validation_level',
            field=models.IntegerField(blank=True, help_text='Nivel de validación aprobado/rechazado', null=True),
        ),
    ]
