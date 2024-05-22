import serial
import time

def delete_sms(port, baudrate, index):
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

        # Delete the SMS message at the specified index
        ser.write(f'AT+CMGD={index}\r'.encode())
        time.sleep(0.5)
        response = ser.read(ser.inWaiting()).decode(errors='ignore')
        if 'OK' in response:
            print(f"SMS at index {index} deleted successfully")
            return True
        else:
            print(f"Failed to delete SMS at index {index}")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        ser.close()

# Example usage
if delete_sms('/dev/serial0', 9600, 2):
    print("SMS deleted successfully")
else:
    print("Failed to delete SMS")
