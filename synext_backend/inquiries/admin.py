from django.contrib import admin
from django.forms.models import BaseInlineFormSet

from .models import ContactInquiry, Product, SiteContent, SiteContentItem


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ("name", "category", "id", "sort_order")
    list_editable = ("sort_order",)
    search_fields = ("name", "id", "description", "category")
    prepopulated_fields = {"id": ("name",)}


class SiteContentItemInlineFormSet(BaseInlineFormSet):
    section = None

    def save_new(self, form, commit=True):
        form.instance.section = self.section
        return super().save_new(form, commit)

    def save_existing(self, form, instance, commit=True):
        instance.section = self.section
        return super().save_existing(form, instance, commit)


class SiteContentItemInline(admin.TabularInline):
    model = SiteContentItem
    formset = SiteContentItemInlineFormSet
    extra = 0
    ordering = ("sort_order", "pk")
    section = None

    def get_queryset(self, request):
        return super().get_queryset(request).filter(section=self.section)

    def get_formset(self, request, obj=None, **kwargs):
        formset = super().get_formset(request, obj, **kwargs)
        formset.section = self.section
        return formset


class NavigationLinkInline(SiteContentItemInline):
    section = SiteContentItem.Section.NAV_LINK
    fields = ("sort_order", "label", "href")
    verbose_name = "Navigation link"
    verbose_name_plural = "Navigation links"


class AboutPointInline(SiteContentItemInline):
    section = SiteContentItem.Section.ABOUT_POINT
    fields = ("sort_order", "icon", "title", "text")
    verbose_name = "About point"
    verbose_name_plural = "About points"


class QualityPointInline(SiteContentItemInline):
    section = SiteContentItem.Section.QUALITY_POINT
    fields = ("sort_order", "icon", "title", "text")
    verbose_name = "Quality assurance point"
    verbose_name_plural = "Quality assurance points"


class CommitmentPointInline(SiteContentItemInline):
    section = SiteContentItem.Section.COMMITMENT_POINT
    fields = ("sort_order", "icon", "title", "text")
    verbose_name = "Commitment point"
    verbose_name_plural = "Commitment points"


class WhyPointInline(SiteContentItemInline):
    section = SiteContentItem.Section.WHY_POINT
    fields = ("sort_order", "icon", "title", "text")
    verbose_name = "Why choose us point"
    verbose_name_plural = "Why choose us points"


class FooterQuickLinkInline(SiteContentItemInline):
    section = SiteContentItem.Section.FOOTER_QUICK_LINK
    fields = ("sort_order", "label", "href")
    verbose_name = "Footer quick link"
    verbose_name_plural = "Footer quick links"


class FooterProductLinkInline(SiteContentItemInline):
    section = SiteContentItem.Section.FOOTER_PRODUCT_LINK
    fields = ("sort_order", "label", "href")
    verbose_name = "Footer product link"
    verbose_name_plural = "Footer product links"


class FooterLegalLinkInline(SiteContentItemInline):
    section = SiteContentItem.Section.FOOTER_LEGAL_LINK
    fields = ("sort_order", "label", "href")
    verbose_name = "Footer legal link"
    verbose_name_plural = "Footer legal links"


@admin.register(SiteContent)
class SiteContentAdmin(admin.ModelAdmin):
    inlines = (
        NavigationLinkInline,
        AboutPointInline,
        QualityPointInline,
        CommitmentPointInline,
        WhyPointInline,
        FooterQuickLinkInline,
        FooterProductLinkInline,
        FooterLegalLinkInline,
    )
    fieldsets = (
        ("Navigation bar", {
            "fields": ("logo_image", "nav_cta_label", "nav_cta_href"),
            "description": "Edit each navigation link in its own row below.",
        }),
        ("About section", {
            "fields": ("about_eyebrow", "about_title", "about_body"),
            "description": "Edit each About point in its own row below.",
        }),
        ("Quality assurance", {
            "fields": ("quality_eyebrow", "quality_background_image"),
            "description": "Edit each quality assurance point in its own row below.",
        }),
        ("Commitments", {
            "fields": ("commitments_title", "commitments_subtitle"),
            "description": "Edit each commitment in its own row below.",
        }),
        ("Why choose us", {
            "fields": ("why_eyebrow", "why_title", "why_body", "why_image"),
            "description": "Edit each Why Choose Us point in its own row below.",
        }),
        ("Footer", {
            "fields": (
                "footer_tagline",
                "footer_products_heading",
                "footer_copyright",
            ),
            "description": "Edit footer links in their own rows below.",
        }),
        ("Section images", {
            "fields": ("hero_image", "about_image", "contact_background_image"),
            "description": "Optional uploads replace the bundled defaults; leave an image empty to keep the current default.",
        }),
    )

    def has_add_permission(self, request):
        return not SiteContent.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ("name", "email", "company", "topic", "created_at")
    list_filter = ("created_at",)
    search_fields = ("name", "email", "company", "topic", "message")
    readonly_fields = ("created_at",)