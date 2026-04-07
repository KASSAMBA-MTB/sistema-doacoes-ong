from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0002_move_doacao_to_doacoes_app"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="Doacao",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("item", models.CharField(max_length=255)),
                        ("quantidade", models.IntegerField()),
                        ("data", models.DateTimeField(auto_now_add=True)),
                    ],
                    options={"db_table": "doacoes"},
                ),
            ],
        ),
    ]
