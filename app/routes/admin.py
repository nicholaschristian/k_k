from urllib.parse import urlparse

from flask import Blueprint, abort, current_app, flash, redirect, render_template, request, url_for
from flask_login import login_required, login_user, logout_user

from app import content
from app.auth import AdminUser
from app.forms import LoginForm
from app.services.inquiry_service import STATUSES, InquiryService

bp = Blueprint("admin", __name__, url_prefix="/admin")

EVENT_TYPE_LABELS = dict(content.EVENT_TYPES)
PACKAGE_LABELS = dict(content.PACKAGE_CHOICES)


@bp.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = AdminUser.authenticate(form.email.data, form.password.data)
        if user:
            login_user(user, remember=True)
            target = request.args.get("next")
            if not target or urlparse(target).netloc or not target.startswith("/"):
                target = url_for("admin.inquiries")
            return redirect(target)
        form.form_errors.append("That email and password don't match.")
    return render_template("admin/login.html", form=form)


@bp.route("/logout", methods=["POST"])
@login_required
def logout():
    logout_user()
    return redirect(url_for("admin.login"))


@bp.route("/")
@login_required
def inquiries():
    status = request.args.get("status")
    service = InquiryService(current_app.db)
    return render_template(
        "admin/inquiries.html",
        inquiries=service.list(status),
        counts=service.counts(),
        active_status=status if status in STATUSES else None,
        statuses=STATUSES,
        event_labels=EVENT_TYPE_LABELS,
        package_labels=PACKAGE_LABELS,
    )


@bp.route("/inquiries/<inquiry_id>/status", methods=["POST"])
@login_required
def set_status(inquiry_id):
    status = request.form.get("status")
    if status not in STATUSES:
        abort(400)
    if not InquiryService(current_app.db).set_status(inquiry_id, status):
        abort(404)
    flash(f"Marked as {status}.", "success")
    return redirect(url_for("admin.inquiries", status=request.form.get("filter") or None))
