# coding:utf-8
import time
import datetime
import smtplib
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email.header import Header


class Mail_Sender:
    def __init__(self, mail_para):
        self.smtp_sever = mail_para.smtp_sever
        self.mail_addr = mail_para.mail_addr
        self.mail_license = mail_para.mail_license
        self.msg = None

    def edit_content(self, subject_content, body_content, img_dir=None):  # 主题、正文
        self.msg = MIMEMultipart()
        self.msg["From"] = self.mail_addr
        self.msg["To"] = ''
        self.msg["Subject"] = Header(subject_content, 'utf-8')
        if img_dir is None:
            html_template = f'<html><body>{body_content}</body></html>'
        else:
            with open(img_dir, 'rb') as img:
                msg_img = MIMEImage(img.read(), _subtype='octet-stream')
            img_name = img_dir.split("/")[-1]
            msg_img.add_header('Content-ID', f'{img_name}')
            html_template = f'<html><body><p>{body_content}</p>' \
                            f'<img src="cid:{img_name})" alt="image load failed" width=100% ></body></html>'
            self.msg.attach(msg_img)
        self.msg.attach(MIMEText(html_template, _subtype='html', _charset='utf-8'))

    def send_email(self, email_receiver):  # 发送次数，间隔时间
        try:
            stp = smtplib.SMTP_SSL(self.smtp_sever, port=994)  # 创建SMTP对象
            # stp.set_debuglevel(1)  # 打印出和SMTP服务器交互的所有信息
            stp.login(self.mail_addr, self.mail_license)  # 登录邮箱，传递参数1：邮箱地址，参数2：邮箱授权码
            print(f'{datetime.datetime.now()} -* smtp: Login successfully! *-')
            stp.sendmail(self.mail_addr, email_receiver, self.msg.as_string())
            print(f'{datetime.datetime.now()} -* smtp: Send successfully! *-')
            stp.quit()
        except Exception as unknown_problem:
            print(f'{datetime.datetime.now()} -* smtp: Send failed! *-\n{unknown_problem}')
            time.sleep(5)


if __name__ == '__main__':
    pass
