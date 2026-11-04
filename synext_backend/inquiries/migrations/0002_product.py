from django.db import migrations, models


PRODUCTS = [
    ("neurosyn-m", "Neurosyn-M", "Alpha Lipoic Acid 200mg + Benfotimine 100mg + Folic Acid 1.5 mg + Inosital 100mg + Methilcobalamin 1000 mcg + vitamin B6 3mg.", "Tablets"),
    ("pantosyn-20-40", "Pantosyn 20/40", "Pantoprazole 20mg/40mg Tablets", "Tablets"),
    ("trypsyn-r", "Trypsyn-R", "Bromelin 90mg + Rutoside Trihydrate 100mg + Trypsin 48mg", "Tablets"),
    ("cefixa-200", "Cefixa 200", "Cefixime 200mg Tablets", "Tablets"),
    ("betasyn-8-16", "Betasyn 8/16", "Betahistine 8mg/16mg Tablets", "Tablets"),
    ("pregasyn", "Pregasyn", "Pregabalin 75mg + Methylcobalamin 1500mcg", "Capsules"),
    ("pregasyn-forte", "Pregasyn Forte", "Methylcobalamin 750mcg + Pregabalin 50mg", "Capsules"),
]


def add_existing_products(apps, schema_editor):
    Product = apps.get_model("inquiries", "Product")
    Product.objects.using(schema_editor.connection.alias).bulk_create(
        [
            Product(id=product_id, name=name, description=description, category=category, sort_order=order)
            for order, (product_id, name, description, category) in enumerate(PRODUCTS)
        ]
    )


class Migration(migrations.Migration):
    dependencies = [
        ("inquiries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Product",
            fields=[
                ("id", models.SlugField(max_length=120, primary_key=True, serialize=False)),
                ("name", models.CharField(max_length=120)),
                ("description", models.TextField(max_length=2000)),
                ("category", models.CharField(blank=True, max_length=120)),
                ("sort_order", models.PositiveIntegerField(default=0)),
            ],
            options={
                "ordering": ["sort_order", "name"],
            },
        ),
        migrations.RunPython(add_existing_products, migrations.RunPython.noop),
    ]
