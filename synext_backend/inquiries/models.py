from django.db import models


class Product(models.Model):
    id = models.SlugField(primary_key=True, max_length=120)
    name = models.CharField(max_length=120)
    description = models.TextField(max_length=2000)
    category = models.CharField(max_length=120, blank=True)
    sort_order = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to="products/", blank=True)

    class Meta:
        ordering = ["sort_order", "name"]

    def __str__(self):
        return self.name


class SiteContent(models.Model):
    id = models.CharField(max_length=20, primary_key=True, default="default", editable=False)
    logo_image = models.ImageField(upload_to="site/", blank=True)
    hero_image = models.ImageField(upload_to="site/", blank=True)
    about_image = models.ImageField(upload_to="site/", blank=True)
    quality_background_image = models.ImageField(upload_to="site/", blank=True)
    why_image = models.ImageField(upload_to="site/", blank=True)
    contact_background_image = models.ImageField(upload_to="site/", blank=True)
    nav_cta_label = models.CharField(max_length=120, default="Explore Products")
    nav_cta_href = models.CharField(max_length=200, default="#products")
    about_eyebrow = models.CharField(max_length=120, default="ABOUT SYNEXTA PHARMA")
    about_title = models.CharField(max_length=200, default="Committed to quality. Focused on care.")
    about_body = models.TextField(default="")
    quality_eyebrow = models.CharField(max_length=120, default="Quality Assurance")
    commitments_title = models.CharField(max_length=120, default="OUR COMMITMENTS")
    commitments_subtitle = models.CharField(max_length=200, default="Quality at the Heart of Every Formulation")
    why_eyebrow = models.CharField(max_length=120, default="WHY CHOOSE US")
    why_title = models.CharField(max_length=200, default="Why choose Synexta Pharma?")
    why_body = models.TextField(default="")
    footer_tagline = models.CharField(max_length=200, default="Quality Medicines. Trusted Care.")
    footer_products_heading = models.CharField(max_length=120, default="Products")
    footer_copyright = models.CharField(max_length=200, default="© 2026 Synexta Pharma. All rights reserved.")

    class Meta:
        verbose_name = "website content"
        verbose_name_plural = "website content"

    def __str__(self):
        return "Website content"


class SiteContentItem(models.Model):
    class Section(models.TextChoices):
        NAV_LINK = "nav_link", "Navigation links"
        ABOUT_POINT = "about_point", "About points"
        QUALITY_POINT = "quality_point", "Quality assurance points"
        COMMITMENT_POINT = "commitment_point", "Commitment points"
        WHY_POINT = "why_point", "Why choose us points"
        FOOTER_QUICK_LINK = "footer_quick_link", "Footer quick links"
        FOOTER_PRODUCT_LINK = "footer_product_link", "Footer product links"
        FOOTER_LEGAL_LINK = "footer_legal_link", "Footer legal links"

    class Icon(models.TextChoices):
        QUALITY = "quality", "Quality"
        TRANSPARENCY = "transparency", "Transparency"
        STANDARDS = "standards", "Standards"
        SUPPORT = "support", "Support"
        CARE = "care", "Care"
        CLARITY = "clarity", "Clarity"
        ENGAGEMENT = "engagement", "Engagement"

    content = models.ForeignKey(SiteContent, on_delete=models.CASCADE, related_name="items")
    section = models.CharField(max_length=32, choices=Section.choices)
    sort_order = models.PositiveIntegerField(default=0)
    label = models.CharField(max_length=200, blank=True)
    href = models.CharField(max_length=300, blank=True)
    icon = models.CharField(max_length=32, choices=Icon.choices, blank=True)
    title = models.CharField(max_length=200, blank=True)
    text = models.TextField(blank=True)

    class Meta:
        ordering = ["sort_order", "pk"]

    def __str__(self):
        return self.label or self.title or self.get_section_display()


class ContactInquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField(max_length=254)
    phone = models.CharField(max_length=30, blank=True)
    company = models.CharField(max_length=120, blank=True)
    topic = models.CharField(max_length=120)
    message = models.TextField(max_length=5000)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name_plural = "contact inquiries"

    def __str__(self):
        return f"{self.name} - {self.topic}"