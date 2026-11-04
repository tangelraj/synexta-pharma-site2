from django.db import migrations


PRODUCT_DETAILS = {
    "neurosyn-m": {
        "old_description": "Alpha Lipoic Acid 200mg + Benfotimine 100mg + Folic Acid 1.5 mg + Inosital 100mg + Methilcobalamin 1000 mcg + vitamin B6 3mg.",
        "old_category": "Tablets",
        "description": "Alpha Lipoic Acid 200 mg + Benfotiamine 100 mg + Folic Acid 1.5 mg + Inositol 100 mg + Methylcobalamin 1000 mcg + Vitamin B6 3 mg",
        "category": "Neurological Health",
    },
    "pantosyn-20-40": {
        "old_description": "Pantoprazole 20mg/40mg Tablets",
        "old_category": "Tablets",
        "description": "Pantoprazole 20 mg / 40 mg Tablets",
        "category": "Gastrointestinal Health",
    },
    "trypsyn-r": {
        "old_description": "Bromelin 90mg + Rutoside Trihydrate 100mg + Trypsin 48mg",
        "old_category": "Tablets",
        "description": "Bromelain 90 mg + Rutoside Trihydrate 100 mg + Trypsin 48 mg",
        "category": "Musculoskeletal Support",
    },
    "cefixa-200": {
        "old_description": "Cefixime 200mg Tablets",
        "old_category": "Tablets",
        "description": "Cefixime 200 mg Tablets",
        "category": "Other Formulations",
    },
    "betasyn-8-16": {
        "old_description": "Betahistine 8mg/16mg Tablets",
        "old_category": "Tablets",
        "description": "Betahistine 8 mg / 16 mg Tablets",
        "category": "Other Formulations",
    },
    "pregasyn": {
        "old_description": "Pregabalin 75mg + Methylcobalamin 1500mcg",
        "old_category": "Capsules",
        "description": "Pregabalin 75 mg + Methylcobalamin 1500 mcg",
        "category": "Neurological Health",
    },
    "pregasyn-forte": {
        "old_description": "Methylcobalamin 750mcg + Pregabalin 50mg",
        "old_category": "Capsules",
        "description": "Methylcobalamin 750 mcg + Pregabalin 50 mg",
        "category": "Neurological Health",
    },
}


def refresh_default_product_details(apps, schema_editor):
    Product = apps.get_model("inquiries", "Product")
    database = schema_editor.connection.alias

    for product_id, details in PRODUCT_DETAILS.items():
        product = Product.objects.using(database).filter(pk=product_id).first()
        if product is None:
            continue

        updated_fields = []
        if product.description == details["old_description"]:
            product.description = details["description"]
            updated_fields.append("description")
        if product.category == details["old_category"]:
            product.category = details["category"]
            updated_fields.append("category")
        if updated_fields:
            product.save(using=database, update_fields=updated_fields)


class Migration(migrations.Migration):
    dependencies = [
        ("inquiries", "0002_product"),
    ]

    operations = [
        migrations.RunPython(refresh_default_product_details, migrations.RunPython.noop),
    ]
