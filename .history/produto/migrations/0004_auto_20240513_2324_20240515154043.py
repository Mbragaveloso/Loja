from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0003_auto_20240513_2224'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='preco',
            field=models.FloatField(default=0.0),  # Adicione o argumento default aqui
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='descricao',
            field=models.TextField(default=0, max_length=800),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='descricao_curta',
            field=models.TextField(default=0, max_length=255),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='slug',
            field=models.SlugField(blank=True, default='', null=False, unique=True),
            preserve_default=False,
        ),
    ]