from serial import Serial
import time

def make_data():
    ARDUINO = Serial("COM3", baudrate=9600, timeout=1)

    AMOSTRAS = 128
    dado = []
    time.sleep(2)

    for i in range(AMOSTRAS):
        linha = ARDUINO.readline().decode('utf-8').strip()
        if linha.isdigit():
            dado.append(int(linha))

    ARDUINO.close()
    with open('dado_nada.txt', 'w') as file:
        for item in dado:
            file.write(str(item) + '\n')

if __name__ == '__main__':
    make_data()