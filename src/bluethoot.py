#https://www.hondata.com/downloads/Bluetooth.pdf
import bluetooth

bd_addr = 'B0:B4:48:7B:94:38'
port = 1
sock = bluetooth.BluetoothSocket(bluetooth.RFCOMM)
sock.connect((bd_addr, port))
print(sock.send(bytearray([0x0, 0x31, 0xAF, 0x0])))

req = sock.recv(2048)
print(req)