from django.db import migrations, models

def set_default_preco_marketing(apps, schema_editor):
    Produto = apps.get_model('produto', 'Produto')
    Produto.objects.filter(preco_marketing__isnull=True).update(preco_marketing=0.0)

class Migration(migrations.Migration):
    dependencies = [
        ('produto', '0006_alter_variacao_preco_marketing'),  # Dependendo da migração anterior
    ]

    operations = [
        migrations.RunPython(set_default_preco_marketing),  # Execute a função para definir o valor padrão
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing',
            field=models.FloatField(default=0.0, verbose_name='Preço de Marketing'),  # Defina o valor padrão aqui
        ),
    ]