# Webmarblow

Django website for Webmarblow, a studio that designs and builds websites for growing businesses.

## Run locally

```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python manage.py migrate
python manage.py seed_site
python manage.py runserver
```

Open [http://127.0.0.1:8000](http://127.0.0.1:8000).

Admin: [http://127.0.0.1:8000/admin](http://127.0.0.1:8000/admin)  
Username: `root`  
Password: `root`

## What is included

- Home, Services, Portfolio, About, Contact, and Get Quote pages
- Enquiry and quote forms saved in the database
- Django admin for services, projects, testimonials, FAQs, and leads
- Demo content via `python manage.py seed_site`
