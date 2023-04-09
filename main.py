import re
import smtplib
import socket
import csv
import dns
from dns import resolver


def checkEmail(email):
    # Step 1: Check email
    # Check using Regex that an email meets minimum requirements, throw an error if not
    match = re.match('^[_a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$', email)

    if match == None:
        # print('Type: '+str(type(email)))
        print('Bad Syntax in ' + email)
        raise ValueError('Bad Syntax')

    # Step 2: Getting MX record
    # Pull domain name from email address
    domain_name = email.split('@')[1]

    # get the MX record for the domain
    resolver = dns.resolver.Resolver()
    resolver.timeout = 120
    resolver.lifetime = 120

    mxRecord = None
    try:
        records = resolver.resolve(domain_name, 'MX')
        mxRecord = records[0].exchange
        mxRecord = str(mxRecord)
    except Exception as e:
        print(email + " - get MX record of %s failed: " % str(e))

    # Step 3: ping email server
    # check if the email address exists

    # Get local server hostname
    host = socket.gethostname()

    # SMTP lib setup (use debug level for full output)
    server = smtplib.SMTP()
    server.set_debuglevel(0)

    code = None

    # SMTP Conversation
    try:
        server.connect(mxRecord)
        server.helo(host)
        server.mail('me@domain.com')
        code, message = server.rcpt(str(email))
        server.quit()
    except Exception as e:
        print(email + " - get SMTP conversation of %s failed: " % str(e))

    # Assume 250 as Success
    if code == 250:
        return 1
    else:
        return 0


with open('Book1.csv', 'r') as csvfile:
    emailreader = csv.reader(csvfile, delimiter=',')
    count = 0
    for row in emailreader:
        if count > 0:
            email_address = row[2]
            if checkEmail(email_address) == 0:
                print(email_address)

        count = count + 1
csvfile.close()
