from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
import logging

from website.email_utils import format_contact_email, format_quote_email, notify_owner
from website.forms import ContactForm, QuoteForm
from website.models import FAQ, PortfolioProject, ProcessStep, Service, TeamMember, Testimonial

logger = logging.getLogger(__name__)


def home(request):
    context = {
        'page_title': 'Websites Today, Bigger Tomorrows',
        'featured_services': Service.objects.filter(is_featured=True)[:4],
        'featured_projects': PortfolioProject.objects.filter(is_featured=True)[:3],
        'testimonials': Testimonial.objects.all()[:3],
        'process_steps': ProcessStep.objects.all(),
    }
    return render(request, 'website/home.html', context)


def services(request):
    context = {
        'page_title': 'Services',
        'service_list': Service.objects.all(),
        'process_steps': ProcessStep.objects.all(),
    }
    return render(request, 'website/services.html', context)


def service_detail(request, slug):
    service = get_object_or_404(Service, slug=slug)
    related = Service.objects.exclude(pk=service.pk)[:3]
    context = {
        'page_title': service.title,
        'service': service,
        'related_services': related,
        'related_projects': service.projects.all()[:3],
    }
    return render(request, 'website/service_detail.html', context)


def portfolio(request):
    category = request.GET.get('category', '')
    projects = PortfolioProject.objects.all()
    if category:
        projects = projects.filter(category=category)
    context = {
        'page_title': 'Portfolio',
        'projects': projects,
        'active_category': category,
        'categories': PortfolioProject.CATEGORY_CHOICES,
    }
    return render(request, 'website/portfolio.html', context)


def portfolio_detail(request, slug):
    project = get_object_or_404(PortfolioProject, slug=slug)
    more_projects = PortfolioProject.objects.exclude(pk=project.pk)[:3]
    context = {
        'page_title': project.title,
        'project': project,
        'more_projects': more_projects,
    }
    return render(request, 'website/portfolio_detail.html', context)


def about(request):
    context = {
        'page_title': 'About',
        'team': TeamMember.objects.all(),
        'process_steps': ProcessStep.objects.all(),
        'faqs': FAQ.objects.all(),
    }
    return render(request, 'website/about.html', context)


def contact(request):
    form = ContactForm(request.POST or None)
    if request.method == 'POST' and form.is_valid():
        inquiry = form.save()
        try:
            text_body, html_body = format_contact_email(inquiry)
            notify_owner(
                subject=f'WebMarblow contact: {inquiry.subject}',
                text_body=text_body,
                html_body=html_body,
                reply_to=inquiry.email,
            )
        except Exception:
            logger.exception('Contact email failed')
        messages.success(
            request,
            'Thank you. We received your message and will reply within one business day.',
        )
        return redirect(reverse('website:contact'))

    context = {
        'page_title': 'Contact',
        'form': form,
        'faqs': FAQ.objects.all()[:4],
    }
    return render(request, 'website/contact.html', context)


def quote(request):
    initial = {}
    service_slug = request.GET.get('service')
    if service_slug:
        service = Service.objects.filter(slug=service_slug).first()
        if service:
            initial['service'] = service.pk

    form = QuoteForm(request.POST or None, initial=initial)
    if request.method == 'POST' and form.is_valid():
        quote_request = form.save()
        try:
            text_body, html_body = format_quote_email(quote_request)
            notify_owner(
                subject=f'WebMarblow quote request from {quote_request.name}',
                text_body=text_body,
                html_body=html_body,
                reply_to=quote_request.email,
            )
        except Exception:
            logger.exception('Quote email failed')
        messages.success(
            request,
            'Your quote request is in. We will send a tailored plan and estimate shortly.',
        )
        return redirect(reverse('website:quote'))

    context = {
        'page_title': 'Get a Quote',
        'form': form,
        'services': Service.objects.all(),
    }
    return render(request, 'website/quote.html', context)
