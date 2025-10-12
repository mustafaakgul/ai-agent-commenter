# Product::AI Agent Commenter
* Description: An AI-powered agent that analyzes and generates meaningful comments based on content context

## Technology Stack
* Python, Django and FastAPI Technologies: Development
* Figma: Design and Project Development
* Postman, DRF UI, Swagger: API Observation
* PyCharm: IDE
* Slack: Team Communication, Project Management, Collaboration, Notification

## To Run Application
* Local:
  * Add and Set Up Python Interpreter in Settings
  * python3 -m venv .venv
  * source .venv/bin/activate
  * which python
  * python -version
  * pip install -r requirements.txt (pip freeze > requirements.txt)
  * python manage.py makemigrations
  * python manage.py migrate
  * python manage.py collectstatic
  * python manage.py createsuperuser, Test(admin-admin)
  * ipconfig getifaddr en0 1
  * python manage.py runserver 192.168.1.11:8000
* Dev: Heroku
* Production: Domain and Allowed Host, Debug False, Hide Secret Key, https://docs.djangoproject.com/en/5.2/howto/deployment/, https://github.com/heroku/python-getting-started/blob/main/gettingstarted/settings.py
