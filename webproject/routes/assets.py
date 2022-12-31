from datetime import datetime as dt

from flask import Blueprint, flash, redirect, render_template, request, url_for
from flask_login import current_user

from webproject import db
from webproject.models import Assets,Assignments,Wallet
from webproject.web3_interface import get_eth_balance, getContracts
from flask_login import login_required

assets = Blueprint("assets", __name__)

asset_types = {"NFT" : 1, "ERC20" : 2,"DAPP": 3}

# Asset Management
@assets.route("/assets")
@login_required
def assets_list():
    assets_t = Assets.query.filter_by(user_id=current_user.id).all()
    return render_template("assets/assets.html", assets=assets_t)


@assets.route('/addethassets')
def add_eth_assets():
    
    wallet = Wallet.query.filter_by(user_id=current_user.id).first()
    assets = getContracts(wallet.wallet)
    for asset in assets:
        
        contract = asset['contract']
        exists = Assets.query.filter_by(asset_address=contract).first()
        if exists:
            continue
        type = asset_types[asset['type']]
        
        new_asset = Assets(user_id=current_user.id, asset_type=type, network='goerli', asset_address=contract, time_added=dt.now(), assignment=None)
        db.session.add(new_asset)
        db.session.commit()
        
    return render_template('assets/assets_table.html')

@assets.route("/assets_table")
@login_required
def assets_table():
    assets_t = Assets.query.filter_by(user_id=current_user.id).all()
    return render_template("assets/assets_table.html", assets=assets_t)


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
    return render_template("assets/addassets.html", assignments=assignments)


@assets.route("/addassets", methods=["POST"])
@login_required
def add_assets_post():
    record = {
        "user_id": current_user.id,
        "asset_type": request.form.get("asset_type"),
        "network": request.form.get("network"),
        "asset_address": request.form.get("asset_address"),
        "assignment": request.form.get("assignment"),
        "time_added": dt.now(),
    }
    asset_exists = Assets.query.filter_by(asset_address=record["asset_address"]).first()
    if asset_exists:
        flash("Asset already exists")
        return redirect(url_for("assets.assets_list"))

    asset_record = Assets(**record)

    db.session.add(asset_record)
    db.session.commit()

    return redirect(url_for("main.profile"))
