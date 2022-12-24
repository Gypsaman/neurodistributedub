from datetime import datetime as dt

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from webproject import db
from webproject.models import Assets
from webproject.web3_interface import get_eth_balance
from . import login_required

assets = Blueprint("assets", __name__)

# Asset Management
@assets.route("/assets")
@login_required
def assets_list():
    assets = Assets.query.filter_by(student_id=current_user.student_id).all()
    return render_template("assets.html", assets=assets)


@assets.route("/assets_table")
@login_required
def assets_table():
    assets_table = Assets.query.filter_by(student_id=current_user.student_id).all()
    return render_template("assets_table.html", assets=assets_table)


@assets.route("/assetdelete/<int:id>")
def assets_delete(id):
    addr = id
    asset_to_delete = Assets.query.get_or_404(id)
    try:
        db.session.delete(asset_to_delete)
        db.session.commit()
        return redirect("/assets")
    except:
        flash("There was a problem deleting the asset")
        return redirect("/assets")


@assets.route("/addassets")
@login_required
def add_assets():
    assignments = Assignments.query.all()
    return render_template("addassets.html", assignments=assignments)


@assets.route("/addassets", methods=["POST"])
@login_required
def add_assets_post():
    record = {
        "student_id": current_user.student_id,
        "asset_type": request.form.get("asset_type"),
        "network": request.form.get("network"),
        "asset_address": request.form.get("asset_address"),
        "assignment": request.form.get("assignment"),
        "time_added": dt.now(),
    }
    asset_exists = Assets.query.filter_by(asset_address=record["asset_address"]).first()
    if asset_exists:
        flash("Asset already exists")
        return redirect(url_for("assets.assets"))

    asset = Assets(**record)

    db.session.add(asset)
    db.session.commit()

    return redirect(url_for("assets.profile"))
