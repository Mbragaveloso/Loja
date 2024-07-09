from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='produto',
            name='preco_marketing',
            field=models.FloatField(blank=True, null=True, verbose_name='Preço de Marketing'),
        ),
    ]