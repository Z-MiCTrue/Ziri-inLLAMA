import os
import time

# 包结构 & 脚本
if os.getcwd() == os.path.split(os.path.realpath(__file__))[0]:
    from mail.mail_receive import Mail_Receiver
    from mail.mail_send import Mail_Sender
    from mail.mail_options import Mail_Options
else:
    from .mail.mail_receive import Mail_Receiver
    from .mail.mail_send import Mail_Sender
    from .mail.mail_options import Mail_Options


def cmd_return(cmd):
    # run
    os.chdir('./llama.cpp-master/')
    res = os.popen(f'./main -m models/7B/ggml-model-q4_1.bin  -p "{cmd}" --color')  # --mlock
    try:
        res_text = res.buffer.read().decode('utf-8')
    except UnicodeDecodeError:
        res_text = res.buffer.read().decode('gbk')
    res.close()
    return res_text


class Ziri_inLLAMA:
    def __init__(self):
        mail_opt = Mail_Options()
        self.mail_receiver = Mail_Receiver(mail_opt)
        self.mail_sender = Mail_Sender(mail_opt)

    def run(self):
        # log dir
        ori_dir = os.getcwd()
        os.chdir(os.path.split(os.path.realpath(__file__))[0])
        # receive
        self.mail_receiver.get_message()
        for mail_unit in self.mail_receiver.mail_message:
            print(f'mail content: {mail_unit}')
            if mail_unit[-1] is not None:
                with open('log.txt', 'a') as logger:
                    logger.write(f'{mail_unit[-1]}\n')
            answer = cmd_return(mail_unit[-1])
            self.mail_sender.edit_text(subject_content=f'Reply to: {mail_unit[0]}', body_content=answer)
            self.mail_sender.send_email(mail_unit[1])
            self.mail_sender.msg = None
        self.mail_receiver.mail_message = []
        # return dir
        os.chdir(ori_dir)


if __name__ == '__main__':
    ziri_inllama = Ziri_inLLAMA()
    while True:
        ziri_inllama.run()
        time.sleep(300)
