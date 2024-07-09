from imporfrom django.db import migrations, models
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0008_alter_produto_imagem_alter_produto_preco_marketing_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='variacao',
            name='preco',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.RunSQL('UPDATE produto_variacao SET preco = 0.0 WHERE preco IS NULL;'),
    ]