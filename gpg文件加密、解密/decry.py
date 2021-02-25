#!/usr/bin/env python
import gnupg
gpg = gnupg.GPG(gnupghome='/root/.gnupg')
privatekey = open('Sylar.sec','rb')
key_data = privatekey.read()
privatekey.close()

import_result = gpg.import_keys(key_data)
private_keys = gpg.list_keys(True)

pgpfile = open('test.gpg','rb')
pgpdata = pgpfile.read()
pgpfile.close()
decrypted_data = gpg.decrypt(pgpdata,passphrase='18846107211',output='test')
