from django.contrib import admin

from website.models import (
    FAQ,
    ContactInquiry,
    PortfolioProject,
    ProcessStep,
    QuoteRequest,
    Service,
    TeamMember,
    Testimonial,
)


@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('title', 'icon', 'is_featured', 'order')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'short_description')


@admin.register(PortfolioProject)
class PortfolioProjectAdmin(admin.ModelAdmin):
    list_display = ('title', 'category', 'year', 'is_featured', 'order')
    list_filter = ('category', 'is_featured', 'year')
    list_editable = ('is_featured', 'order')
    prepopulated_fields = {'slug': ('title',)}
    search_fields = ('title', 'client', 'summary')
    filter_horizontal = ('services',)
    fields = (
        'title',
        'slug',
        'category',
        'client',
        'summary',
        'description',
        'cover_url',
        'sample_url',
        'result',
        'year',
        'services',
        'is_featured',
        'order',
    )


@admin.register(Testimonial)
class TestimonialAdmin(admin.ModelAdmin):
    list_display = ('name', 'company', 'rating', 'order')
    list_editable = ('order',)


@admin.register(ProcessStep)
class ProcessStepAdmin(admin.ModelAdmin):
    list_display = ('number', 'title', 'order')
    list_editable = ('order',)


@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    list_display = ('question', 'order')
    list_editable = ('order',)


@admin.register(TeamMember)
class TeamMemberAdmin(admin.ModelAdmin):
    list_display = ('name', 'role', 'order')
    list_editable = ('order',)


@admin.register(ContactInquiry)
class ContactInquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject', 'created_at', 'is_read')
    list_filter = ('is_read', 'created_at')
    search_fields = ('name', 'email', 'subject', 'message')
    list_editable = ('is_read',)
    readonly_fields = ('name', 'email', 'phone', 'subject', 'message', 'created_at')


@admin.register(QuoteRequest)
class QuoteRequestAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'service', 'budget', 'timeline', 'created_at', 'is_reviewed')
    list_filter = ('budget', 'timeline', 'is_reviewed', 'created_at')
    search_fields = ('name', 'email', 'company', 'project_details')
    list_editable = ('is_reviewed',)
    readonly_fields = (
        'name',
        'email',
        'phone',
        'company',
        'service',
        'budget',
        'timeline',
        'project_details',
        'created_at',
    )
