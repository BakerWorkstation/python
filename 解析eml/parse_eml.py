#-*- encoding: gb2312 -*-

import os

import email

class  Prase_eml():
    
    def __init__(self, filename):
        self.__file = filename
        fp = open('./1.eml', "r")
        self.msg = email.message_from_file(fp)

    def prase_head(self):
        __subject = self.msg.get('subject')
        h = email.Header.Header(__subject)
        dh = email.Header.decode_header(h)
        subject = dh[0][0]
        __from = email.utils.parseaddr(self.msg.get("from"))[1]
        __to = email.utils.parseaddr(self.msg.get("to"))[1]
        return (__from, __to, __subject)

    def prase_file(self):
        for par in self.msg.walk():
            if  par.is_multipart():
                continue

            name = par.get_param('name')
            if name:
                h = email.Header.Header(name)
                dh = email.Header.decode_header(h)
                __fname = dh[0][0]
                data = par.get_payload(decode=True)
                f = open('./' + __fname, 'wb')
                f.write(data)
                f.close()
                __save_path = os.getcwd()
            else:
                if 'html' in str(par):
                    continue
                __content = par.get_payload(decode=True)
        return (__content, __fname, __save_path)

if __name__ == '__main__':
    P = Prase_eml('./1.eml')
    element = P.prase_head()
    element += P.prase_file()
    print '''
    (Email)\n
            from : %s\n
            to : %s\n
            subject : %s\n
            content : %s\n
            attachment : %s\n
            save_path : %s\n
        '''  %  element
    del element
