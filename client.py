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
# inserimento messaggio
message = input(str("Io : "))
print ('sending "%s"' % message)
message = binarycode(message)
print(message)
#invio lunghezza bit del messaggio
len = str(len(message))
s.sendto(len.encode(),(host, 1024))
len = int(len)
#inizalizzazione finestra
sixzeWind=int(input("Inserisci la dimensione della finestra -> ")) # dimensione della finestra
windMaxIndex = sixzeWind - 1
windMinIndex = 0

sent=0 # bit in trasmissione
ack=""

while windMinIndex!=len:
    # invia pacchetti finché c'è spazio nella finestra
    while sent <= windMaxIndex and sent!=len:
        if random.random() > 0.007:# pacchetto perso 0.7% dei casi
            print("pacchetto ", sent, "inviato : ",message[sent])
            pacchetto = str(sent) + ":" + message[sent]
            bitSent = s.sendto(pacchetto.encode(),(host, 1024))
        else:
            print("pacchetto ", sent, "perso")
        sent += 1
        
    ack, addr = s.recvfrom(1024)
    ack = ack.decode()
    ack, descr = ack.split(":")
    ack=int(ack)
    print("ack ricevuto: ", ack)
    print("descrizione: ", descr)
    if descr == "time":
       print("ACK non valido ricevuto, ignorato.")
    elif(ack==windMinIndex):
        print("ack OK")
        windMaxIndex += 1
        windMinIndex += 1
    else:
        print("ack ERRORE")
        sent = windMinIndex
        print("ritrasmissione pacchetto...")
