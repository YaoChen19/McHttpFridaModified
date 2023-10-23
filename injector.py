import frida
import sys
import os

LOG_FILE_MAX_SIZE = 1000000  # Establecer el tamaño máximo del archivo de registro en bytes
BUFFER_SIZE = 100000  # Establecer el tamaño del búfer en bytes

logFile = None
start_position = 0

def setup_log_file():
    global logFile, start_position
    logFile = open('log.txt', 'w', encoding='utf-8')
    logFile.seek(0, os.SEEK_END)
    current_position = logFile.tell()
    if current_position < BUFFER_SIZE:
        start_position = 0
    else:
        start_position = current_position - BUFFER_SIZE

def on_message(message, data):
    global logFile, start_position
    if message['type'] == 'send':
        print(message['payload'], file=logFile)
    else:
        print(message, file=logFile)

    current_position = logFile.tell()
    if current_position - start_position > LOG_FILE_MAX_SIZE:
        roll_log_file()

def roll_log_file():
    global logFile, start_position
    logFile.seek(start_position)
    buffer = logFile.read(BUFFER_SIZE)
    logFile.close()

    logFile = open('log.txt', 'w')
    logFile.write(buffer)
    logFile.flush()

# Inicializar archivo de registro
setup_log_file()


with open("nohttpinterceptor.js", "r") as jscodeFile:
    jscode = jscodeFile.read()

def main():
    def process_messages(message, data):
        if message['type'] == 'send':
            print(message['payload'])
        else:
            print(message)

   
    device = frida.get_usb_device()

    
    process = device.attach("InfoJobs")

   
    script = process.create_script(jscode)
    script.on('message', on_message)

    print('[+] Running')
    script.load()
    sys.stdin.read()

    
    logFile.close()

if __name__ == '__main__':
    main()

