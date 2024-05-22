import sys
from sim800lv2 import *

modem = SIM800lV2()

def main(number, message):
    modem.send_sms(number,message)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: your_script.py <number> <message>")
        sys.exit(1)
    number = sys.argv[1]
    message = sys.argv[2]
    main(number, message)
