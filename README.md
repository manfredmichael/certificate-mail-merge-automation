# Certificate Mail Merge Automation
Send your event certificates with 3 lines of code

![](./preview.png)

### Project Tree
In this project tree, the data/ directory is your main interest. This is where you put:

1. Certificate Template (.pdf)
2. List of Recipients (.csv)
3. email_message.txt 
4. Certificate Code (.code) <- It's optional

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


A typical project tree with required data would look like this.

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

### Setting up Certificate Data

#### 1. Certificate Template (.pdf)
You can choose whether to use pdf/png file as certificate template.

#### 2. List of Recipients (.csv)
Put your recipients data in a csv file with `Email` and `Name` column.

```
Name,Email
Muhammad Fadhiil F, fadhil@example.com
Manfred Michael, manfredmichael2030@gmail.com
Michael Corleone, michaelandolini@example.com
GDSC Gunadarma University, dscgunadarma@example.com
```


#### 3. email_message.txt 
Put your email message in a simple txt file. You can put the subject with `SUBJECT:` prefix on the first line, but this is optional. You can put `[NAME]` keyword to be replaced by recipient's own name.

```
SUBJECT: Your Weekly Class UI/UX 2022 Participation
Hello, [NAME]!

Thank you so much for becoming a part of our first UI & UX Weekly Class. We hope that this event has helped you in your own UI/UX journey and greatly magnified your passion in this field. We are truly looking forward to see you on our next event. Until then, we are sending our appreciation your way through this certificate.

Best regards,
GDSC UG
Together We Grow <>

Contact Us!
Instagram: https://www.instagram.com/gdscug/
Discord: https://dscug.club/discord
Email: dscgunadarma@gmail.com
```
