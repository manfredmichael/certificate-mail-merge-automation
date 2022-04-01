# Certificate Mail Merge Automation
Send your event certificates with 3 lines of code

![](./preview.png)

### Project Tree
```
•
├── data/
│   └── <CERTIFICATE_NAME>/
│       ├── certificate.pdf
│       ├── recipient_list.csv
│       ├── email_message.txt
│       └── <CERTIFICATE_CODE>.code
├── secrets/
│   └── client_secret.json
├── imgs/
├── imgs/
├── logs/
├── modules/
│   ├── certificate_generator/
│   ├── certificate_sender/
│   └── google_api/templates/
└── main.py
```

A typical project tree

```
•
├── data
│   ├── best-student
│   │   ├── CERTIFICATE OF APPRECIATION - WEEK 2_TTD.pdf
│   │   ├── data.csv
│   │   ├── message.txt
│   │   └── WYUX260322AP.code
│   └── weekly-participant
│       ├── certificate.pdf
│       ├── data.csv
│       ├── message.txt
│       └── WYUX260322PT.code
├── secrets/
│   └── client_secret.json
├── imgs/
├── logs/
├── modules/
│   ├── certificate_generator/
│   ├── certificate_sender/
│   └── google_api/templates/
└── main.py
```
