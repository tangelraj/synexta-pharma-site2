# Synexta Pharma

A responsive React and Django implementation of the supplied Synexta Pharma landing-page design.

## Requirements

- Node.js 18 or newer
- Python 3.10 or newer

## Run locally

Install the frontend dependencies and Django package:

```powershell
npm install
python -m pip install -r requirements.txt
```

Start the Django API and Vite frontend together:

```powershell
npm run dev
```

Open the Vite URL printed in the terminal, normally `http://localhost:5173`. Vite proxies `/api` requests to Django at `http://127.0.0.1:8000`.

Create the local SQLite database before using the admin site or viewing saved inquiries:

```powershell
python ".\synext_backend\manage.py" migrate
python ".\synext_backend\manage.py" createsuperuser
```

The admin site is at `http://127.0.0.1:8000/admin/`. Contact inquiries are stored in `synext_backend/db.sqlite3` and can be reviewed there.

To manage the website catalogue, sign in to the admin site and open **Products**. Add products with a name, description, category and display order; the ID is generated from the name and can be adjusted if needed. Edit or delete products from the same list.

To edit the navigation bar, About section, Quality Assurance section, Commitments section, Why Choose Us section, or footer, open **Website content**. This is a single shared record; edits are reflected on the website when it reloads. Repeating items appear as individual rows: navigation and footer links have label and destination fields, while About, Quality Assurance, Commitments, and Why Choose Us points have icon, title, and text fields. Use the order field to arrange rows.

To change the site images, use the image upload fields on **Website content** for the logo, hero, About, Quality Assurance/Commitments background, Why Choose Us, and contact banner. To change a product image, open that product under **Products** and upload an image. Leaving an image empty uses the bundled site default (or, for products, the original product image). Uploads are stored under `synext_backend/media/`; back up and persist this folder along with the database.

## API

- `GET /api/products/` returns the product catalogue.
- `GET /api/content/` returns the editable website section content.
- `POST /api/contact/` accepts JSON with `name`, `email`, `phone`, `topic` and `message`; valid inquiries are stored in SQLite.

Run the backend tests with:

```powershell
python ".\synext_backend\manage.py" test inquiries
```

Contact enquiry notifications are emailed to `tangelraj@gmail.com`. Configure an SMTP sender account before submitting enquiries. For Gmail, use an app password (not your regular account password) and set these environment variables in the terminal before starting Django:

```powershell
$env:EMAIL_HOST_USER = "your-sender@gmail.com"
$env:EMAIL_HOST_PASSWORD = "your-gmail-app-password"
$env:DEFAULT_FROM_EMAIL = $env:EMAIL_HOST_USER
$env:INQUIRY_NOTIFICATION_EMAIL = "tangelraj@gmail.com"
npm run dev
```

Keep the sender app password private; do not put it in source control or share it in chat. The SMTP host defaults to Gmail (`smtp.gmail.com`, port `587`, TLS enabled). For another mail provider, also set `EMAIL_HOST`, `EMAIL_PORT`, and `EMAIL_USE_TLS`. If SMTP is not configured or delivery fails, the inquiry is still saved in the admin and the form reports that the notification email was not sent.

## Vercel and Render deployment

Vercel hosts the frontend; Django must run as a separate backend service. This repository includes a Render Blueprint in `render.yaml` and Vercel rewrites in `vercel.json` for the Render service named `synexta-pharma-api`.

1. In Render, choose **New → Blueprint**, connect this GitHub repository, and deploy the `render.yaml` Blueprint. Set `EMAIL_HOST_USER`, `EMAIL_HOST_PASSWORD`, and `DEFAULT_FROM_EMAIL` in the Render service environment before expecting enquiry notifications to arrive.
2. To create the first admin on Render's free plan (which does not include Shell access), add these environment variables to the Render service:
   - `DJANGO_SUPERUSER_USERNAME`: a new admin username
   - `DJANGO_SUPERUSER_EMAIL`: the admin email address
   - `DJANGO_SUPERUSER_PASSWORD`: a strong, unique password

   Save the variables and wait for the service to redeploy. The startup command creates the admin only if that username is not already present; it never resets an existing account's password. Keep the password in Render's environment settings, not in source code or chat. If the username already belongs to a non-admin account, choose another username. The free service's SQLite database is ephemeral, so the admin can be recreated from these variables if the database is lost.
3. Redeploy the Vercel project after the Render service is available. The rewrites send `/api/` and `/media/` requests to `https://synexta-pharma-site1.onrender.com`; the Django admin is at `https://synexta-pharma-site1.onrender.com/admin/`.

The included Render service collects and serves Django static assets through WhiteNoise. It uses the free plan for testing. Its local SQLite database and uploaded images are ephemeral and can be lost when the service restarts or redeploys; Render's free service may also sleep when idle. Do not use this configuration for production admin content or inquiries without moving to persistent database and file storage. For production, configure durable database/media storage and update the Render and Vercel deployment settings accordingly.

The frontend-only Vercel deployment cannot process enquiries until the Render backend is deployed and healthy. Contact submissions return a clear message if SMTP is not configured or mail delivery fails.
