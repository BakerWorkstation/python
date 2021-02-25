

from poplib import POP3

p = POP3('pop.163.com')
p.user('')
p.pass_('')
num=p.stat()[0]
print p.stat()

ff = open('./1.mail','w')
for eachnum in range(1,num+1):
	rsp, msg, siz = p.retr(eachnum)
	for eachline in msg:
		ff.write(eachline + '\n')
	ff.close()
	p.quit()
