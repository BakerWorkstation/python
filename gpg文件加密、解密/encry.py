#!/usr/bin/env python
import gnupg

gpg = gnupg.GPG(gnupghome='/root/.gnupg')
publickey = open('Sylar.pub','rb')
key_data = publickey.read()
publickey.close()

import_result = gpg.import_keys(key_data)
public_keys = gpg.list_keys()

pgpfile = open('/etc/rc.local','rb')
pgpdata = pgpfile.read()
pgpfile.close()

encrypted_ascii_data = gpg.encrypt(pgpdata, 'Sylar', output='./test.gpg')
