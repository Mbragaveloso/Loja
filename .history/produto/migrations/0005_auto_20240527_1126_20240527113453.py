from django.db import migrations, models

class Migration(migrations.Migration):
    dependencies = [
        ('produto', '0004_alter_variacao_preco_marketing_promocional'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='preco_marketing',
            field=models.FloatField(verbose_name='Preço de Marketing'),
        ),
        migrations.AddField(
            model_name='variacao',
            name='preco_marketing',
            field=models.FloatField(default=0.0, verbose_name='Preço de Marketing'),
        ),
    ]