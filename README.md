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

## Email quotes to Gmail

**Send message** and **Request my quote** email full details to `tejastalole7@gmail.com`.

### Works without SMTP (FormSubmit)
1. Submit the Contact or Quote form once on the live site.
2. Open `tejastalole7@gmail.com` and confirm the FormSubmit activation email (first time only).
3. Later submissions will arrive in Gmail.

### Optional: Gmail SMTP (more reliable)
On Vercel → Project → Settings → Environment Variables:

- `EMAIL_HOST_USER` = `tejastalole7@gmail.com`
- `EMAIL_HOST_PASSWORD` = Gmail [App Password](https://myaccount.google.com/apppasswords)
- `LEAD_NOTIFY_EMAIL` = `tejastalole7@gmail.com`

Then redeploy.

