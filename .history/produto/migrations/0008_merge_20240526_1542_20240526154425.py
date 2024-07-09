from django.db import migrations


def set_default_preco_marketing(apps, schema_editor):
    Produto = apps.get_model('produto', 'Produto')
    Produto.objects.filter(preco_marketing__isnull=True).update(preco_marketing=0.0)


class Migration(migrations.Migration):
    dependencies = [
        ('produto', 'xxxx_migration_name'),  # Substitua 'xxxx_migration_name' pelo nome da sua última migração
    ]

    operations = [
        migrations.RunPython(set_default_preco_marketing),
    ]   