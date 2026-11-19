import time
from collections import defaultdict, deque

from flask import Blueprint, current_app, redirect, render_template, request, url_for

from app import content
from app.forms import InquiryForm
from app.services.inquiry_service import InquiryService

bp = Blueprint("public", __name__)

# Per-worker, in-memory: good enough to blunt a form-spamming script.
_recent_submissions = defaultdict(deque)
_WINDOW_SECONDS = 3600


def _render_home(form, status=200):
    return render_template("index.html", form=form, c=content), status


@bp.route("/")
def index():
    return _render_home(InquiryForm())


@bp.route("/inquire", methods=["POST"])
def inquire():
    form = InquiryForm()

    if form.website.data:
        # Bot filled the honeypot; pretend it worked.
        current_app.logger.info("Dropped honeypot inquiry from %s", request.remote_addr)
        return redirect(url_for("public.thanks"))

    if not form.validate_on_submit():
        return _render_home(form, 400)

    if _rate_limited(request.remote_addr):
        form.form_errors.append(
            "We've received several inquiries from this connection in the last hour. "
            f"Email us at {content.BRAND['email']} instead."
        )
        return _render_home(form, 429)

    InquiryService(current_app.db).create(form.data)
    return redirect(url_for("public.thanks"))


@bp.route("/thanks")
def thanks():
    return render_template("thanks.html")


def _rate_limited(ip):
    limit = current_app.config["INQUIRY_RATE_LIMIT"]
    now = time.monotonic()
    hits = _recent_submissions[ip]
    while hits and now - hits[0] > _WINDOW_SECONDS:
        hits.popleft()
    if len(hits) >= limit:
        return True
    hits.append(now)
    return False
