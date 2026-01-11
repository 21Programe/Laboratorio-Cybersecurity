import socket

# Configuração para ouvir o broadcast da Tuya (Porta 6667 UDP)
UDP_PORT = 6667
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('', UDP_PORT))

print(f"[*] Escutando na porta {UDP_PORT}... Puxe a tela do App no celular agora!")

while True:
    data, addr = sock.recvfrom(2048)
    # Filtramos apenas o IP do seu dispositivo Tuya
    if addr[0] == "192.168.1.2":
        print(f"\n[+] Pacote interceptado de: {addr[0]}")
        
        # Tentamos extrair o texto legível (onde geralmente está o ID)
        texto_extraido = data.decode('utf-8', errors='ignore')
        print(f"Conteúdo: {texto_extraido}")
        
        if "devId" in texto_extraido:
            print(">>> SUCESSO: Device ID localizado no pacote!")
