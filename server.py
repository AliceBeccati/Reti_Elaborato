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

#while True:
print("server avviato...\n")
len, addr = s.recvfrom(1235)
len = len.decode()
len = int(len)
print("lunghezza del messaggio: ", len)
expectedN = 0 # pacchetto ricevuto

while expectedN != len:
        s.settimeout(1)  # 1 secondo di timeout
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
                        ack = str(receivedN) + ":" + "ack"
                        expectedN = expectedN + 1
                s.sendto(ack.encode(), addr)
                print("ack inviato", ack)
        except socket.timeout:
                print("⏳ Timeout: nessun pacchetto ricevuto")
                ack = str(expectedN - 1) + ":" + "time"
                s.sendto(ack.encode(), addr)