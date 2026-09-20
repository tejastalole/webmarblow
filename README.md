## Email quotes to Gmail

**Send message** and **Request my quote** email full details to `tejastalole7@gmail.com`.

### One-time activation (required)
1. Open Gmail for `tejastalole7@gmail.com`
2. Check **Inbox** and **Spam** for an email from **FormSubmit**
3. Click **Activate Form**
4. Submit Contact or Quote again — the lead email will arrive

### Stronger option (recommended): Resend
1. Create a free key at [resend.com](https://resend.com)
2. On Vercel → Settings → Environment Variables add:
   - `RESEND_API_KEY` = your key
   - `LEAD_NOTIFY_EMAIL` = `tejastalole7@gmail.com`
3. Redeploy

### Or Gmail SMTP
- `EMAIL_HOST_USER` = `tejastalole7@gmail.com`
- `EMAIL_HOST_PASSWORD` = Gmail [App Password](https://myaccount.google.com/apppasswords)
- Redeploy
