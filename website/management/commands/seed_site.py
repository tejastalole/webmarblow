from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from website.models import (
    FAQ,
    PortfolioProject,
    ProcessStep,
    Service,
    TeamMember,
    Testimonial,
)


class Command(BaseCommand):
    help = 'Load demo services, projects, and site content for Webmarblow.'

    def handle(self, *args, **options):
        services = self._seed_services()
        self._seed_projects(services)
        self._seed_process()
        self._seed_testimonials()
        self._seed_faqs()
        self._seed_team()
        self._seed_admin()
        self.stdout.write(self.style.SUCCESS('Webmarblow demo content is ready.'))

    def _seed_services(self):
        items = [
            {
                'title': 'Custom Website Design',
                'slug': 'custom-website-design',
                'icon': 'monitor',
                'short_description': 'Clean layouts that look premium and make your offer easy to understand.',
                'description': (
                    'We design websites around your brand, your customers, and the action you want them to take. '
                    'Every page is planned for clarity first: what you do, who it is for, and why someone should choose you. '
                    'The result is a modern site that feels like your business - not a generic template.'
                ),
                'features': 'Brand-led visual system\nHomepage and inner-page layouts\nClear calls to action\nContent structure for conversion',
                'order': 1,
                'is_featured': True,
            },
            {
                'title': 'Web Development',
                'slug': 'web-development',
                'icon': 'code',
                'short_description': 'Fast, secure, and easy-to-update websites built to last.',
                'description': (
                    'We build production-ready websites with clean code, sensible structure, and a content admin your team can use. '
                    'From brochure sites to enquiry-driven platforms, we focus on reliability, speed, and future changes - '
                    'so you are not stuck when the business grows.'
                ),
                'features': 'Custom Django builds\nCMS-ready content\nContact and quote flows\nSecure hosting-ready code',
                'order': 2,
                'is_featured': True,
            },
            {
                'title': 'Mobile Responsive',
                'slug': 'mobile-responsive',
                'icon': 'phone',
                'short_description': 'Every screen works - phone, tablet, and desktop - without compromise.',
                'description': (
                    'Most of your visitors will arrive on a phone. We design mobile first so buttons are easy to tap, '
                    'text is readable, and key pages load quickly. Then we refine the desktop experience so it still feels generous and premium.'
                ),
                'features': 'Mobile-first layouts\nTouch-friendly navigation\nFast image delivery\nConsistent brand across devices',
                'order': 3,
                'is_featured': True,
            },
            {
                'title': 'SEO Friendly',
                'slug': 'seo-friendly',
                'icon': 'chart',
                'short_description': 'Technical SEO and content structure that help people find you.',
                'description': (
                    'A beautiful website that nobody can find is unfinished work. We set up clean URLs, page titles, '
                    'meta descriptions, heading structure, and performance basics so search engines can understand your pages. '
                    'Then we help you plan content that matches what customers actually search for.'
                ),
                'features': 'On-page SEO setup\nFast page performance\nSitemap-ready structure\nLocal business visibility basics',
                'order': 4,
                'is_featured': True,
            },
            {
                'title': 'E-commerce Websites',
                'slug': 'ecommerce-websites',
                'icon': 'cart',
                'short_description': 'Product catalogues and checkout journeys that feel simple to buy from.',
                'description': (
                    'We create storefronts that make products easy to browse and purchase. From category pages to enquiry-led catalogues, '
                    'we keep the journey short and trustworthy so customers do not drop off on mobile.'
                ),
                'features': 'Product listing pages\nClear product detail layouts\nEnquiry or checkout flows\nMobile shopping experience',
                'order': 5,
                'is_featured': False,
            },
            {
                'title': 'Website Care',
                'slug': 'website-care',
                'icon': 'wrench',
                'short_description': 'Updates, backups, and small improvements after launch.',
                'description': (
                    'Launch is the start. We stay available for content updates, security patches, performance checks, '
                    'and the small changes that keep a website useful as your offers evolve.'
                ),
                'features': 'Content updates\nSecurity and backups\nPerformance reviews\nMonthly improvement notes',
                'order': 6,
                'is_featured': False,
            },
        ]
        created = {}
        for item in items:
            obj, _ = Service.objects.update_or_create(slug=item['slug'], defaults=item)
            created[item['slug']] = obj
        return created

    def _seed_projects(self, services):
        items = [
            {
                'title': 'Northline Interiors',
                'slug': 'northline-interiors',
                'category': 'business',
                'client': 'Northline Interiors',
                'summary': 'A calm studio site that turns walk-in curiosity into booked consultations.',
                'description': (
                    'Northline needed a site that showed finished rooms without looking like a photo dump. '
                    'We built a project-led homepage, a filtered gallery, and a simple consultation form. '
                    'The new site made it obvious who they serve and how to start a project.'
                ),
                'cover_url': 'website/img/portfolio/northline-interiors.jpg',
                'sample_url': 'https://northline-interiors-web-marblow.vercel.app/',
                'result': 'Consultation requests up after relaunch',
                'year': 2026,
                'is_featured': True,
                'order': 1,
                'service_slugs': ['custom-website-design', 'web-development'],
            },
            {
                'title': 'Harvest Basket',
                'slug': 'harvest-basket',
                'category': 'ecommerce',
                'client': 'Harvest Basket',
                'summary': 'A farm-to-home storefront with clear products and a frictionless mobile cart.',
                'description': (
                    'Harvest Basket sells weekly produce boxes. We designed category pages that feel fresh, '
                    'product cards that show origin and price at a glance, and a checkout path that works on a phone in one hand.'
                ),
                'cover_url': 'website/img/portfolio/harvest-basket.jpg',
                'result': 'Higher mobile add-to-cart rate',
                'year': 2025,
                'is_featured': True,
                'order': 2,
                'service_slugs': ['ecommerce-websites', 'mobile-responsive'],
            },
            {
                'title': 'Pulse Labs',
                'slug': 'pulse-labs',
                'category': 'startup',
                'client': 'Pulse Labs',
                'summary': 'A product site that explains a complex tool in a one-minute story.',
                'description': (
                    'Pulse Labs had a strong product and a confusing homepage. We rewrote the narrative, '
                    'added a simple demo request flow, and designed a visual system that feels technical without being cold.'
                ),
                'cover_url': 'website/img/portfolio/pulse-labs.jpg',
                'result': 'Demo requests became the main lead source',
                'year': 2026,
                'is_featured': True,
                'order': 3,
                'service_slugs': ['custom-website-design', 'seo-friendly'],
            },
            {
                'title': 'Atelier Nova',
                'slug': 'atelier-nova',
                'category': 'portfolio',
                'client': 'Atelier Nova',
                'summary': 'A photography portfolio that loads fast and still feels editorial.',
                'description': (
                    'The brief was simple: let the work breathe. We used large images, restrained type, '
                    'and a contact path that does not interrupt the gallery. Performance work kept the visual quality without slow pages.'
                ),
                'cover_url': 'website/img/portfolio/atelier-nova.jpg',
                'result': 'Faster pages with larger images',
                'year': 2025,
                'is_featured': False,
                'order': 4,
                'service_slugs': ['custom-website-design', 'mobile-responsive'],
            },
            {
                'title': 'BrightPath Academy',
                'slug': 'brightpath-academy',
                'category': 'education',
                'client': 'BrightPath Academy',
                'summary': 'Course pages and enquiry forms that help parents decide with confidence.',
                'description': (
                    'BrightPath needed parents to understand programmes quickly. We organised courses by age group, '
                    'added faculty and outcome sections, and built an enquiry form that captures the right details for admissions.'
                ),
                'cover_url': 'website/img/portfolio/brightpath-academy.jpg',
                'result': 'Clearer programme enquiries',
                'year': 2025,
                'is_featured': False,
                'order': 5,
                'service_slugs': ['web-development', 'seo-friendly'],
            },
            {
                'title': 'Urban Roast Co.',
                'slug': 'urban-roast-co',
                'category': 'business',
                'client': 'Urban Roast Co.',
                'summary': 'A café brand site with locations, menus, and a wholesale enquiry path.',
                'description': (
                    'Urban Roast wanted one place for café visitors and wholesale buyers. We split those journeys clearly, '
                    'kept the brand warm, and made location and menu updates easy for the team.'
                ),
                'cover_url': 'website/img/portfolio/urban-roast-co.jpg',
                'result': 'Wholesale enquiries from the website',
                'year': 2024,
                'is_featured': False,
                'order': 6,
                'service_slugs': ['custom-website-design', 'website-care'],
            },
        ]

        for item in items:
            slugs = item.pop('service_slugs')
            obj, _ = PortfolioProject.objects.update_or_create(slug=item['slug'], defaults=item)
            obj.services.set([services[slug] for slug in slugs if slug in services])

    def _seed_process(self):
        steps = [
            (1, 'Discover', 'We learn your offer, customers, and what a successful website should achieve.'),
            (2, 'Design', 'We shape the pages, words, and visuals so the site feels like your brand.'),
            (3, 'Develop', 'We build a fast, responsive site your team can update with confidence.'),
            (4, 'Grow', 'We launch, measure, and keep improving so the website keeps earning its place.'),
        ]
        for number, title, description in steps:
            ProcessStep.objects.update_or_create(
                number=number,
                defaults={'title': title, 'description': description, 'order': number},
            )

    def _seed_testimonials(self):
        items = [
            {
                'name': 'Meera Kulkarni',
                'role': 'Founder',
                'company': 'Northline Interiors',
                'quote': 'Webmarblow made our work look as considered as the rooms we design. Clients now arrive already trusting us.',
                'rating': 5,
                'order': 1,
            },
            {
                'name': 'Arjun Shah',
                'role': 'Operations Lead',
                'company': 'Harvest Basket',
                'quote': 'The store finally works on phones the way our customers shop. Orders are cleaner and we spend less time explaining products.',
                'rating': 5,
                'order': 2,
            },
            {
                'name': 'Priya Nair',
                'role': 'Co-founder',
                'company': 'Pulse Labs',
                'quote': 'They turned a technical product into a clear story. Demo requests started coming from the homepage within weeks.',
                'rating': 5,
                'order': 3,
            },
        ]
        for item in items:
            Testimonial.objects.update_or_create(name=item['name'], company=item['company'], defaults=item)

    def _seed_faqs(self):
        items = [
            (
                'How long does a typical website take?',
                'Most brochure sites take 3 to 6 weeks from brief to launch. Stores and custom tools take longer depending on pages, integrations, and content readiness.',
            ),
            (
                'Do you write the website copy as well?',
                'Yes. We can shape headlines, service pages, and calls to action with you. If you already have copy, we edit it so it reads clearly on the site.',
            ),
            (
                'Will I be able to update the site myself?',
                'Yes. Content you change often - services, projects, FAQs, and enquiries - lives in the Django admin. We show you how to use it before launch.',
            ),
            (
                'Do you work with businesses outside Pune?',
                'Yes. We work remotely across India. Kickoff, reviews, and launch can all happen online.',
            ),
            (
                'What do I need to get started?',
                'A short note about your business, who you want to reach, and any sites you like. If you have a logo and photos, even better. We handle the rest.',
            ),
            (
                'Can you improve an existing website?',
                'Yes. We can redesign, rebuild, or fix the parts that are slowing you down - mobile layout, speed, enquiry forms, or SEO structure.',
            ),
        ]
        for index, (question, answer) in enumerate(items, start=1):
            FAQ.objects.update_or_create(question=question, defaults={'answer': answer, 'order': index})

    def _seed_team(self):
        items = [
            {
                'name': 'Design Studio',
                'role': 'Visual & UX',
                'bio': 'Layouts, type, and brand systems that make a first visit feel confident.',
                'initials': 'DS',
                'order': 1,
            },
            {
                'name': 'Build Team',
                'role': 'Django Development',
                'bio': 'Clean code, admin tools, and sites that stay fast after launch.',
                'initials': 'BT',
                'order': 2,
            },
            {
                'name': 'Growth Desk',
                'role': 'SEO & Content',
                'bio': 'Page structure and messaging that help the right people find you.',
                'initials': 'GD',
                'order': 3,
            },
        ]
        for item in items:
            TeamMember.objects.update_or_create(name=item['name'], defaults=item)

    def _seed_admin(self):
        user_model = get_user_model()
        user = user_model.objects.filter(username='admin').first() or user_model.objects.filter(username='root').first()
        if user:
            user.username = 'root'
            user.set_password('root')
            user.is_staff = True
            user.is_superuser = True
            user.save()
        else:
            user_model.objects.create_superuser(
                username='root',
                email='hello@webmarblow.com',
                password='root',
            )
        self.stdout.write('Admin user is root / root')
