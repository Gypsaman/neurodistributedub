from flask import Blueprint,render_template,request,redirect,flash,url_for
from flask_login import current_user
from webproject.models import User,Wallet #,Assets
from webproject.modules.web3_interface import get_nft_uri
from webproject import db
from flask_login import login_required
import os

nfts = Blueprint('nfts',__name__)


@nfts.route('/assets/view/<int:page_num>/<int:asset_id>')
@login_required
def nfts_view(page_num,asset_id):
    pass
    
    # asset = Assets.query.filter_by(id=asset_id).first()

    # if asset.asset_type != 2:
    #     return redirect (url_for('assets.noview',page_num=page_num))

    # metadatas = get_nft_uri(asset.asset_address)
      
    # return render_template('nfts/nfts.html',metadatas=metadatas,page_num=page_num)


@nfts.route('/test')
def test():
    from webproject.modules.dotenv_util import get_cwd
    return get_cwd()