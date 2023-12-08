from multiprocessing import Process
import mouseControl

class MyProcess(Process): #继承Process类
    def __init__(self,name,mouse):
        super(MyProcess,self).__init__()
        self.name = name
        self.mouse = mouse
        self.x = 1
        self.y = 1

    def run(self):
        while True:
            self.mouse.move(self.x, self.y)

    def mouseMoveSet(self,x,y):
        self.x = x
        self.y = y


# if __name__ == '__main__':
#     process_list = []
#     for i in range(5):  #开启5个子进程执行fun1函数
#         p = MyProcess('Python') #实例化进程对象
#         p.start()
#         process_list.append(p)
#
#     for i in process_list:
#         p.join()
#
#     print('结束测试')