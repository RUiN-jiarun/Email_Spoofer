# Email_Spoofer demo  

## Install

```cmd
$ pip install -r requirements.txt
```

## Usage
```
usage: python spoofer.py [-h] [-tls] [-helo HELO] [-sa SENDER] [-ra RECEIVER]
                  [-f MFROM] [-s SUBJECT] [-b BODY]

OPTIONS:
  -h, --help            show this help message and exit
  -tls, --starttls      Enable STARTTLS command.
  -helo HELO, --helo HELO
                        Set HELO domain.
  -sa SENDER, --sender SENDER
                        Set sender address.
  -ra RECEIVER, --receiver RECEIVER
                        Set receiver address.
  -f MFROM, --mfrom MFROM
                        Set FROM domain.
  -s SUBJECT, --subject SUBJECT
                        Set SUBJECT domain.
  -b BODY, --body BODY  Set email content.
```
## Using spoof parameter  
```  
Usage: python spoofer.py [spoofparam]
```

**Please check all of the parameters before running this demo!!**