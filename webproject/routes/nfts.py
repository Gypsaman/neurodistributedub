from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import current_user
from webproject.models import User,Wallet,Assets
from webproject.web3_interface import get_nft_uri
import requests
import json
from webproject import db
from flask_login import login_required

nfts = Blueprint('nfts',__name__)


@nfts.route('/viewnfts/<int:asset_id>')
def nfts_view(asset_id):
    
    asset = Assets.query.filter_by(id=asset_id).first()
    metadatas = get_nft_uri(asset.asset_address)
    
    
    return render_template('nfts/nfts.html',metadatas=metadatas)


@nfts.route('/test')
def test():

    return render_template('nfts/test.html',html_text=html_text)