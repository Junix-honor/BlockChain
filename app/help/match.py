from sqlalchemy.orm import aliased
from ..models import Account
from .. import db


def matchCrossChainUser(out_RPC_server, in_RPC_server, user_id):
    account1 = aliased(Account)
    account2 = aliased(Account)
    res = db.session.query(account1.id, account2.id, account1.money, account2.money). \
        join(account2, account1.user_id == account2.user_id). \
        filter(account1.user_id != user_id). \
        filter(account1.chain_address == in_RPC_server). \
        filter(account2.chain_address == out_RPC_server).all()
    return res
