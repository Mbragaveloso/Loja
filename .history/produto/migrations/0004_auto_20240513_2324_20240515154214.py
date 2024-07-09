from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_auto_20240513_2314'),
    ]

    operations = [
       migrations.AddField(
            model_name='produto',
            name='preco',
            field=models.FloatField(default=0.0),  # Adicione o argumento default aqui
            preserve_default=False,
        ),
    ] 