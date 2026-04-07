from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("core", "0003_move_usuario_to_usuarios_app"),
    ]

    operations = [
        migrations.SeparateDatabaseAndState(
            database_operations=[],
            state_operations=[
                migrations.CreateModel(
                    name="Usuario",
                    fields=[
                        ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                        ("usuario", models.CharField(max_length=150, unique=True)),
                        ("senha", models.CharField(max_length=255)),
                    ],
                    options={"db_table": "usuarios"},
                ),
            ],
        ),
    ]
