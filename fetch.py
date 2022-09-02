import imaplib
import os
import smtplib
from email.header import decode_header
from email.utils import parseaddr
from imaplib import IMAP4_SSL

from ldap3 import ALL, Connection, Server

imaplib._MAXLINE = 10_000_000_000

def fetch_all():
  if os.getenv('LDAP_ENABLED').lower() == 'true': 
    print("LDAP Enabled - Fetching all users") 
    server_ldap = Server(os.getenv('LDAP_SERVER'), get_info=ALL)
    conn_ldap = Connection(server_ldap, user=os.getenv('LDAP_BIND_DN'), password=os.getenv('LDAP_BIND_PW'), auto_bind=True)
    conn_ldap.search(os.getenv('LDAP_USER_DN'), '(objectClass=inetOrgPerson)', attributes=['mail'])
    os.environ['TARGET_EMAILS'] = ' '.join(e.mail.values[0] for e in conn_ldap.entries)
    print(f"Fetched users: {os.getenv('TARGET_EMAILS')}")
    conn_ldap.unbind()
    
  server_imap = IMAP4_SSL(os.getenv('IMAP_SERVER'))
  server_imap.login(os.getenv('IMAP_USER'), os.getenv('IMAP_PASS'))
  server_imap.select()

  server_lmtp = smtplib.LMTP(os.getenv('LMTP_HOST'), os.getenv('LMTP_PORT'))

  for email in os.getenv('TARGET_EMAILS').split(' '):
    print(f"Fetching email for {email}")
    count = 0
    _, nums = server_imap.search(None, 'TO', email)
    for num in nums[0].split():
      count += 1
      _, data = server_imap.fetch(num, '(RFC822)')
    
      body = data[0][1].decode('utf-8')

      name, addr = parseaddr(body)
      addr = email.strip().lower()
      if name:
        name = name.strip()
        decoded_string, charset = decode_header(name)[0]
        if charset is not None:
          try:
            name = decoded_string.decode(charset)
          except UnicodeDecodeError:
            print(f"Failed to decode {name}")
        else:
          name = decoded_string

      print(name, addr)
      server_lmtp.sendmail(name + addr, email, body)

      server_imap.store(num, '+FLAGS', '\\Deleted')
    print(f"Fetched {count} emails for {email}")
  server_imap.expunge()
  server_imap.close()
  server_imap.logout()

def fetch(email):
  server_imap = IMAP4_SSL(os.getenv('IMAP_SERVER'))
  server_imap.login(os.getenv('IMAP_USER'), os.getenv('IMAP_PASS'))
  server_imap.select()

  server_lmtp = smtplib.LMTP(os.getenv('LMTP_SERVER'))

  count = 0
  _, nums = server_imap.search(None, 'TO', email)
  for num in nums[0].split():
    count += 1
    _, data = server_imap.fetch(num, '(RFC822)')
    
    body = data[0][1].decode('utf-8')

    name, addr = parseaddr(body)
    addr = email.strip().lower()
    if name:
      name = name.strip()
      decoded_string, charset = decode_header(name)[0]
      if charset is not None:
        try:
          name = decoded_string.decode(charset)
        except UnicodeDecodeError:
          print(f"Failed to decode {name}")
      else:
        name = decoded_string

    server_lmtp.sendmail(name + addr, email, body)

    server_imap.store(num, '+FLAGS', '\\Deleted')
  print(f"Fetched {count} emails for {email}")
  server_imap.expunge()
  server_imap.close()
  server_imap.logout()
