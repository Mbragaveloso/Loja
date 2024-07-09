from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_remove_produto_preco_remove_variacao_preco_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing',
            field=models.FloatField(verbose_name='Preço', default=0.0),
        ),
        migrations.RunPython(set_default_preco_marketing),
    ]

def set_default_preco_marketing(apps, schema_editor):
    Produto = apps.get_model('produto', 'Produto')
    Produto.objects.filter(preco_marketing__isnull=True).update(preco_marketing=0.0)