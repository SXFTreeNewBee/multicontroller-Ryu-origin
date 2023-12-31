# -*-coding:utf-8-*-
from ConRecMsgProcess import ConRecMsgProcess
import json
import  settings
from StreamInfo import InfoProcess
class ConRec(object):
    def __init__(self,socket,controller):
        """
        :param socket: 套接字对象
        :param controller: controller对象，用于操控外部的controller
        """
        super(ConRec, self).__init__()
        self.socket=socket
        self.log=InfoProcess()
        self.controller=controller
        self.MsgProcess=ConRecMsgProcess(controller)#实例化接收消息的处理对象
    def deco(self,msg):
        """
        :param msg: 需要加码的消息内容 bytes->str
        :return: 返回加码后的内容
        """
        return msg.decode(encoding='utf-8')
    def rec_loop(self):  # 接受消息循环
        while self.controller.status:
            try:
                message = self.socket.recv(settings.CLIENT_RECV_BUFSIZE)# 接受TCP数据,1024bytes
                if message:

                    mess = self.deco(message)

                    mess_list = mess.split(settings.MsgBarrier)

                    if mess_list[-1] != '':
                        mess_list.pop(-1)

                        mess_list.append('')

                    for msg in mess_list:

                        if msg != '':
                            # 解析为python对象，为字典
                            self.MsgProcess.process(json.loads(msg))  # 根据种类，选择处理方式
                else:
                    break
            except Exception as e:
                raise e
    #生成器
    def y(self,x):
        yield from x