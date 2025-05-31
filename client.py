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

while True:
    # inserimento messaggio
    message = input(str("MESSAGGIO : "))
    print ('sending "%s"' % message)
    message = binarycode(message)
    print(message)
    #invio lunghezza bit del messaggio
    leng = str(len(message))
    s.sendto(leng.encode(),(host, 1024))
    leng = int(leng)
    #inizalizzazione finestra
    sixzeWind=input("Inserisci la dimensione della finestra -> ") 
    s.sendto(sixzeWind.encode(),(host, 1024))
    sixzeWind = int(sixzeWind)
    windMaxIndex = sixzeWind - 1
    windMinIndex = 0

    sent=0 # bit in trasmissione
    ack=""

    #statistiche
    received_ack = 0
    lost = 0
    resend = 0

    while windMinIndex!=leng:
        # invia pacchetti finché c'è spazio nella finestra
        while sent <= windMaxIndex and sent!=leng:
            if random.random() > 0.01:# pacchetto perso 1% dei casi
                print("pacchetto ", sent, "inviato : ",message[sent])
                pacchetto = str(sent) + ":" + message[sent]
                bitSent = s.sendto(pacchetto.encode(),(host, 1024))
            else:
                print("pacchetto ", sent, "perso")
                lost += 1
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
            received_ack += 1
            windMaxIndex += 1
            windMinIndex += 1
        else:
            print("ack ERRORE")
            sent = windMinIndex
            resend += (windMaxIndex - windMinIndex + 1)
            print("ritrasmissione pacchetto...")
        
    #statistiche
    print("Su ",leng," pacchetti :","\n- ",resend," ritrasmessi","\n- ",received_ack," ack corretti ricevuti","\n- ",lost," persi")
