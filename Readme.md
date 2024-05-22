Tested with RPI1 B rev 2.0, but it should work with all models

Be sure not to use a wire connection with older SIM800L modules because they use lower voltages!


I also included some scripts I used for testing that have some additional functionality, like deleting SMS.
I also included a PHP API file that receives a bearer token, JSON message, and number, and forwards them to a Python script to send an SMS.

In this repo, you can find the official module serial AT commands manual for further improvements.


The script is not perfect and it has strange bugs, like a 1KB MMS I received when I was testing and didn't hang up a call. However, the API for sending SMS seems to work fine.

Wire connection:

P1:

         3V3  (1) (2)  5V    
       GPIO2  (3) (4)  5V    
       GPIO3  (5) (6)  GND   
       GPIO4  (7) (8)  GPIO14
         GND  (9) (10) GPIO15
      GPIO17 (11) (12) GPIO18
      GPIO27 (13) (14) GND   
      GPIO22 (15) (16) GPIO23
         3V3 (17) (18) GPIO24     
      GPIO10 (19) (20) GND   
       GPIO9 (21) (22) GPIO25
      GPIO11 (23) (24) GPIO8 
         GND (25) (26) GPIO7 


SIM800L V2 5V    Raspberry PI BV2

   Power section:

       5VIN    ->  (2)  5V 
       GND     ->  (6)  GND      
   UART TTL section:
   
       VDD     ->  3V3  (1)    (Found in docs: it doesn't need to be connected for the module to work, but I haven't tried it)
       TXD     ->  (10) GPIO15
       RXD     ->  (8)  GPIO14
       GND     ->  GND  (9)
RST (Used to hard reset the module, function not implemented; it doesn't have to be connected for this to work)

    RST     ->  (16) GPIO23

Raspberry PI Setup

    sudo apt update
    sudo apt -y upgrade
    sudo apt -y install python3-serial

    sudo sed -i '1s/^/enable_uart=1\n/' /boot/firmware/config.txt

sudo raspi-config Here go to Interface Options, than to Serial Port. 
Answer No to first promt " Would you like a login shell to be accessible over serial" and Yes to second "Would you like the serial port hardware to be enabled?"


    sudo usermod -a -G dialout $USER

    sudo reboot


Web server API Setup

    sudo apt install -y apache2 php8.2 

    # add files to /var/www/html folder


Files ownership and permissions:
    -Run commands from the /var/www/html folder.

    sudo usermod -a -G dialout www-data
    sudo chown www-data:www-data send-sms.php
    sudo chmod 644 send-sms.php
    sudo chown www-data:www-data send_sms.py
    sudo chmod 755 send_sms.py
    sudo chown www-data:www-data sim800lv2.py
    sudo chmod 755 sim800lv2.py

    sudo service apache2 restart
