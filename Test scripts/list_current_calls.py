import serial
import time

def list_current_calls(port, baudrate):
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

        # List current calls
        ser.write(b'AT+CLCC\r')
        time.sleep(1)
        response = ser.read(ser.inWaiting()).decode(errors='ignore')
        if 'OK' in response:
            print("Current Calls:")
            calls = response.split('\r\n')
            for call in calls:
                if call.startswith('+CLCC:'):
                    parts = call.split(',')
                    call_id = parts[0].split(': ')[1]
                    direction = 'Outgoing' if parts[1] == '0' else 'Incoming'
                    status = ['Active', 'Held', 'Dialing', 'Alerting', 'Incoming', 'Waiting', 'Disconnect'][int(parts[2])]
                    mode = ['Voice', 'Data', 'Fax'][int(parts[3])]
                    mpty = 'Multiparty' if parts[4] == '1' else 'Single'
                    number = parts[5].replace('"', '') if len(parts) > 5 else 'Unknown'
                    print(f"Call ID: {call_id}")
                    print(f"Direction: {direction}")
                    print(f"Status: {status}")
                    print(f"Mode: {mode}")
                    print(f"Multiparty: {mpty}")
                    print(f"Number: {number}")
                    print("---")
            return True
        else:
            print("Failed to list current calls")
            return False

    except Exception as e:
        print(f"Error: {e}")
        return False

    finally:
        ser.close()

# Example usage
if list_current_calls('/dev/serial0', 9600):
    print("Listed current calls successfully")
else:
    print("Failed to list current calls")
