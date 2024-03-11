import uuid
import MySQLdb

from db.models import ShortenedURL
from db.database import session
from celery_config import celery_app


def save_url(original_url: str, shortened_url: str) -> None:
    """
    Save URL object in the db
    """
    try:
        new_shortened_url = ShortenedURL(
            original_url=original_url, shortened_url=shortened_url
        )
        session.add(new_shortened_url)
        session.commit()

    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
        raise MySQLdb.OperationalError(error)

    except Exception as error:
        raise Exception(f"Problem with saving data in the database because - {error}")


def is_duplicate(original_url: str) -> bool:
    """
    Here we also check whether there are no duplicates in the database
    """
    existing_shortened_url = ShortenedURL.query.filter_by(
        original_url=original_url
    ).first()
    if existing_shortened_url:
        return True
    return False


@celery_app.task()
def process_shorten_url_task(original_url: str) -> tuple:
    """
    Celery task responsible for shortening the URL and saving it in the database.
    :return - We return information whether the URL is already in the database and if not, a shortened link
    """
    try:
        if is_duplicate(original_url=original_url):
            return True, ""

        shortened_url = "https://shortener/" + str(uuid.uuid4())[:8]
        save_url(original_url=original_url, shortened_url=shortened_url)
        return False, shortened_url

    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
        raise MySQLdb.OperationalError(error)

    except Exception as error:
        raise Exception(f"Problem with shortening the link - {error}")
