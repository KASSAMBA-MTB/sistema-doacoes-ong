from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_move_doacao_to_doacoes_app"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.DeleteModel(name="Usuario"),
            ],
        ),
    ]
