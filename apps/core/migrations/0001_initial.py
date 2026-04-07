from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
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
        migrations.CreateModel(
            name="Usuario",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("usuario", models.CharField(max_length=150, unique=True)),
                ("senha", models.CharField(max_length=255)),
            ],
            options={"db_table": "usuarios"},
        ),
    ]
