import serial
import time

def check_incoming_call(port, baudrate):
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

        # Enable Caller ID presentation
        ser.write(b'AT+CLIP=1\r')
        time.sleep(0.5)
        response = ser.read(ser.inWaiting()).decode(errors='ignore')
        if 'OK' not in response:
            print("Failed to enable caller ID presentation")
            return False

        print("Waiting for incoming calls...")

        while True:
            if ser.inWaiting():
                response = ser.read(ser.inWaiting()).decode(errors='ignore')
                if 'RING' in response:
                    # Wait for CLIP response
                    time.sleep(1)
                    response += ser.read(ser.inWaiting()).decode(errors='ignore')
                    if '+CLIP' in response:
                        start = response.find('"') + 1
                        end = response.find('"', start)
                        caller_number = response[start:end]
                        print(f"Incoming call from: {caller_number}")

                        # Hang up the call
                        ser.write(b'AT+CHUP\r')
                        time.sleep(0.5)
                        ser.read(ser.inWaiting())
                        print("Call rejected")

                        return True
                time.sleep(0.1)

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        ser.close()

# Example usage
if check_incoming_call('/dev/serial0', 9600):
    print("Call handled successfully")
else:
    print("Failed to handle call")
