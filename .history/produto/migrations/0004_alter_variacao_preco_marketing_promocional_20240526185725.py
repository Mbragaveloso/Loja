from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_remove_produto_tamanho_alter_produto_preco_marketing'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variacao',
            name='preco_marketing_promocional',
            field=models.FloatField(blank=True, null=True, verbose_name='Preço de Marketing'),
            preserve_default=False,
        ),
    ]