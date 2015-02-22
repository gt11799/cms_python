# coding:utf-8
import smtplib
from email.mime.text import MIMEText
import time

# 正文


def send_mail(subject, body, mail_to, username="cops@pluray.com", password="pluray123", mail_type='plain', isHome=False):
    # 收信邮箱
    # mail_to=['lovedboy.tk@qq.com','guohui@pluray.com']
    # 定义正文
    assert isinstance(mail_to, list) == True
    msg = MIMEText(body, _subtype=mail_type, _charset='utf-8')
    # 定义标题
    msg['Subject'] = subject
    # 定义发信人
    if isHome:
        msg['From'] = '小荷特卖'+'<' + username + '>'
    else:
        msg['From'] = username  

    msg['To'] = ';'.join(mail_to)
    # 定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    try:
        smtp = smtplib.SMTP()
        # 连接SMTP服务器，
        smtp.connect('smtp.exmail.qq.com')
        # 用户名密码
        smtp.login(username, password)
        # smtp.set_debuglevel(1)
        smtp.sendmail(username, mail_to, msg.as_string())
        smtp.quit()
        return True
    except Exception as e:
        print "send mail error:%s"%e
        return False

def sys_send_mail(subject, body, mail_to, mail_from="fmaster@notify.xiaoher.com", mail_type='plain', isHome=False):
    # 系统发送邮箱
    # mail_to=['lovedboy.tk@qq.com','guohui@pluray.com']
    # 定义正文
    if not isinstance(mail_to,(list,tuple)):
        mail_to = [mail_to,]
    msg = MIMEText(body, _subtype=mail_type, _charset='utf-8')
    # 定义标题
    msg['Subject'] = subject
    # 定义发信人
    if isHome:
        msg['From'] = '小荷特卖'+'<' + mail_from + '>'
    else:
        msg['From'] = mail_from  
    print ';'.join(mail_to)
    msg['To'] = ';'.join(mail_to)
    # 定义发送时间（不定义的可能有的邮件客户端会不显示发送时间）
    msg['date'] = time.strftime('%a, %d %b %Y %H:%M:%S %z')
    try:
        smtp = smtplib.SMTP('121.199.31.97',25)
        smtp.sendmail(mail_from, mail_to, msg.as_string())
        smtp.quit()
        msg =  "Successfully sent email"
        print msg
        return (True,msg)
    except Exception as e:
        msg = "send mail error:%s"%e
        print msg
        return (False,msg)

if __name__ == "__main__":
    # send_mail("test", 'test body', ["haifang@pluray", "lovedboy.tk@qq.com"])
    send_mail("test", 'test body', ["479649938@qq.com"])
