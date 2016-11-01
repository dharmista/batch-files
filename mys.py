import socket,struct
import subprocess
from urllib2 import urlopen, URLError
cmds = ["test_ips","free","starth","stoph","scan"]
import test_ips,os

def connection():
    try:
        response = urlopen('https://www.google.co.in', timeout=5)  # Time out 5 seconds
        return True
    except URLError as err:
        pass
    return False

def main(user = "Baba"):
    ip = socket.gethostbyname(socket.gethostname())
    print "Welcome to {1} {0}.".format(user,os.environ.get("OS"))
    test_ips.check_ip()
    if not connection():
        print "No net connection..."
    while(1):
        try:
            cmd = " ".join(raw_input(">>> ").split())
            if cmd in cmds:
                print "Under development"
            else:
                subprocess.call(cmd)
        except WindowsError as e:
            print "no such command as {0}".format(cmd)
        except Exception as e:
            print "Bye!"

if __name__ == '__main__':
    main()