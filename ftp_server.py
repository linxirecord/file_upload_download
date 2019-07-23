import socketserver,os

class Ftp_server(socketserver.BaseRequestHandler):

    def handle(self):
        while True:
            data = self.request.recv(1024).decode()
            print(data)
            data = data.split('|')
            if hasattr(self,data[0]):
                func = getattr(self,data[0])
                func(data[1:])

    def file_transfer(self,cmd):
        if cmd[0] == 'get':
            print("going to send file:%s"%(cmd[1]))
            file_name = cmd[1]
            if os.path.isfile(file_name):
                file_size = int(os.path.getsize(file_name))
                msg = "file_transfer|get|ready|%s"%(file_size)
                self.request.send(msg.encode())
                client_ack = self.request.recv(1024).decode()
                if client_ack.startswith("file_transfer|get|recv|ready"):
                    with open(file_name,'rb')as f:
                        send_size = 0
                        while not file_size == send_size:
                            if file_size - send_size > 1024:
                                data = f.read(1024)
                                send_size += len(data)
                            else:
                                data= f.read(file_size-send_size)
                                send_size += file_size-send_size
                            self.request.send(data)
                        else:
                            print("文件传输完成")
                else:
                    print(client_ack)
            else:
                msg = b"file_transfer|get|don`t exist"
                self.request.send(msg)

        elif cmd[0] == 'put':
            print("going to put file:%s"%(cmd[1]))
            file_name = cmd[1]
            file_size = int(cmd[2])
            base_path = 'D:\python_project'
            ack_msg = b"transfer|put|ready"
            self.request.send(ack_msg)
            recv_size = 0
            place_file_dir = os.path.join(base_path,file_name)
            with open (place_file_dir+'2','wb')as f:
                while not file_size == recv_size:
                    if  file_size - recv_size > 1024:
                        data = self.request.recv(1024)
                        recv_size += len(data)
                    else:
                        data = self.request.recv(file_size-recv_size)
                        recv_size += file_size-recv_size
                    f.write(data)
                print("文件上传成功")

        else:
            pass

if __name__ == '__main__':
    HOST,PORT = 'localhost',9999
    server = socketserver.ThreadingTCPServer((HOST,PORT),Ftp_server)
    server.serve_forever()
