import sys
import getpass
import argparse
from smtp_sender import MailSender
import spoofparam
import dns.resolver
import traceback

def parser_error(errmsg):
    print(("Usage: python " + sys.argv[0] + " [Options] use -h for help"))
    print(("Error: " + errmsg))
    sys.exit()

def parse_args():
    # parse the arguments
    parser = argparse.ArgumentParser()
    parser.error = parser_error
    parser._optionals.title = "OPTIONS"
    
    parser.add_argument(
    	'-tls', '--starttls', action='store_true', help="Enable STARTTLS command.")
    parser.add_argument(
        '-helo', '--helo', default=None, help="Set HELO domain.")
    parser.add_argument(
        '-sa', '--sender', default=None, help="Set sender address.")
    parser.add_argument(
        '-ra', '--receiver', default=None, help="Set receiver address.")
    parser.add_argument(
        '-f', '--mfrom', default=None, help="Set FROM domain.")
    parser.add_argument(
        '-s', '--subject', default=None, help="Set SUBJECT domain.")
    parser.add_argument(
        '-b', '--body', default=None, help="Set email content.")

    args = parser.parse_args()
    return args

def query_mx_record(domain):
	try:
		mx_answers = dns.resolver.resolve(domain, 'MX')
		for rdata in mx_answers:
			a_answers = dns.resolver.resolve(rdata.exchange, 'A') 
			for data in a_answers:
				return str(data)
	except Exception:
		traceback.print_exc()

def get_mail_server_from_email_address(e):
    e = e[1:-1]
    e = e.encode()
    domain = e.split(b"@")[1]
    return query_mx_record(domain.decode())

def main():
    param = sys.argv[1]
    args = spoofparam.param[param]
    # print('E-mail Spoofer Ver 1.0')
    # print('E-mail Spoofer Ver 1.1')
    print('E-mail Spoofer Ver 1.2')
    # sender_addr = input('Please input the sender mail address:')
    if args['login']:
        password = getpass.getpass('Please input the password:')
        # sending_server = ('smtp.' + sender_addr[(sender_addr.index('@')+1):], 25)
        # print(args)
        mail_sender = MailSender()
        mail_sender.set_param(sender_addr=args['sender'], password=password, rcpt_to=args['receiver'], helo=args['helo'], mail_from=args['mailfrom'],  
                            dkim_para=args['dkim_para'],starttls=True, Subject=args['subject'], From=args['mfrom'], body=args['body'])
        mail_sender.send_email()
    else:
        mail_sender = MailSender()
        sender_addr = get_mail_server_from_email_address(args['receiver'])
        mail_sender.set_param(sender_addr=sender_addr, password=None, rcpt_to=args['receiver'], helo=args['helo'], mail_from=args['mailfrom'],  
                            dkim_para=args['dkim_para'],starttls=False, Subject=args['subject'], From=args['mfrom'], body=args['body'])
        mail_sender.send_email()

if __name__ == '__main__':
    main()