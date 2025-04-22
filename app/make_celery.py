from app import create_app

# Windows: celery -A make_celery worker -l INFO -P solo
# ref: https://stackoverflow.com/a/78803901/23867578
flask_app = create_app()
celery_app = flask_app.extensions["celery"]
