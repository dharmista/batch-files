import socket
import threading

def test(pizza,piece):
    try:
        status = socket.gethostbyaddr(pizza + str(piece))
    except Exception as e:
        status = ("IP is free",)

    print "{0} : {1}".format(pizza + str(piece), status[0])

ip = "125.200."

third = raw_input("Enter third piece :")

fourth = raw_input("Enter range as low,high :").split(",")

pizza = ip+third+"."
for piece in range(int(fourth[0]),int(fourth[1])+1):
    t = threading.Thread(test(pizza,piece))
    t.start()