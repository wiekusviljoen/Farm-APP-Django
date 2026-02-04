# Project Name : Farm Application

# Description : This Farm application is used to register cattle herds, feed costs, sick animals, etc. It now includes an AI-powered chatbot that provides expert farming advice.

# Features:
- Farm management and cattle herd tracking
- Feed cost calculations and analysis
- Sick animal management
- Live abattoir price updates
- **NEW: AI Chatbot for farming advice** 🤖

# Table of Contents : 

[Installation](https://github.com/wiekusviljoen/Farm-APP-Django/blob/main/README.md#installation-)
[Chatbot Setup](https://github.com/wiekusviljoen/Farm-APP-Django/blob/main/README.md#ai-chatbot-setup-)
[Usage](https://github.com/wiekusviljoen/Farm-APP-Django/blob/main/README.md#usage-)
[Credits](https://github.com/wiekusviljoen/Farm-APP-Django/blob/main/README.md#credits-)

# Installation :

Installation steps

git clone https://github.com/wiekusviljoen/Farm-APP-Django.git

cd Farm-APP-Django

pip install -r requirements.txt

python manage.py runserver

# AI Chatbot Setup :

The application includes an AI-powered chatbot for farming advice powered by OpenAI.

## Quick Setup (5 minutes):

1. **Get API Key**: https://platform.openai.com/api-keys
2. **Configure**: Set environment variable `OPENAI_API_KEY=sk-your-key`
3. **Migrate**: `python manage.py migrate`
4. **Visit**: http://localhost:8000/chatbot/

## Features:
- 💬 Ask questions about cattle feeding, breeding, health, and farm management
- 🌾 Farm-specific advice based on your herd data
- 💾 Conversation history auto-saved
- 📱 Mobile-friendly interface
- ⚡ Real-time AI responses

## Full Documentation:
- Quick Start: See [QUICK_START.md](QUICK_START.md) (5 min read)
- Setup Guide: See [CHATBOT_SETUP.md](CHATBOT_SETUP.md) (30 min read)
- Technical Details: See [CHATBOT_IMPLEMENTATION.md](CHATBOT_IMPLEMENTATION.md)

**Important**: OpenAI API has associated costs. Monitor usage at https://platform.openai.com/usage

# Usage :

Here is the login page where you can login in if you have already registered. If not, then click register:

![Login](https://github.com/wiekusviljoen/Farm-APP-Django/assets/92153476/58c2f811-df4a-4c9a-bc6e-b2d6292834ba)


This is the register page where a new user can register:

![farm_register](https://github.com/wiekusviljoen/Farm-APP-Django/assets/92153476/8278dcf1-73ee-4322-bb33-4b4ebb3f26ff)


When logged in this is the Home page where all farms is listed that is registered:

![farmLists](https://github.com/wiekusviljoen/Farm-APP-Django/assets/92153476/4a667344-de0d-499c-938b-6fedf4fb34c4)


This is where the user can see the dashboard:

![Farm_dashboard](https://github.com/wiekusviljoen/Farm-APP-Django/assets/92153476/1e41439a-2468-4e63-af53-7ca734dfc22b)


This is where the administrator can register herds etc.

![farm_admin](https://github.com/wiekusviljoen/Farm-APP-Django/assets/92153476/55ff0c4e-8962-4307-b322-12a206e6bd74)


# Credits : 

Author : Petrus Viljoen

Bootcamp : HyperionDev : https://www.hyperiondev.com/

https://github.com/wiekusviljoen/Farm-APP-Django

---

## External feed price API (optional)
If you want the app to fetch live feed prices, set the following environment variables (example in `.env` or your host env):

- `FEED_PRICE_API_URL` — URL of the feed-price endpoint returning JSON.
- `FEED_PRICE_API_KEY` — API key (optional). By default it will be sent as `Authorization: Bearer <key>`.
- `FEED_PRICE_API_KEY_QUERY_PARAM` — instead of header, name of query param to add the key (e.g. `api_key`).
- `FEED_PRICE_JSON_PATH` — dot-path to the price value in the JSON response (default: `price`).
- `FEED_PRICE_AUTODISCOVER` — set to `False` to disable attempts to query public provider endpoints automatically.
- `FEED_PRICE_DEMO` — when `True` and no provider responds, a randomized demo price will be used for testing.

Add these to `.env` or your deployment environment. See `.env.example` for a template.


## Abattoir automatic polling
If you want abattoir prices polled automatically, you have two simple options:

1) django-crontab (recommended for quick deployments)

- Ensure `django-crontab` is installed in your environment (example in the project virtualenv):

  pip install django-crontab

- The project will automatically append `django_crontab` to `INSTALLED_APPS` when the
  `ABATTOIR_PRICE_POLL_ENABLED` environment variable is `True` (default), and sets a
  `CRONJOBS` entry to run `fetch_abattoir_prices` every `ABATTOIR_PRICE_POLL_INTERVAL_MINUTES`.

- To enable scheduling:
  - python manage.py crontab add
  - To list installed cron jobs: python manage.py crontab show
  - To remove: python manage.py crontab remove

2) System scheduler (cron / Windows Task Scheduler)

- Alternatively, run the management command on your host using cron (Linux/macOS):

  */15 * * * * /path/to/venv/bin/python /path/to/project/manage.py fetch_abattoir_prices

  Or with Windows Task Scheduler, create a scheduled task that runs the same command on your preferred interval.

Notes:
- The management command `fetch_abattoir_prices` will call each active abattoir's configured `api_url` and update its `last_prices` and `last_fetched` fields.
- You can still run the command manually to force an immediate refresh:

  python manage.py fetch_abattoir_prices

