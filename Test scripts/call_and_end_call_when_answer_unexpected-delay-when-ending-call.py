import serial
import time

def dial_and_check_call(port, baudrate, number):
    try:
        # Initialize the serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(0.5)

        # Ensure the module is ready
        ser.write(b'AT\r')
        time.sleep(0.5)
        response = ser.read(ser.inWaiting()).decode(errors='ignore')
        if 'OK' not in response:
            print("Module not responding to AT command")
            return False

        # Dial the number
        ser.write(f'ATD{number};\r'.encode())
        time.sleep(1)
        response = ser.read(ser.inWaiting()).decode(errors='ignore')
        if 'OK' not in response and 'CONNECT' not in response:
            print("Failed to dial the number")
            return False

        print(f"Dialing {number}...")

        # Check the call status
        while True:
            ser.write(b'AT+CLCC\r')
            time.sleep(0.5)
            response = ser.read(ser.inWaiting()).decode(errors='ignore')
            if '+CLCC:' in response:
                parts = response.split(',')
                call_status = int(parts[2].strip())
                if call_status == 0:  # Active call
                    print("Call answered, hanging up")
                    ser.write(b'ATH\r')
                    time.sleep(0.5)
                    ser.read(ser.inWaiting()).decode(errors='ignore')
                    print("Call ended")
                    return True
            time.sleep(1)

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        ser.close()

# Example usage
if dial_and_check_call('/dev/serial0', 9600, 'Your_number'):
    print("Call handled successfully")
else:
    print("Failed to handle call")
