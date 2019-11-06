# UPS2

## Enable I2C in raspi-config
sudo raspi-config  
-Interfacing Options  
-I2C  
-Enable  
-Yes  

 ## View battery Info  
    wget https://github.com/geekworm-com/UPS2/raw/master/viewinfo.py  
    #edit viewinfo.py and modify battery capacity  
    nano viewinfo.py  
    #.Change 2500 to your battery capacity (mAh)  
    MY_BATTERY_CAP = 2500  
