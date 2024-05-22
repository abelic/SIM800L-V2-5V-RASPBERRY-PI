import serial
import time
from collections import defaultdict

def read_sms(port, baudrate):
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

        # Set SMS to text mode
        ser.write(b'AT+CMGF=1\r')
        time.sleep(0.5)
        response = ser.read(ser.inWaiting()).decode(errors='ignore')
        if 'OK' not in response:
            print("Failed to set SMS to text mode")
            return False

        # List all SMS messages
        ser.write(b'AT+CMGL="ALL"\r')
        time.sleep(1)
        response = ser.read(ser.inWaiting()).decode(errors='ignore')
        if 'OK' in response:
            print("Received SMS messages:")
            messages = response.split('\r\n')
            sms_parts = defaultdict(str)
            for message in messages:
                if message.startswith('+CMGL'):
                    parts = message.split(',')
                    index = parts[0].split(' ')[1]
                    status = parts[1].replace('"', '')
                    sender = parts[2].replace('"', '')
                    timestamp = ','.join(parts[4:6]).replace('"', '')
                    print(f"Index: {index}")
                    print(f"Status: {status}")
                    print(f"Sender: {sender}")
                    print(f"Timestamp: {timestamp}")

                elif message and not message.startswith('AT') and not message.startswith('OK'):
                    # Decode UCS2 message content
                    try:
                        content = bytes.fromhex(message).decode('utf-16-be')
                        sms_parts[timestamp] += content
                    except Exception as e:
                        print(f"Failed to decode message content: {e}")
            
            # Print concatenated messages
            for timestamp, content in sms_parts.items():
                print(f"Timestamp: {timestamp}")
                print(f"Content: {content}")
            return True
        else:
            print("Failed to read SMS messages")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        ser.close()

# Example usage
if read_sms('/dev/serial0', 9600):
    print("SMS read successfully")
else:
    print("Failed to read SMS")
