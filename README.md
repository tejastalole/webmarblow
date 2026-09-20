# WebMarblow

Django website for WebMarblow — websites for growing businesses.

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

## Email setup (required for live site)

**Send message** and **Request my quote** email full form details to `tejastalole7@gmail.com`.

### 1. Create a Gmail App Password
1. Open [Google Account → Security](https://myaccount.google.com/security)
2. Turn on **2-Step Verification** (required)
3. Open [App Passwords](https://myaccount.google.com/apppasswords)
4. Create one named `WebMarblow` and copy the 16-character password

### 2. Add env vars on Vercel
Project → **Settings** → **Environment Variables** (Production):

| Name | Value |
| --- | --- |
| `EMAIL_HOST_USER` | `tejastalole7@gmail.com` |
| `EMAIL_HOST_PASSWORD` | *(the 16-char App Password)* |
| `LEAD_NOTIFY_EMAIL` | `tejastalole7@gmail.com` |
| `DEFAULT_FROM_EMAIL` | `tejastalole7@gmail.com` |

### 3. Redeploy
Deployments → Redeploy the latest production deployment.

### 4. Test
Submit Contact or Quote once. You should get an email with every field (name, email, phone, subject/service, budget, timeline, message).

Without `EMAIL_HOST_PASSWORD`, forms still save in Admin, but no email is sent.
