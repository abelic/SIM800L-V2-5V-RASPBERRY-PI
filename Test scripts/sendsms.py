import serial
import time

def send_sms(port, baudrate, number, text):
    try:
        # Initialize the serial connection
        ser = serial.Serial(port, baudrate, timeout=1)
        time.sleep(0.5)
        
        # Ensure the module is ready
        ser.write(b'AT\r')
        time.sleep(0.5)
        response = ser.read(ser.inWaiting())
        if b'OK' not in response:
            print("Module not responding to AT command")
            return False

        # Set SMS to text mode
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        response = ser.read(ser.inWaiting())
        if b'OK' not in response:
            print("Failed to set SMS to text mode")
            return False

        # Set the recipient number
        ser.write(f'AT+CMGS="{number}"\r'.encode())
        time.sleep(0.5)
        response = ser.read(ser.inWaiting())
        if b'> ' not in response:
            print("Failed to set recipient number")
            return False

        # Send the SMS text
        ser.write((text + '\x1A').encode())
        time.sleep(5)  # Wait for the message to be sent
        response = ser.read(ser.inWaiting())
        if b'OK' in response:
            print("SMS sent successfully")
            return True
        else:
            print("Failed to send SMS")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        ser.close()

# Example usage
if send_sms('/dev/serial0', 9600, "Your_number", "Your_text"):
    print("SMS sent successfully")
else:
    print("Failed to send SMS")
