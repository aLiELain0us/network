#!/usr/bin/python3
#!/utf/8in/FileSender

from    socket      import  socket,setdefaulttimeout
from    hashlib     import  md5
from    sys         import  argv
from    time        import  sleep
from    os          import  (path, listdir, mkdir,
                            chdir,getcwd)

def isit(txt,_Hash=0):
    if _Hash:return _Hash == md5(txt).hexdigest()
    else:return md5(txt).hexdigest()

def files(PATH,_files=[]):
    if path.isfile(PATH[:-1]):return [PATH[:-1]]
    for File in listdir(PATH):
        if path.isdir(PATH+File):
            files(PATH+File+'/')
        else:_files+=[PATH+File]
    return _files

def data(typ,conn):
    if typ == 'send':
        PATH = input('\nPATH_name : ')
        if not PATH:
            quit(conn.send(b'quit'))
        for File in files(PATH if PATH[-1]=='/' else PATH+'/'):
            #_f = File.replace('/',' ').replace('\\',' ').split()[-1]
            print('Sending ('+File+')... ',end='  ',flush=1)
            with open(File,'rb') as f:
                fr = f.read() ; sz = len(fr) ; _Hash = isit(fr);count = 0
                conn.send((File+'@'+str(sz)+'@'+_Hash).encode());conn.recv(2)
                cnd = fr[count:count+2048]
                while cnd: 
                    conn.send(cnd);count += 2048 ; cnd = fr[count:count+2048]
                print('OK');conn.recv(2)
    else:
        print('Waiting ...')
        try:File, sz, _Hash = conn.recv(1024).decode().split('@')
        except Exception as e:
            if 'timed out' in str(e):data(md,conn)
            else:quit('>>>'+str(e))
        conn.send(b'ok') ;count = 0 ; print('receving ('+File+')...',end=' ',flush=1)
        info=File.replace('/',' ').replace('\\',' ').split()
        old_path=getcwd()
        for i in info[:-1]:
            try:mkdir(i)
            except:pass
            chdir(i)
        with open(info[-1],'wb') as f:
            conn.settimeout(4)
            while 1:
                try:f.write(conn.recv(2048))
                except:break
            print('OK');conn.send(b'ok')
            conn.settimeout(300)
            chdir(old_path)

def connection(typ,ip,port):
    s = socket() ; #setdefaulttime(10)
    s.setsockopt(1,2,1)
    if typ == 'connect':
        print('Connecting to {} on {} ...'.format(ip,port), end=' ', flush=1)
        while True:
            try:s.connect((ip,port)) ; print('OK');return s
            except:sleep(2)
    else:
        print('Listenning from {} on {} ...'.format(ip,port), end=' ', flush=1)
        s.bind((ip,port)) ;s.listen(1)
        c,a = s.accept();print('OK') ; return c

def main():
    _help = '''
         _____________________________
         ||   connect   |     listen
    _____||-_-_-_-_-_-_-|_-_-_-_-_-_-_
         ||             |
    send ||     cs      |       ls
    _____||_____________|______________
         ||             |
    recv ||     cr      |       lr   
    _____||_____________|______________
    Ex: 
        $ ae_share (typ) (ip) (port)
        (ip/port): 
            (typ):Target_ip & port : cs or cr  # connect
            (typ):My_ip & port     : ls or lr  # listen
    
    '''
    try:
        typ,ip,port = input(_help+'typ ip port : ').split()
        dt = {'cs':'connect/send','cr':'connect/recv','ls':'listen/send' ,'lr':'listen/recv'}
        if not (typ in dt or typ[::-1] in dt):quit('Err: type of connection not found',_help)
        typ,md = dt[typ].split('/') if typ in dt else dt[typ[::-1]].split('/')
        conn = connection(typ,ip,int(port))
        while 1:
            try:data(md,conn);sleep(1)
            except Exception as e:print('>> ',e)#break
    except Exception as err:print(err)

if __name__ == '__main__':main()

#by:
#   aLi_eLainous
#   9.2.20
