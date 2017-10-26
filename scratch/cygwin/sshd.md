
https://docs.oracle.com/cd/E24628_01/install.121/e22624/preinstall_req_cygwin_ssh.htm#EMBSC281

```bash
chown cyg_server /var/log/sshd.log
chown -R cyg_server /var/empty
chown cyg_server /etc/ssh*
chmod 755 /var/empty
chmod 644 /var/log/sshd.log
editrights -a SeAssignPrimaryTokenPrivilege -u cyg_server
editrights -a SeCreateTokenPrivilege -u cyg_server
editrights -a SeTcbPrivilege -u cyg_server
editrights -a SeServiceLogonRight -u cyg_server

cygrunsrv -S sshd
```

https://cygwin.com/ml/cygwin/2016-03/msg00097.html

https://www.cygwin.com/faq/faq.html#faq.setup.cli
