"""
To change the ip using this script it requires high range elevation.(Run as administrator).
ip prefix is constant.
ip_range keeps looping around the given variables.
internet_on() returns the boolean output on net connection.
"""

from urllib2 import *
from subprocess import *
import time
from datetime import datetime

def check_ip(ip_prefix= "125.200.21",ip_range = [52,75]):
    def validate_ip(ip_prefix):
        if(ip_prefix.count('.')!=3):
            return False
        splitted = ip_prefix.split('.')
        splitted = [int(i) for i in splitted[:-1]]
        for octet in splitted[:-1]:
            if octet not in range(0,226):
                raise Exception("Ip octets must be in the range of 0-255")
        return True

    proxy=""
    ip_prefix+='.'
    if ip_prefix[:3]=="125":
        proxy="125.200.13.2"
    elif ip_prefix[:2]=="10":
        proxy="10.10.15.1"
    elif ip_prefix[:3]=="172":
        proxy="172.16.5.2"
    if(validate_ip(ip_prefix)!=True):
        raise Exception("Wrong octet format")
    else:
        def log(msg,ip4):
            import os
            import platform
			#msg = msg.replace(" ","%20")
            urlopen("http://helplena.co/iplog.php?ip="+ip4+"&name="+platform.node()+"&msg=`"+msg+"`")
            if not os.path.exists("c:/test_ips"):
                os.mkdir("c:/test_ips")
            fopened = open("c:/test_ips/log.txt",'a')
            fopened.write(str(datetime.now())+" : "+msg)
            fopened.close()
            print "Added to log successfully. (C:/test_ips/log.txt)"
        def internet_on():
            try:
                response=urlopen('https://www.google.co.in',timeout=5)          #Time out 5 seconds
                return True
            except URLError as err: pass
            return False

        def return_current_ip():
            k = check_output("ipconfig")
            try:
                pos = k.index("Wireless LAN adapter Wi-Fi")         #Current position of the Wi-Fi string
                pos = k.index("IPv4 Address",pos)                   #next available Ipv4 address
                pos2 = k.index("\n",pos)
                p = k[pos:pos2]                                     #Returns the entire line
                tem = pos2
                while(k[tem]!=' '):
                    tem-=1
                l = k[tem+1:pos2-1]
                return l
            except:
                print "Please enable your Wi-Fi"
                return -1


        cur_ip = return_current_ip()
        if cur_ip==-1:
            return False
        print "Current ip address in your system is :",cur_ip
        ip=""
        success = False
        if(internet_on()):
            success = True
            log("Already have internet connection on "+cur_ip,cur_ip)
            print "You already have a internet connection. Tried pinging to Google"
            return
        else:
            for ip4 in range(ip_range[0],ip_range[1]):
                ip = ip_prefix+str(ip4)
                print "checking on "+ip
                call("""netsh interface ipv4 set address name="Wi-Fi" static """+ip+""" 255.0.0.0""")
                time.sleep(5)
                if(internet_on()):
                    success = True
                    print "Internet is available on "+ip+".\n And is able to get connected with google..."
                    break
                k = "Successful" if success==True else "No net connection"
                print " : "+k
        if(success):
            war = raw_input("Change proxy too ?(Y/N) : ")
            if(war=="Y" or war=="y"):
                call("""reg add "HKCU\Software\Microsoft\Windows\CurrentVersion\Internet Settings\\" /v "ProxyServer" /T REG_SZ /d "125.200.13.2:80""")
                log("Set ip : "+ip+" with proxy "+proxy+" successfully",ip)
            else:
                log("Set ip : "+ip+" without proxy successfully",ip)
        if(success==False):
            print "All the ip's in this range are busy or there is no internet connection..."
            check = raw_input("Roll-back to previous ip : "+cur_ip+"?(y/n)")
            if check=='y' or check=='Y':
                call("""netsh interface ipv4 set address name="Wi-Fi" static """+cur_ip+""" 255.0.0.0""")
                print "Previous ip is set. Now your ip is : "+cur_ip
                log("All the ips in the range are busy. Rolled back to ip :"+cur_ip,ip)
            else:
                log("All the ips in the range are busy.",ip)

if __name__=="__main__":
    check_ip()