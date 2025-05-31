# Simulazione del protocollo Go-Back-N con socket UDP
# SERVER 
"""
@authors: Alice Beccati
"""
import time, socket

#definisco la funzione per convertire il binario in testo utf-8
def bin2text(s): return "".join([chr(int(s[i:i+8],2)) for i in range(0,len(s),8)])

#creazione del socket UDP
s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
host = socket.gethostname()
ip = socket.gethostbyname(host) 
port = 1024 
s.bind((host, port))

while True:
        s.settimeout(None)
        print("server IN ASCOLTO...\n")
        
        while True:  #controllo che non arrivino pacchetti non validi
                l, addr = s.recvfrom(1235)
                l = l.decode()
                if ":" not in l:      
                        l = int(l)
                        print("lunghezza del messaggio: ", l)
                        break


        wind, addr = s.recvfrom(1235)
        wind = wind.decode()
        wind = int(wind)
        print("lunghezza della finestra: ", wind)

        expectedN = 0 # pacchetto ricevuto
        messages = ""
        
        while expectedN != l:
                s.settimeout(wind * 0.5)  # timeout si adatta alla dimensione della finestra
                try :
                        message, addr = s.recvfrom(1235)
                        message = message.decode()
                        seq, bit = message.split(":")
                        receivedN = int(seq)
                        print("pacchetto RICEVUTO", receivedN, "==", expectedN)
                        if receivedN != expectedN:
                                print("ordine errato, pacchetto perso")
                                ack = str(expectedN - 1) + ":" + "ack"
                        else:
                                print("ordine corretto")
                                messages = messages + bit
                                ack = str(receivedN) + ":" + "ack"
                                expectedN = expectedN + 1
                        s.sendto(ack.encode(), addr)
                        print("ack inviato", ack)
                except socket.timeout:
                        print("Timeout: nessun pacchetto ricevuto")
                        ack = str(expectedN - 1) + ":" + "time"
                        s.sendto(ack.encode(), addr)
 
        print("mess == ", bin2text(messages))