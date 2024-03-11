import MySQLdb

from typing import Union
from flask import (
    Blueprint,
    request,
    jsonify,
    redirect,
    render_template,
)

from db.models import ShortenedURL
from worker.tasks import process_shorten_url_task

# Blueprint initialization for controllers
api = Blueprint("api", __name__)


@api.route("/shorten", methods=["GET"])
def redirect_to_original(shortened_url: str) -> Union[redirect, jsonify]:
    try:
        # Get the shortened URL from the database
        shortened_url_obj = ShortenedURL.query.filter_by(
            shortened_url=shortened_url
        ).first()

        # If exists, redirect to original URL, otherwise return 404
        if shortened_url_obj:
            return redirect(shortened_url_obj.original_url, code=302)
        return jsonify({"error": "URL not found"}), 404

    except Exception as error:
        raise Exception(f"Problem with redirect in /shorten GET endpoint - {error}")


@api.route("/", methods=["GET", "POST"])
def index():
    try:
        if request.method == "POST":
            # Get the original URL from the form
            original_url = request.form.get("original_url")

            # Run the celery task responsible for shortening the link and saving it in the database
            celery_task = process_shorten_url_task.delay(original_url=original_url)
            shortened_url_duplicate, shortened_url = celery_task.get(timeout=5)

            if shortened_url_duplicate is True:
                return jsonify({"warning": "This URL already exists in the database"}), 200

            # Return an asynchronous task response to the template
            return render_template(
                "index.html", original_url=original_url, shortened_url=shortened_url
            )
        else:
            return render_template("index.html")

    except (MySQLdb.ProgrammingError, MySQLdb.OperationalError) as error:
        raise MySQLdb.OperationalError(
            f"The database does not have a URL table. "
            f"Please make migration according to the documentation - {error}"
        )

    except Exception as error:
        raise Exception(f"Problem with / endpoint - {error}")
