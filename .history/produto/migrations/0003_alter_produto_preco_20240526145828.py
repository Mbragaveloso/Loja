import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0002_rename_preco_marketing_variacao_preco'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='produto',
            name='preco',
        ),
        migrations.RemoveField(
            model_name='variacao',
            name='preco',
        ),
        migrations.AddField(
            model_name='produto',
            name='opcoes_tamanho',
            field=models.CharField(blank=True, help_text='Separadas por vírgula', max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='produto',
            name='preco_marketing',
            field=models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Preço'),
        ),
        migrations.AddField(
            model_name='variacao',
            name='preco_marketing',
            field=models.FloatField(default=0.0),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='produto',
            name='nome',
            field=models.CharField(max_length=255),
        ),
        migrations.AlterField(
            model_name='produto',
            name='preco_marketing_promocional',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10, verbose_name='Preço Promo.'),
        ),
        migrations.AlterField(
            model_name='produto',
            name='slug',
            field=models.SlugField(blank=True, null=True, unique=True),
        ),
        migrations.AlterField(
            model_name='produto',
            name='tipo',
            field=models.CharField(choices=[('V', 'Variável'), ('S', 'Simples')], default='V', max_length=1),
        ),
        migrations.AlterField(
            model_name='variacao',
            name='nome',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
        migrations.AlterField(
            model_name='variacao',
            name='preco_marketing_promocional',
            field=models.FloatField(blank=True, null=True),
        ),
    ]