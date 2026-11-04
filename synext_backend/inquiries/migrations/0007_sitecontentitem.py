from django.db import migrations, models
import django.db.models.deletion


def migrate_site_content_items(apps, schema_editor):
    SiteContent = apps.get_model("inquiries", "SiteContent")
    SiteContentItem = apps.get_model("inquiries", "SiteContentItem")
    database = schema_editor.connection.alias
    fields = {
        "nav_links": ("nav_link", ("label", "href")),
        "about_points": ("about_point", ("icon", "title", "text")),
        "quality_points": ("quality_point", ("icon", "title", "text")),
        "commitments_points": ("commitment_point", ("icon", "title", "text")),
        "why_points": ("why_point", ("icon", "title", "text")),
        "footer_quick_links": ("footer_quick_link", ("label", "href")),
        "footer_product_links": ("footer_product_link", ("label", "href")),
        "footer_legal_links": ("footer_legal_link", ("label", "href")),
    }

    for content in SiteContent.objects.using(database).all():
        items = []
        for field, (section, keys) in fields.items():
            values = getattr(content, field)
            if not isinstance(values, list):
                continue
            for sort_order, value in enumerate(values):
                if not isinstance(value, dict):
                    continue
                item_fields = {
                    key: str(value[key])
                    for key in keys
                    if value.get(key) is not None
                }
                items.append(SiteContentItem(
                    content_id=content.pk,
                    section=section,
                    sort_order=sort_order,
                    **item_fields,
                ))
        SiteContentItem.objects.using(database).bulk_create(items)


class Migration(migrations.Migration):

    dependencies = [
        ("inquiries", "0006_contactinquiry_company"),
    ]

    operations = [
        migrations.CreateModel(
            name="SiteContentItem",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("section", models.CharField(choices=[
                    ("nav_link", "Navigation links"),
                    ("about_point", "About points"),
                    ("quality_point", "Quality assurance points"),
                    ("commitment_point", "Commitment points"),
                    ("why_point", "Why choose us points"),
                    ("footer_quick_link", "Footer quick links"),
                    ("footer_product_link", "Footer product links"),
                    ("footer_legal_link", "Footer legal links"),
                ], max_length=32)),
                ("sort_order", models.PositiveIntegerField(default=0)),
                ("label", models.CharField(blank=True, max_length=200)),
                ("href", models.CharField(blank=True, max_length=300)),
                ("icon", models.CharField(blank=True, choices=[
                    ("quality", "Quality"),
                    ("transparency", "Transparency"),
                    ("standards", "Standards"),
                    ("support", "Support"),
                    ("care", "Care"),
                    ("clarity", "Clarity"),
                    ("engagement", "Engagement"),
                ], max_length=32)),
                ("title", models.CharField(blank=True, max_length=200)),
                ("text", models.TextField(blank=True)),
                ("content", models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name="items", to="inquiries.sitecontent")),
            ],
            options={
                "ordering": ["sort_order", "pk"],
            },
        ),
        migrations.RunPython(migrate_site_content_items, migrations.RunPython.noop),
        migrations.RemoveField(model_name="sitecontent", name="nav_links"),
        migrations.RemoveField(model_name="sitecontent", name="about_points"),
        migrations.RemoveField(model_name="sitecontent", name="quality_points"),
        migrations.RemoveField(model_name="sitecontent", name="commitments_points"),
        migrations.RemoveField(model_name="sitecontent", name="why_points"),
        migrations.RemoveField(model_name="sitecontent", name="footer_quick_links"),
        migrations.RemoveField(model_name="sitecontent", name="footer_product_links"),
        migrations.RemoveField(model_name="sitecontent", name="footer_legal_links"),
    ]
