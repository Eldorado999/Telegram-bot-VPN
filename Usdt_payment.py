import random
import requests
from Config import USDT_ADRESS

def create_payment(user_id):
    bill_id = str(user_id) + '_' + str(random.randint(10000, 99999))
    return bill_id


def check_payment(value, trans_hash):
    to_adress = '"to_address":"' + USDT_ADRESS
    value = 'amount_str":"' + str(round(value * 1000000))
    token_adress = '"contract_address":"TR7NHqjeKQxGTCi8q8ZY4pL8otSzgjLj6t"'
    status = '"confirmed":true'
    url = 'https://apilist.tronscanapi.com/api/transaction-info?hash=' + trans_hash
    session = requests.Session()
    response = session.get(url).text
    if trans_hash in response:
        # print('transaction: ' + trans_hash + ' found')
        if token_adress in response:
            # print('USDT confirmed')
            if to_adress in response:
                # print('address confirmed')
                if value in response:
                    # print('value confirmed')
                    if status in response:
                        return 'status: confirmed, transaction done'
                    else:
                        return 'transaction is not confirmed yet, pls wait'
                else:
                    return 'wrong value'
            else:
                return 'invalid recipient address'
        else:
            return 'wrong coin'
    else:
        return 'transaction not found'
