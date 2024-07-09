from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0008_pedido_itempedido'),
    ]

   operations = [
        migrations.AddField(
            model_name='pedido',
            name='status',
            field=models.CharField(max_length=50, default='Pendente'),
        ),
    ]