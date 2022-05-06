
# SMART BUS SYSTEM


## CLOUD 

``` 
    DATABASE
    
    docker run -it --name smart_bus_db  -p 7118:3306 -e MYSQL_ROOT_PASSWORD=test -e LANG=en_US.UTF-8 -v /home/$USER/mysql:/var/lib/mysql -d mysql:5.7

    with out persistent

    docker run -it --name smart_bus_db  -p 7118:3306 -e MYSQL_ROOT_PASSWORD=test -e LANG=en_US.UTF-8  -d mysql:5.7

    
    GRPC
    
    git clone https://github.com/yitbarek123/SMART-BUS.git
    cd SMART-BUS
    cd cloud    
    docker build -t raspberry-pi .
    docker run --network host -it raspberry-pi bash   
    python3 smart_bus.py
     
```


## RASPBERRY-PI

``` 
    git clone https://github.com/yitbarek123/SMART-BUS.git
    cd SMART-BUS
    cd cloud
    cd raspberry-pi
    python3 sensors.py

```

