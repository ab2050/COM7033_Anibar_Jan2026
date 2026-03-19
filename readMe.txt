Technologies used : 

Python
Flask
PostgresQL
MongoDB
Sqlite
HTML
CSS
Javascript
Redis
Docker




Business Requirements : 

Secure storage of health records
Patients can make appointments
Admins can see user count and deletion reasons
Doctors can see which patients are assigned to them
Doctors can add notes and diagnosis per patient
Audit logs
In accordance with GDPR and HIPAA
Strict RBAC to prevent users from accessing sensitive data they are not authorised to view

Data Sensitivity :

Patient health records, being extremely sensitive, were stored in mongoDB with encryption for the highest level of security.
Since login data is sensitive to the system, passwords were hashed using argon2. Flask security features like CSRF, HTTPOnly and session cookie signer were implemented to prevent unauthorized access.
Audit logs were implemented in accordance with GDPR.
Since deletion reasons are the least sensitive, they were stored in sqlite without any hashing or encryption.


Security : 

Security was implemented via hashing (argon2), encryption (encrypt library), and flask security features to protect against CSRF, XSS and other attacks. RBAC was also implemented with checks for both username and role. Session timeout was added. 2FA was also implemented using pyotp and smtp libraries wherein all users would have to verify their emails via a link sent to their email at the time of registration to create an account, and with OTPs at login. Security was implemented as defense in depth with multiple layers of checks and least privilege at every point to ensure there is no unauthorised access to data. Input validation was also implemented to prevent SQL injection attacks. I also used the “Have I been pwned” API, via k-anonymity, to prevent users from using already breached passwords, and a blacklist system was implemented to prevent slurs or offensive language from being used as usernames.








Threat Modelling : 

STRIDE : 

SPOOFING - Password hashing, session management containing username and role, email verification, IP level rate limiting
TAMPERING - Flask[SESSION_USE_SIGNER], CSRF, Redis stores cookies
REPUDIATION - Audit logs, MongoDB updated on timestamps
INFORMATION DISCLOSURE - Flask[SESSION_COOKIE_HTTPONLY], RBAC, server side cookies via Redis, password hashing, health record encryption
DENIAL OF SERVICE - IP level rate limiting via Redis
ELEVATION OF PRIVILEGE - Session cookies store roles, RBAC, every session is signed with a flask secret key

Potential threats : 

Logged in on an unattended device - Mitigated by session timeouts
SQL injection - Mitigated by input sanitization

Trust Boundaries : 

Browser - protected by CSRF, session management, HTTP only, Session cookie samesite and session cookie signer
Login/Registration - protected by 2FA, password hashing
Health records - encrypted and stored in mongoDB
External variables - stored in .env file, not pushed to a public repo
Application logic - Session cookies stored in redis, checked before each protected route

Security requirements : 

Password hashing - argon2
Encryption - encrypt library to encrypt health records in mongoDB
2FA - pyotp and smtp
Session cookies - stored in Redis
Input sanitization - parameterized inputs
CSRF - flask-wtf, session cookie samesite
IP Rate limiting to prevent repeated attempts - flask-limiter, account locked
XSS - session cookie http only
Unauthorized access from unattended device - session timeout
 Username blacklist - to prevent offensive language from being used as username

A screenshot of flask security features that have been implemented : 


“Lax” was selected, otherwise the email checking flow during registration would fail, as “strict” would not allow a separate email sent link.

Professional practices, ethics and compliance : 

Restricted access - only medical staff and patients can see their data, admins are not permitted
Data minimisation - Only important data is collected
Transparency - Users can view their own data at any time
Auditability and accountability - All actions are logged as mandated by GDPR, time stamped update column on mongoDB

Evaluation and Risk Justification : 

Passwords are hashed via argon2, making it computationally very expensive to attempt to crack passwords

2FA verification ensures that any data breach won’t expose critical information since OTPs are needed on login

Session timeout to prevent access from unattended devices

Sessions are signed to prevent tampering
IP level rate limiting to prevent brute force attacks

Parameterized inputs to prevent SQL injection

Data encryption as an added level of security on MongoDB


Trade-offs : 

2FA adds an extra step on every login, can make login tedious but greatly improves security

Short duration for session timeouts can create additional hassle for users interrupted by genuine reasons

Encryption adds extra overhead on every mongodb query, but makes user health records more secure

Multiple databases can cause integration problems

Testing : 

Implemented unit testing and integration testing to ensure all databases are working properly and in tandem with each other.

test_passwordauth.py - ensures that passwords are hashed and are up to required security standards

test_integration.py - ensures that databases are working fine and that the system is usable and secure

Future Enhancements  :

Payment system to allow users to pay for prescriptions and other medical procedures online, using Stripe API for PCI DSS compliance
Dual admin approval before new admins are added
AWS KMS instead of an env file
Grafana dashboard to have live system performance overview
Video verification system
Azure SQL to store backup data
Complete API endpoints with JWT and OAuth tokens
NHS content API so doctors can lookup medicines
End to end testing using playwright to ensure that the full system is working
Functional testing since the code has multiple parts working in tandem












Deployment Guide : 

Required software : Python, PostgreSQL, Docker, redis and mongoDB images on docker

Install required libraries : flask, flask-wtf, flask-limiter, argon2, encryption, cryptography, psycopg2, pymongo
Create an env file with the following variables : flaskKey, mongouser ,mongopass, appPassword, emailid, encryptionkey
Create docker-compose.yml and pull images of redis and mongodb
Start docker : docker-compose up -d
Initialise postgre tables by running maketables on dbCreator.py only once
Run from mainpage.py, the site will be on http://localhost:5000
Run tests to ensure all components are working fine
Create folder “tests”
Create conftest.py , create a client and set WTF_CSRF_ENABLED to false, otherwise testing fails
Create test_passwordAuth and test_integration files, it is mandatory for all file names and function names to start with test_
Run pytest tests/test_passwordAuth.py or pytest tests/test_integration.py

























References : 

Biryukov, A., Dinu, D., & Khovratovich, D. (2015). Argon2: the memory-hard function for password hashing and other applications. https://www.password-hashing.net/argon2-specs.pdf
Cloudflare. (2018, February 21). Validating Leaked Passwords with k-Anonymity. The Cloudflare Blog. https://blog.cloudflare.com/validating-leaked-passwords-with-k-anonymity/
Cryptography.com. (2014). Fernet (symmetric encryption) — Cryptography 2.9.dev1 documentation. Cryptography.io. https://cryptography.io/en/latest/fernet/
Drake, V. (2022). Threat Modeling | OWASP. Owasp.org; OWASP. https://owasp.org/www-community/Threat_Modeling
Exabeam. (2024, June 28). How Does GDPR Impact Log Management? Exabeam. https://www.exabeam.com/explainers/gdpr-compliance/how-does-gdpr-impact-log-management/
haveibeenpwned. (n.d.). Have I Been Pwned: Pwned Passwords. Haveibeenpwned.com. https://haveibeenpwned.com/Passwords
Microsoft. (2022, August 25). Threats - Microsoft Threat Modeling Tool - Azure. Learn.microsoft.com. https://learn.microsoft.com/en-us/azure/security/develop/threat-modeling-tool-threats
OWASP. (2025, July). OWASP Top Ten. Owasp.org; OWASP. https://owasp.org/www-project-top-ten/
W3Schools. (2024). HTML Tutorial. W3schools.com. https://www.w3schools.com/html/
Wetzels, J. (2016). Open Sesame: The Password Hashing Competition and Argon2. 10.48550/arXiv.1602.03097. 
Anthropic. (2025). Claude. Claude.ai. https://claude.ai/
