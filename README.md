# UPS2

## Enable I2C in raspi-config
sudo raspi-config  
-Interfacing Options  
-I2C  
-Enable  
-Yes  

## Run setup  
    wget https://github.com/geekworm-com/UPS2/raw/master/ups2_setup.sh  
    chmod +x ./ups2_setup.sh  
    sudo ./ups2_setup.sh  
    ┌─────────────────┤ GEEKWORM WORKSHOP UPS2 ├───────────────┐
    │ Select the appropriate options:                          │
    │                                                          │
    │                1 Select Poweroff GPIO(#6 OR #13)         │
    │                2 Enable Poweroff function                │
    │                3 Disable Poweroff function               │
    │                4 Exit                                    │
    │                                                          │
    │                                                          │
    │                                                          │
    │                                                          │
    │                          <Ok>                            │
    │                                                          │
    └──────────────────────────────────────────────────────────┘
  
Option 1: Select poweroff GPIO  
Option 2: Enable Poweroff function  
Option 3: Disable Poweroff function  
Option 4: Exit  
  
## View battery Info  
    wget https://github.com/geekworm-com/UPS2/raw/master/viewinfo.py  
    edit viewinfo.py and modify battery capacity  
    nano viewinfo.py  
    #.Change 2500 to your battery capacity (mAh)  
    MY_BATTERY_CAP = 2500  
