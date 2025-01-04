# CEDAV - Banking App

Banking application powered by NextJS and FastAPI. Connect in real time with your bank via Plaid APIs.

It lets you manage your budgets and spending categories, and several bank accounts can be connected at the same time and accessed by different users.

<img alt="Dashboard in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/dashboard_dark.png" />

## Application
Functionalities:
- Directly connected to your bank account to fetch bank data
- Automatically categorizes transactions
- Budgeting tools
- Expense tracking by category
- Multiple accounts connected

Technologies:
- NextJS
- Chakra UI
- TypeScript
- Vercel
- Plaid API
- Python
- Supabase
- Prisma ORM

Frontend Repository:
https://github.com/davidmonnom/banking-frontend

---

Please note that this application is not yet in production. If you try to connect to it, you'll get an access error.
However, you can download it and add your own API identifier via Google & Plaid.

## Setup

Here are the necessary environment variables to place in the .env file
```
DATABASE_URL="postgres database"

PLAID_REDIRECT_URI=https://cedav.be
PLAID_CLIENT_ID=
PLAID_SECRET=
PLAID_SANDBOX_SECRET=
PLAID_ENV=development
PLAID_PRODUCTS=transactions,auth

GOOGLE_CLIENT_ID=
GOOGLE_SECRET=
ALLOWED_USER="email addresses of allowed users"
```

Create a new python environment.
Install dependencies with `pip install -r requirement.txt`.
Start the server with `uvicorn app.main:app --port 1997 --host 0.0.0.0`.

Follow the frontend server installation instructions.

## Screenshots
#### Dashboard
<p float="left">
  <img alt="Dashboard in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/dashboard_light.png" width="300" />
  <img alt="Dashboard in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/dashboard_dark.png" width="300" />
</p>

#### Transaction
<p float="left">
  <img alt="Transaction in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/transaction_light.png" width="300" />
  <img alt="Transaction in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/transaction_dark.png" width="300" />
</p>

#### Category
<p float="left">
  <img alt="Category in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/category_light.png" width="300" />
  <img alt="Category in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/category_dark.png" width="300" />
</p>

#### Saving
<p float="left">
  <img alt="Saving in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/saving_light.png" width="300" />
  <img alt="Saving in dark and light mode" src="https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/saving_dark.png" width="300" />
</p>

## Video
[![Watch the video](https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/dashboard_dark.png)](https://github.com/davidmonnom/banking-frontend/blob/main/screenshots/cedav.mp4)
