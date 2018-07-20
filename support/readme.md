# Support

This file contains instructions for lab setup of all devices and cleanup after the first time devices have been used. Also there are a few useful scripts here as well. 

## Super Simple Clean

To do the clean without checking out any code, just enter one of the following commands directly on the device.

```
sudo sh -c "$(curl -fsSL https://bit.ly/2LxtJwY)"
```

or 

```
sudo sh -c "$(curl -fsSL https://raw.githubusercontent.com/kenstler/aws-ml-iot-lab/master/support/cleanup.sh)"
```

## Configuring the Device ( first time )

When these kits arive they are missing:
* Wifi Software
* WPA Security Software

The following instructions and scripts [here](https://github.com/chrisking/upsquaredsetup) cover everything that is needed to patch the kits via automation or with specific commands.

## Triaging Network Connectivity

If the device will not connect to the network remove the following lines from `/etc/network/interfaces`

```
        wpa-ssid MYSSID
        wpa-psk fun_key_here
```

Then enter the following command with the values changed for the SSID and passkey:

```shell
wpa_passphrase MYSSID MySecretPassphrase | grep -vE "{|#|}" | tr -d '\t' | sudo tee -a /etc/network/interfaces
```

## Loading Support Content Onto the Device:

It is a good idea to keep a local copy of the lab content and all supporting content on the device, to do so enter the following:

```shell
sudo mkdir /labs
sudo chown -R upsquared /labs
cd /labs
git clone https://github.com/chrisking/upsquaredsetup.git
git clone https://github.com/chrisking/aws-ml-iot-lab.git
```

If the content is already in `/labs` on the device enter the following to ensure it is up to date.

```shell
cd /labs/aws-ml-iot-lab
git pull origin master
cd /labs/upsquaredsetup
git pull origin master
```

## After Lab Cleanup

Before packing the UpSquared devices into their boxes for the next lab, the systems must be restored to a clean state. This process has been automated via a script provided below but the rough directions are below if they need to be performed manually

Removing all Greengrass content from the home directory:
```shell
cd ~/
rm greengrass-ubuntu*.*
rm ML*.*
```

Remove the Greengrass directories:
```shell
sudo rm -rf /greengrass
```

Remove the Greengrass user and group:
```shell
sudo groupdel ggc_group
sudo userdel ggc_user
sudo rm -rf /home/ggc_user
```

Or to make this super simple since you've cloned the support repo:

```shell
sudo /labs/aws-ml-iot-lab/support/cleanup.sh
```


## Full Restore ( Worst Case )

The absolute worst case scenario is a bricked device or the passwords have been changed. If that occurs find a local Linux Desktop( a Deep Lens would work in a pinch) or a local Linux VM with a Desktop and a 16GB or greater USB drive.

Follow the instructions [here](https://downloads.up-community.org/download/up-squared-iot-grove-development-kit-ubuntu-16-04-server-image/) to restore the UpSquared kit to its original factory settings.