import socket,os

class Ftp_client(object):
    def __init__(self,host,port):
        self.host = host
        self.port = port
    def get(self,cmd):
        if len(cmd) > 0:
            newfile_name = cmd[0]
            msg = "file_transfer|get|%s"%(newfile_name)
            self.sock.send(msg.encode())
            server_back = self.sock.recv(1024).decode()
            if server_back.startswith("file_transfer|get|ready"):
                file_size = int(server_back.split('|')[-1])
                ack_msg = b"file_transfer|get|recv|ready"
                self.sock.send(ack_msg)
                with open(newfile_name+'3','wb')as f:
                    recv_size = 0
                    while not file_size == recv_size:
                        if file_size - recv_size > 1024:
                            data = self.sock.recv(1024)
                            recv_size += len(data)
                        else:
                            data = self.sock.recv(file_size-recv_size)
                            recv_size += file_size - recv_size
                        f.write(data)
                    print ("文件下载完成")
            else:
                print (server_back)

    def put(self,cmd):
        if len(cmd) > 0:
            local_filename = cmd[0]
            if os.path.isfile(local_filename ):
                file_size = int(os.path.getsize(local_filename))
                msg = "file_transfer|put|%s|%s"%(local_filename,file_size)
                self.sock.send(msg.encode())
                server_back = self.sock.recv(1024).decode()
                print("服务器正常，可以进行传输")
                if server_back.startswith("transfer|put|ready"):
                    with open(local_filename,'rb')as f:
                        send_size = 0
                        while not send_size == file_size:
                            if file_size - send_size > 1024:
                                data = f.read(1024)
                                send_size +=1024
                            else:
                                data = f.read(file_size-send_size)
                                send_size += file_size-send_size
                            self.sock.send(data)
                        else:
                            print("文件上传完成")
                else:
                    print (server_back)

    def interactive(self):
        '''客户端交互'''
        while True:
            cmd_list = input("请输入你需要执行的操作get or put:").strip().split()
            if len(cmd_list) == 0:
                continue

            if hasattr(self,cmd_list[0]):
                func = getattr(self,cmd_list[0])
                func(cmd_list[1:])
            else:
                print("输入错误，请重新输入")
    def connect(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect((self.host, self.port))
        self.interactive()

if __name__ == '__main__':
    ftp = Ftp_client('localhost',9999)
    ftp.connect()