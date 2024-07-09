from django.db import migrations, models

def set_default_preco_marketing(apps, schema_editor):
    Produto = apps.get_model('produto', 'Produto')
    for produto in Produto.objects.all():
        if produto.preco_marketing is None:
            produto.preco_marketing = 0.0
            produto.save()

class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0004_alter_variacao_preco_marketing_promocional'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing',
            field=models.FloatField(default=0.0, verbose_name='Preço'),
        ),
        migrations.AlterField(
            model_name='variacao',
            name='preco_marketing',
            field=models.FloatField(blank=True, null=True, verbose_name='Preço'),
        ),
        migrations.RunPython(set_default_preco_marketing),  # Certifique-se de incluir essa linha
    ]