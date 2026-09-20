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

Quote and contact forms email full details to `tejastalole7@gmail.com`.

On Vercel, add these environment variables:

- `EMAIL_HOST_USER` = `tejastalole7@gmail.com`
- `EMAIL_HOST_PASSWORD` = your Gmail [App Password](https://myaccount.google.com/apppasswords)
- `LEAD_NOTIFY_EMAIL` = `tejastalole7@gmail.com` (optional)
- `DEFAULT_FROM_EMAIL` = `tejastalole7@gmail.com` (optional)

Without `EMAIL_HOST_PASSWORD`, emails print to the server log only (local/console mode).

