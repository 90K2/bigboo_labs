import hashlib


def validation(payment: dict, secret: str) -> bool:
    # payment_sample = {'notification_type': 'p2p-incoming', 'amount': '387.55', 'datetime': '2017-07-28T07:36:01Z', 
    # 'codepro': 'false', 'sender': '41001000040', 'sha1_hash': 'ba58c1e29a75b2bf4fe0c12144eedd89eb8a5da1',
    # 'test_notification': 'true', 'operation_label': '', 'operation_id': 'test-notification', 'currency': '643', 
    # 'label': ''} 

    check_string = '{}&{}&{}&{}&{}&{}&{}&{}&{}'.format(
        payment['notification_type'],
        payment['operation_id'],
        payment['amount'],
        payment['currency'],
        payment['datetime'],
        payment['sender'],
        payment['codepro'],
        secret,
        payment['label']
    )
    return hashlib.sha1(check_string.encode('utf-8')).hexdigest() == payment['sha1_hash']
