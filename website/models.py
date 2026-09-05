from django.db import models
from django.templatetags.static import static
from django.urls import reverse


class Service(models.Model):
    ICON_CHOICES = [
        ('monitor', 'Monitor'),
        ('code', 'Code'),
        ('phone', 'Phone'),
        ('chart', 'Chart'),
        ('cart', 'Cart'),
        ('wrench', 'Wrench'),
    ]

    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    icon = models.CharField(max_length=40, choices=ICON_CHOICES)
    short_description = models.CharField(max_length=220)
    description = models.TextField()
    features = models.TextField(help_text='One feature per line')
    order = models.PositiveIntegerField(default=0)
    is_featured = models.BooleanField(default=True)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('website:service_detail', args=[self.slug])

    def feature_list(self):
        return [line.strip() for line in self.features.splitlines() if line.strip()]


class PortfolioProject(models.Model):
    CATEGORY_CHOICES = [
        ('business', 'Business'),
        ('ecommerce', 'E-commerce'),
        ('startup', 'Startup'),
        ('portfolio', 'Creative'),
        ('education', 'Education'),
    ]

    title = models.CharField(max_length=160)
    slug = models.SlugField(unique=True)
    category = models.CharField(max_length=40, choices=CATEGORY_CHOICES)
    client = models.CharField(max_length=120, blank=True)
    summary = models.CharField(max_length=240)
    description = models.TextField()
    cover_url = models.CharField(max_length=255)
    sample_url = models.URLField(blank=True)
    result = models.CharField(max_length=180, blank=True)
    year = models.PositiveIntegerField(default=2026)
    services = models.ManyToManyField(Service, blank=True, related_name='projects')
    is_featured = models.BooleanField(default=False)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order', '-year']

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('website:portfolio_detail', args=[self.slug])

    @property
    def cover_src(self):
        if self.cover_url.startswith(('http://', 'https://', '/')):
            return self.cover_url
        return static(self.cover_url)


class Testimonial(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=160)
    company = models.CharField(max_length=120)
    quote = models.TextField()
    rating = models.PositiveSmallIntegerField(default=5)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.name} - {self.company}'


class ProcessStep(models.Model):
    number = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=80)
    description = models.CharField(max_length=240)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return f'{self.number}. {self.title}'


class FAQ(models.Model):
    question = models.CharField(max_length=200)
    answer = models.TextField()
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    def __str__(self):
        return self.question


class TeamMember(models.Model):
    name = models.CharField(max_length=120)
    role = models.CharField(max_length=120)
    bio = models.CharField(max_length=240)
    initials = models.CharField(max_length=4)
    order = models.PositiveIntegerField(default=0)

    class Meta:
        ordering = ['order']

    def __str__(self):
        return self.name


class ContactInquiry(models.Model):
    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30, blank=True)
    subject = models.CharField(max_length=160)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']
        verbose_name_plural = 'Contact inquiries'

    def __str__(self):
        return f'{self.name}: {self.subject}'


class QuoteRequest(models.Model):
    BUDGET_CHOICES = [
        ('starter', 'Under ₹25,000'),
        ('growth', '₹25,000 - ₹75,000'),
        ('business', '₹75,000 - ₹2,00,000'),
        ('enterprise', '₹2,00,000+'),
        ('unsure', 'Not sure yet'),
    ]
    TIMELINE_CHOICES = [
        ('asap', 'As soon as possible'),
        ('1month', 'Within a month'),
        ('3months', '1-3 months'),
        ('flexible', 'Flexible'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=30)
    company = models.CharField(max_length=160, blank=True)
    service = models.ForeignKey(
        Service,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='quote_requests',
    )
    budget = models.CharField(max_length=20, choices=BUDGET_CHOICES)
    timeline = models.CharField(max_length=20, choices=TIMELINE_CHOICES)
    project_details = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_reviewed = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Quote from {self.name}'
