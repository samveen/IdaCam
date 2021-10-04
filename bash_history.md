# Bash history
The following is a sanitized version of the setup required for the software side
of things for the raspberry pi. For the full mess, check the bash_history.fail.txt
and bash_history.success.txt for details of the 2 different system iterations the
camera went through.

    # OS upgrade
    sudo apt update
    sudo apt upgrade
    sudo apt autoremove
    sudo reboot
    sudo apt dist-upgrade
    sudo apt install vim
    sudo reboot

    # hostname
    sudo sed -i 's/raspberrypi/idacam/' /etc/hosts
    sudo hostnamectl --static set-hostname idacam
    sudo hostnamectl --transient set-hostname idacam
    sudo hostnamectl --pretty set-hostname idacam
    sudo hostnamectl set-icon-name camera-photo
    sudo reboot

    # enable hw clock and disable the fake-hwclock
    sudo systemctl disable fake-hwclock.service
    sudo update-rc.d -f fake-hwclock remove
    sudo apt purge fake-hwclock 
    sudo dpkg-reconfigure tzdata 
    # comment out the section that checks for '/run/systemd/system' and exits
    sudo vim /lib/udev/hwclock-set
    sudo timedatectl set-ntp off
    sudo reboot

    # TTY mirroring to SPI display
    sudo apt install git cmake dkms
    git clone https://github.com/juj/fbcp-ili9341.git
    cd fbcp-ili9341/
    git grep ILI9341
    cmake -DILI9341=ON -DSPI_BUS_CLOCK_DIVISOR=6 -DGPIO_TFT_DATA_CONTROL=22 -DGPIO_TFT_RESET_PIN=27 -DDISPLAY_ROTATE_180_DEGREES=ON -S . -B build/
    cd build/
    make
    file fbcp-ili9341 
    sudo install -s -t /usr/local/sbin fbcp-ili9341 
    ls -l fbcp-ili9341 /usr/local/sbin/fbcp-ili9341 
    cd ..
    tee fbcp.service <<_ENDL
    [Unit]
    Description=Fast Framebuffer Copy Service for the Raspberry Pi
    StartLimitIntervalSec=10

    [Service]
    Type=simple
    EnvironmentFile=/etc/fbcp.conf
    Restart=always
    RestartSec=1
    StartLimitBurst=2
    ExecStart=/usr/local/sbin/fbcp-ili9341

    [Install]
    WantedBy=default.target
    _ENDL
    tee fbcp.conf <<_ENDL
    # Config for the fbcp service.
    # Nothing here yet, just a placeholder for future configuration.
    _ENDL
    sudo install -m 0644 -t /etc/systemd/system fbcp.service 
    sudo install -m 0644 -t /etc fbcp.conf 
    ls -l /etc/systemd/system/fbcp.service /etc/fbcp.conf 
    sudo systemctl daemon-reload
    sudo systemctl enable fbcp
    sudo systemctl start fbcp
    sudo systemctl status fbcp
    sudo reboot

    # enable camera module and enable auto-login on tty1
    sudo raspi-config 
    sudo reboot
    raspistill -o test.jpg

    # check python and install required packages
    which python
    python --version
    python3 --version

    sudo apt install python-six
    sudo apt install --no-install-recommends fbi

    # Mount last partition of sdcard on DCIM
    mkdir DCIM
    cat /etc/fstab 
    vim /etc/fstab 
    sudo vim /etc/fstab 
    sudo mount DCIM/
    bash -c 'cd DCIM/ && sudo chown pi:pi .'

    # uinput and autoloading it
    sudo lsmod |grep uinput
    sudo modprobe uinput
    sudo lsmod |grep uinput
    sudo dmesg |tail
    ls -l /etc/modules-load.d/
    cat /etc/modules
    sudo tee /etc/modules-load.d/load-uinput.conf <<_ENDL
    # Load uinput for terminal input control via fauxcon
    uinput
    _ENDL

    # set up group based access to uinput 
    sudo groupadd uinput
    getent group uinput
    sudo usermod -a -G uinput pi
    sudo ls -l /etc/udev/rules.d/99-uinput.rules
    sudo tee /etc/udev/rules.d/99-uinput.rules <<_ENDL
    # group for access to uinput group
    KERNEL=="uinput", GROUP="uinput", MODE:="0660"
    _ENDL

    # install fauxcon
    sudo apt search fauxcon
    git clone 'git@github.com:lornix/fauxcon.git'
    cd fauxcon/
    make
    sudo make install
    ls -l /usr/local/bin/fauxcon 
    file /usr/local/bin/fauxcon fauxcon

    # Some extra memory using swap, as we're running at half the usual (half given to gpu mem for raspistill)
    sudo free -h
    sudo swapon -s
    cat /etc/fstab 
    man dphys-swapfile 
    cat /etc/dphys-swapfile 
    sudo systemctl list-units '*swap*'
    sudo systemctl status '*swap*'
    cat /lib/systemd/system/dphys-swapfile.service
    cat /lib/systemd/system/swap.target
    sudo systemctl stop dphys-swapfile 
    sudo sed -i 's/^.*CONF_SWAPFACTOR.*/CONF_SWAPFACTOR=1/' /etc/dphys-swapfile 
    sudo systemctl start dphys-swapfile 
    ls -lh /var/swap
    free -h

    # Disable a few unneeded services to decrease system resource usage even more
    sudo systemctl list-units
    sudo systemctl status '*avahi*'
    sudo systemctl list-units '*avahi*'
    sudo systemctl stop '*avahi*'
    sudo systemctl list-unit-files '*avahi*'
    sudo systemctl disable avahi-daemon.service avahi-daemon.socket
    sudo systemctl list-unit-files '*avahi*'
    sudo systemctl list-units 
    sudo systemctl list-unit-files '*lue*'
    sudo systemctl stop bluetooth.service dbus-org.bluez.service
    sudo systemctl disable bluetooth.service dbus-org.bluez.service
    sudo systemctl list-unit-files bluetooth.service dbus-org.bluez.service
    sudo systemctl list-units 
    sudo systemctl status hciuart.service
    sudo systemctl stop hciuart.service
    sudo systemctl disable hciuart.service

    # check on components of the system and test them
    cd $HOME

    sudo raspinfo
    sudo less raspinfo.txt 

    man raspistill
    raspistill --help

    vim test.py
    python test.py


    # shortcut development
    wget 'https://gist.githubusercontent.com/elktros/faa43bbf413d4414e2cbbea580143d05/raw/fa20d16aa3fcd1749117a7d9f58131656cab55c8/Raspberry_Button_Tutorial.py'
    vim Raspberry_Button_Tutorial.py

    vim led.py 
    python led.py 

    vim button.py 
    python button.py 

    # Magic complete, but check references for inner workings of magic
    vim camera.py 
    python camera.py 

    # Auto run for the camera app
    cat >>.bashrc <<_ENDL

    # Start camera code in background on tty1
    if tty | grep -q tty1; then
      python camera.py >>camera.log 2>&1 &
    fi
    _ENDL

    # It's ALIVE
    sudo reboot

