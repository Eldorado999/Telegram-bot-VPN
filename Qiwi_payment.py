import random
from pyqiwip2p import QiwiP2P
from Config import QIWI_TOKEN


p2p = QiwiP2P(auth_key=QIWI_TOKEN)


def create_payment(user_id, summ):
    comment = str(user_id) + '_' + str(random.randint(1000, 9999))
    bill = p2p.bill(amount=summ, lifetime=15, comment=comment)
    return [user_id, summ, bill.bill_id, comment, bill.pay_url]


def check_payment(bill_id):
    if str(p2p.check(bill_id=bill_id).status) == 'PAID':
        return True
    else:
        return False
