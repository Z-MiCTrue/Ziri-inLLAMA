from email.parser import Parser
from email.header import decode_header
from email.utils import parseaddr
import poplib
import time
import os

# 包结构 & 脚本
if os.getcwd() == os.path.split(os.path.realpath(__file__))[0]:
    from html_text import de_html
else:
    from .html_text import de_html


def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value


# 获取邮件编码并解码
def solve_charset(html, msg):
    charset = msg.get_charset()
    if charset is None:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    if charset:
        html = html.decode(charset)
    return html


def parse_text(msg, key_word=''):
    message_text = [None, None, None]
    mail_subject = msg.get('Subject', '')
    if mail_subject:
        mail_subject = decode_str(mail_subject)
        if key_word in mail_subject:
            message_text[0] = mail_subject  # 主题
            sender_id = msg.get('From', '')
            hdr, addr = parseaddr(sender_id)
            message_text[1] = addr  # 地址
            # 根据不同类型解码
            if msg.get_content_type() in ['text/html', 'text/plain']:
                html = msg.get_payload(decode=True)
                html = solve_charset(html, msg)  # 邮件解码
                mail_content = de_html(html)  # html 解码
                message_text[2] = mail_content
            elif msg.is_multipart():
                html = msg.get_payload()
                for n, part in enumerate(html):
                    content_type = part.get_content_type()
                    if content_type == 'text/plain':
                        mail_content = part.get_payload(decode=True)
                        try:
                            mail_content = mail_content.decode('utf-8')
                        except UnicodeDecodeError:
                            mail_content = mail_content.decode('gbk')
                        message_text[2] = mail_content
            if message_text[-1] is None:
                print('Error: no useful content')
                return None
            else:
                return message_text
        else:
            print('Error: without keyword')
            return None
    print('Error: no email')
    return None


class Mail_Receiver:
    def __init__(self, mail_para):
        self.pop3_server = mail_para.pop3_server
        self.mail_addr = mail_para.mail_addr
        self.mail_license = mail_para.mail_license
        self.mail_message = []  # 储存邮件集合

    def get_message(self):
        print(time.asctime(time.localtime(time.time())))
        try:
            server = poplib.POP3_SSL(self.pop3_server, 995)
            # server.set_debuglevel(1)  # 打开调试信息
            # 身份认证:
            server.user(self.mail_addr)
            server.pass_(self.mail_license)
            resp, mails, octets = server.list()
            print('-* pop3: Receive successfully! *-')
            for i in range(1, len(mails) + 1):
                resp, lines, octets = server.retr(i)  # lines存储了邮件的原始文本的每一行
                try:
                    msg_content = b'\r\n'.join(lines).decode('utf-8')
                except UnicodeDecodeError:
                    msg_content = b'\r\n'.join(lines).decode('gbk')
                # 解析出邮件:
                msg = Parser().parsestr(msg_content)
                message_text = parse_text(msg)
                self.mail_message.append(message_text)
                # 根据邮件索引号直接从服务器删除邮件:
                if message_text is not None:
                    server.dele(i)
            server.quit()
        except Exception as error_receive:
            print(f'-* pop3: Receive error! *-\n{error_receive}')
            time.sleep(60)


if __name__ == '__main__':
    pass
