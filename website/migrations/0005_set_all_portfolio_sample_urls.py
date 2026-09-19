from django.db import migrations

SAMPLE_URLS = {
    'northline-interiors': 'https://northline-interiors-web-marblow.vercel.app/',
    'harvest-basket': 'https://harvest-basket-web-marblow.vercel.app/',
    'pulse-labs': 'https://pulse-labs-web-marblow.vercel.app/',
    'atelier-nova': 'https://atelier-nova-web-marblow.vercel.app/',
    'brightpath-academy': 'https://brightpathacademy-web-marblow.vercel.app/',
    'urban-roast-co': 'https://urban-roast-co-web-marblo.vercel.app/',
}


def set_sample_urls(apps, schema_editor):
    PortfolioProject = apps.get_model('website', 'PortfolioProject')
    for slug, url in SAMPLE_URLS.items():
        PortfolioProject.objects.filter(slug=slug).update(sample_url=url)


def clear_sample_urls(apps, schema_editor):
    PortfolioProject = apps.get_model('website', 'PortfolioProject')
    PortfolioProject.objects.filter(slug__in=SAMPLE_URLS.keys()).update(sample_url='')


class Migration(migrations.Migration):

    dependencies = [
        ('website', '0004_service_is_active_service_price'),
    ]

    operations = [
        migrations.RunPython(set_sample_urls, clear_sample_urls),
    ]
