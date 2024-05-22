import serial
import time
import threading
import binascii

class SIM800LV2:
    def __init__(self, port='/dev/serial0', baudrate=9600, timeout=1):
        self.serial_port = serial.Serial(port, baudrate, timeout=timeout)
        self.incoming_call_thread = None
        self.new_message_thread = None
        self.running = False
        self.initialize_modem()

    def send_command(self, command, delay=1):
        # print(f"Sending command: {command}")  # Debugging
        self.serial_port.write((command + '\r').encode())
        time.sleep(delay)
        response = self.serial_port.read(self.serial_port.inWaiting()).decode(errors='ignore')
        # print(f"Response: {response}")  # Debugging
        return response

    def initialize_modem(self):
        # Basic modem setup
        self.send_command('AT')
        self.send_command('ATE0')  # Echo off
        self.send_command('AT+CMGF=1')  # Set SMS to text mode

    def call_number(self, number):
        response = self.send_command(f'ATD{number};')
        return response

    def end_call(self):
        response = self.send_command('ATH')
        return response

    def reject_call(self):
        response = self.send_command('ATH')
        return response

    def read_sms(self, index):
        response = self.send_command(f'AT+CMGR={index}')
        return response

    def delete_sms(self, index):
        response = self.send_command(f'AT+CMGD={index}')
        return response

    def list_current_calls(self):
        response = self.send_command('AT+CLCC')
        return response

    def send_sms(self, number, message):
        self.send_command(f'AT+CMGS="{number}"')
        self.serial_port.write((message + '\x1A').encode())  # \x1A is Ctrl+Z
        time.sleep(3)  # Pause in order for modem to have time to send message recomended in docs 2 - 5s
        response = self.serial_port.read(self.serial_port.inWaiting()).decode(errors='ignore')
        # print(f"SMS send response: {response}")  # Debugging
        return response

    def handle_incoming_call(self, caller_number):
        print(f"{caller_number} Just called")
        self.reject_call()

    def check_incoming_call(self):
        while self.running:
            response = self.send_command('AT+CLCC', delay=0.5)
            if '+CLCC:' in response:
                caller_number = self.parse_caller_number(response)
                if caller_number:
                    self.handle_incoming_call(caller_number)
            time.sleep(1)

    def parse_caller_number(self, response):
        lines = response.split('\n')
        for line in lines:
            if '+CLCC:' in line:
                parts = line.split(',')
                if len(parts) > 5:
                    return parts[5].strip('"')
        return None

    def check_new_message(self):
        while self.running:
            response = self.send_command('AT+CMGL="REC UNREAD"', delay=0.5)
            if '+CMGL:' in response:
                messages = self.parse_new_messages(response)
                for message in messages:
                    self.handle_new_message(message)
            time.sleep(5)  # Proveravajte na svakih 5 sekundi

    def parse_new_messages(self, response):
        messages = []
        lines = response.split('\n')
        for i in range(len(lines)):
            if '+CMGL:' in lines[i]:
                parts = lines[i].split(',')
                if len(parts) > 1:
                    message_index = parts[0].split(':')[1].strip()
                    sender = parts[2].strip('"')
                    message = lines[i+1].strip()
                    messages.append((message_index, sender, message))
        return messages

    def handle_new_message(self, message):
        message_index, sender, message_text = message
        decoded_message = self.decode_message(message_text)
        print(f"New message from {sender}: {decoded_message}")
        # Delete message after reading
        self.delete_sms(message_index)

    def decode_message(self, message):
        try:
            bytes_message = binascii.unhexlify(message)
            decoded_message = bytes_message.decode('utf-16-be')
            return decoded_message
        except Exception as e:
            return f"Failed to decode message: {e}"

    def start_incoming_call_check(self):
        if not self.running:
            self.running = True
            self.incoming_call_thread = threading.Thread(target=self.check_incoming_call)
            self.incoming_call_thread.start()

    def stop_incoming_call_check(self):
        self.running = False
        if self.incoming_call_thread:
            self.incoming_call_thread.join()

    def start_new_message_check(self):
        if not self.running:
            self.running = True
            self.new_message_thread = threading.Thread(target=self.check_new_message)
            self.new_message_thread.start()

    def stop_new_message_check(self):
        self.running = False
        if self.new_message_thread:
            self.new_message_thread.join()

    def stop(self):
        self.stop_incoming_call_check()
        self.stop_new_message_check()

