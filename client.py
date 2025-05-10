# Simulazione del protocollo Go-Back-N con socket UDP
# CLIENT 
"""
@authors: Alice Beccati
"""
import time, socket, random

# definizione funzione di conversione decimale in binario
def decimalToBinary(n):  
    return n.replace("0b", "0")

#definizione della funzione di trasposizione da utf-8 in binario
def binarycode(s):
    a_byte_array = bytearray(s, "utf8")
    byte_list = []

    for byte in a_byte_array:
        binary_representation = bin(byte)
        byte_list.append(decimalToBinary(binary_representation))

    #print(byte_list)
    a=""
    for i in byte_list:
        a=a+i
    return a

#creazione del socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
ip = socket.gethostbyname(host) 
port = 1235 

#while True:
try:
        # inviate il messaggio
        message = input(str("Io : "))
        print ('sending "%s"' % message)
        time.sleep(2) #attende 2 secondi prima di inviare la richiesta
        message=binarycode(message)
        print(message)
        #invio lunghezza bit del messaggio
        len = str(len(message))
        s.sendto(len.encode(),(host, 1024))

        sent=0 # bit in trasmissione
        wind=int(input("Inserisci la dimensione della finestra -> "))-1 # dimensione della finestra
        len=int(len)
        ack=""
        

        while sent!=len:
            print("pacchetto ", sent, "inviato : ",message[sent])
            bitSent = s.sendto(message[sent].encode(),(host, 1024))
            time.sleep(1)
            ack, addr = s.recvfrom(1024)
            print("ack ricevuto: ", ack)
            ack=ack.decode()
            if(ack!="lost"):
                time.sleep(1)
                print("ack RIVEVUTO")
                sent=sent+1
            else:
                print("ack PERSO")
                time.sleep(1)
                print("ritrasmissione pacchetto...")
                
except Exception as info:
        print(info)