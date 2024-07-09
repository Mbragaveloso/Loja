from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='produto',
            old_name='preco_marketing',
            new_name='preco',
        ),
        migrations.RenameField(
            model_name='variacao',
            old_name='preco_marketing',
            new_name='preco',
        ),
    ]