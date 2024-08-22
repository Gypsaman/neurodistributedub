# from datetime import datetime as dt

# from flask import Blueprint, flash, redirect, render_template, request, url_for
# from flask_login import current_user

# from webproject import db
# from webproject.models import Assets,Assignments,Wallet
# from webproject.modules.web3_interface import get_eth_balance, getContracts
# from flask_login import login_required

# from webproject.modules.table_creator import TableCreator, Field,asset_type_string,timestamp_to_date

# assets = Blueprint("assets", __name__)

# asset_types = {"NFT" : 2, "ERC20" : 1,"DAPP": 3}

# # Asset Management
# @assets.route("/assets/<int:page_num>")
# @login_required
# def assets_list(page_num):
#     fields = {
#         'id': Field(None,None),
#         'asset_type': Field(asset_type_string,'Type'),
#         'network': Field(None,'Network'),
#         'asset_address': Field(None,'Address'),
#         'time_added': Field(timestamp_to_date,'Added On'),
#         'assignment': Field(None,'Assignment')
#     }
#     table_creator = TableCreator("Assets", fields, condition=f"user_id={current_user.id}",actions=["View", "Delete","Edit"])
#     table_creator.set_items_per_page(10)
#     table_creator.create_view()
#     table = table_creator.create(page_num)
    
#     return render_template("assets/assets.html", table=table)

# @assets.route("/assets/noview/<int:page_num>")
# @login_required
# def noview(page_num):
#     return render_template("assets/noview.html",page_num=page_num)

# @assets.route('/addethassets')
# @login_required
# def add_eth_assets():
    
#     wallet = Wallet.query.filter_by(user_id=current_user.id).first()
#     assets = getContracts(wallet.wallet)
#     for asset in assets:
        
#         contract = asset['contract']
#         exists = Assets.query.filter_by(asset_address=contract).first()
#         if exists:
#             continue
#         type = asset_types[asset['type']]
        
#         new_asset = Assets(user_id=current_user.id, asset_type=type, network='sepolia', asset_address=contract, time_added=dt.now(), assignment=None)
#         db.session.add(new_asset)
#         db.session.commit()
        
#     return render_template('assets/assets_table.html')


# @assets.route("/assetdelete/<int:id>")
# @login_required
# def assets_delete(id):
#     addr = id
#     asset_to_delete = Assets.query.get_or_404(id)
#     try:
#         db.session.delete(asset_to_delete)
#         db.session.commit()
#         return redirect("/assets")
#     except:
#         flash("There was a problem deleting the asset")
#         return redirect("/assets")


# @assets.route("/addassets")
# @login_required
# def add_assets():
#     assignments = Assignments.query.all()
#     return render_template("assets/addassets.html", assignments=assignments)


# @assets.route("/addassets", methods=["POST"])
# @login_required
# def add_assets_post():
#     record = {
#         "user_id": current_user.id,
#         "asset_type": request.form.get("asset_type"),
#         "network": request.form.get("network"),
#         "asset_address": request.form.get("asset_address"),

#         "time_added": dt.now(),
#     }
#     asset_exists = Assets.query.filter_by(asset_address=record["asset_address"]).first()
#     if asset_exists:
#         flash("Asset already exists")
#         return redirect(url_for("assets.assets_list"))

#     asset_record = Assets(**record)

#     db.session.add(asset_record)
#     db.session.commit()

#     return redirect(url_for("main.profile"))
