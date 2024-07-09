from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0008_pedido_itempedido'),  # Substitua pelo nome da última migração de produto
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='status',
            field=models.CharField(max_length=50, default='Pendente'),
        ),
    ]