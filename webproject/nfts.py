from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import login_required,current_user
from .models import User,Wallet,Assets
from .web3_interface import get_nft_uri
import requests
import json
from . import db

nfts = Blueprint('nfts',__name__)


@nfts.route('/viewnfts/<int:asset_id>')
def nfts_view(asset_id):
    
    asset = Assets.query.filter_by(id=asset_id).first()
    metadatas = get_nft_uri(asset.asset_address)
    

    
    return render_template('nfts.html',metadatas=metadatas)
