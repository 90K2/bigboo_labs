import re
import dns.resolver
import socket
import smtplib

socket.setdefaulttimeout(5)
host = socket.gethostname()


SMTP_CODES = {
    550: 'Requested email is unavailable',
    250: 'Requested email is okay',
    553: 'mailbox name not allowed'
}
isascii = lambda s: len(s) == len(s.encode())


def check_email(addressToVerify):
    # print(addressToVerify)
    # check address syntax
    match = re.match('[^@]+@[^@]+\.[^@]+', addressToVerify)
    decision = ''
    if match is None:
        decision = 'Bad Syntax'
    else:
        # Step 2: Getting MX record
        # Pull domain name from email address
        domain_name = addressToVerify.split('@')[1]

        # get the MX record for the domain
        try:
            records = dns.resolver.query(domain_name, 'MX')
            mxlist = list([str(rec.exchange) for rec in records])
            try:
                for mxRecord in mxlist:
                    decision = SMTP_CODES[550]

                    server = smtplib.SMTP()
                    server.set_debuglevel(0)
                    # check mailbox on mailserver
                    try:
                        server.connect(mxRecord)
                        server.helo(host)
                        server.mail('me@domain.com')
                        code, message = server.rcpt(str(addressToVerify))
                        server.quit()
                        decision = SMTP_CODES.get(code, code)
                        raise StopIteration
                    except (TimeoutError, socket.timeout, smtplib.SMTPServerDisconnected) as e:
                        decision = 'Cannot verify {}'.format(e)
                        continue
            except StopIteration:
                pass
        except (dns.resolver.NoAnswer, dns.resolver.NXDOMAIN,dns.exception.Timeout):
            decision = 'Bad domain'
    # print(decision)
    return decision
