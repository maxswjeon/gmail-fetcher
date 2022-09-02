# Gmail Fetcher with LDAP Support

## Description

This program is made to use multiple Google Workspace Gmails with a single Google Workspace Account

## How to use

1. Go to [Google Workspace Admin](https://admin.google.com)
2. If you want another domain rather than the original one that you used for signing up the Google Workspace
   1. Go to Account > Domains > Manage Domains
   2. (Optional) Add a domain as a Secondary Domain
3. Go to Apps > Google Workspace > Gmail > Default routing
4. Add a rule to route all emails to the Gmail account you want to use
   1. Pattern match
   2. `.\*@(YOUR-DOMAIN-HERE)`
   3. Modify Message > Envelope recipient > Change envelope recipient > Replace recipient: `YOUR-GMAIL-HERE`
   4. Save
5. Go to [Google Account Settings](https://myaccount.google.com) and register a 2-factor authorization (Security > 2-Step Verification)
6. Create a App password
   1. Select App > Other (Custom name)
   2. Put any name you want (e.g. Gmail Fetcher) and click Create
   3. Copy the password and save it well
7. Enable IMAP from Gmail
   1. Go to [Gmail](https://mail.google.com)
   2. Click Settings > See all settings > Forwarding and POP/IMAP
   3. Enable IMAP
   4. Auto-Expunge on
   5. Save
8. Run the program

## Environments

- IMAP_SERVER  
  If you are working with Gmail, set this to `imap.gmail.com`.

- IMAP_USER  
  The IMAP Username to connect to. Google Workspace account.

- IMAP_PASS  
  The app password that you generated in step 6.

- LMTP_HOST  
  LTMP host to save the emails to. Recommend using [Dovecot Docker Image](https://hub.docker.com/r/dovecot/dovecot/).

- LMTP_PORT  
  LMTP port to save the emails to. Usually `24`.

- LDAP_ENABLED  
  Boolean Value. If you want to use LDAP, set this to `true`.

- TARGET_EMAILS  
  Comma separated list of emails to send the fetched emails to. Only used if `LDAP_ENABLED` is `false`.

- LDAP_SERVER  
  LDAP server to connect to.

- LDAP_BIND_DN  
  LDAP bind DN.

- LDAP_BIND_PW  
  LDAP bind password.

- LDAP_BASE_DN  
  LDAP base DN.

- LDAP_USER_DN  
  LDAP user DN.

## Endpoints

- `/fetch`  
  Fetches emails for all accounts.

- `/fetch/{email}`  
  Fetches emails for specific account
