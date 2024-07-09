from django.db import migrations

class Migration(migrations.Migration):
    dependencies = [
        ('produto', '0006_alter_variacao_preco_marketing'),  # Dependa apenas da última migração
    ]

    operations = [
        # Adicione as operações necessárias aqui, como definir um valor padrão para preco_marketing
    ]