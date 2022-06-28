# Gravel

Gravel is my Summer 2022 personal project. This project focuses on creating an Arch Linux ARM compute cluster using low-cost Rock64 Single-Board Computers (SBC) and utilizing it to analyze data gathered from the European Space Agency's Space Debris Database.

## Purpose

The purpose of this project is to learn and demonstrate my knowledge of engineering principles and technologies through the design, building, and testing process. This project also demonstrates my knowledge of networking technologies, Unix and Linux tools, data science technologies and principles, and professional engineering principles. More generally, this project also demonstrates the accessibility of higher-end computing technologies to the average engineering student.

## Project Overview

This project consists of two main parts, the compute cluster itself and the data analysis for which it is used. The compute cluster is made up of 3 Rock64 2GB SBCs running Arch Linux ARM, managed by the SLRUM workload manager in conjunction with OpenMPI.

## Setup and Instructions

This section will detail instructions for the setup of the cluster and the R scripts.

### Compute Cluster Setup

#### Materials

Materials needed for this project:

- 3x Pine64 Rock64 2GB SBCs
- 3x MicroSD Cards (16GB preferred)
- 3x Rock64 Power Supplies (5V/3A)
- 4x Ethernet Patch Cables
- 1x 6-port 10/100/1000 network switch

#### Rock64 Initialization and Startup

The first step of the project is to get the Rock64 boards running smoothly. This requires the flashing of the Arch Linux ARM image to the MicroSD cards. The commands to do this are listed below (Note that these steps were done on a computer running OpenSuSe Tumbeleweed).

First we zero the MicroSD card and format it (sdb in this case is the MicroSD card).

```bash
$ sudo dd if=/dev/zero of=/dev/sdb bs=1M count=32
$ sudo fdisk /dev/sdb
// Type O, P, N, P, 1, 32768, ENTER, w
$ sudo mkfs.ext4 /dev/sdb1
$ mkdir root
$ sudo mount /dev/sdb1 root
```
Next we get the Arch Linux ARM image and flash it to the card. We also flash the required firmware and U-boot bootloader.

```bash
$ wget http://os.archlinuxarm.org/os/ArchLinuxARM-aarch64-latest.tar.gz
$ sudo tar -xzvf ArchLinuxARM-aarch64-latest.tar.gz -C root
$ sudo wget http://os.archlinuxarm.org/os/rockchip/boot/rock64/boot.scr -O root/boot/boot.scr
$ sudo umount root
$ wget http://os.archlinuxarm.org/os/rockchip/boot/rock64/rksd_loader.img
$ wget http://os.archlinuxarm.org/os/rockchip/boot/rock64/u-boot.itb
$ sudo dd if=rksd_loader.img of=/dev/sdb seek=64 conv=notrunc
$ sudo dd if=u-boot.itb of=/dev/sdb seek=16384 conv=notrunc
```
Now that the image has been flashed successfully, insert the microSD card into the Rock64 board and connect it to power and ethernet. Once the board has booted up, find the IP of the board and ssh into it. The default user is alarm with alarm as the password. The root user password is root. Once you have logged in, login to the root user and initialize the pacman keyring and populate the Arch Linux ARM package signing keys using the commands below.

```bash
$ su
# pacman-key --init
# pacman-key --populate archlinuxarm
```
Additionally, remove the boot.scr file manually downloaded previously and install the U-Boot package. Then reboot the board.

```bash
# rm /boot/boot.scr
# pacman -Sy uboot-rock64
# reboot
```

Now that the basic setup of the Rock64 is done, we'll move onto getting the board setup for the cluster.

#### User Setup & Cluster Networking

In this section we will setup NTP and the networking for the board and user settings as well. First, we need to set the correct timezone and install some needed packager for later.

```bash
$ su
# timedatectl set-timezone
# pacman -Syu
# pacman -Sy sudo inetutils macchanger
```
Now that sudo is installed we can go ahead and add alarm to the sudoers group for easier management.

```bash
# usermod -aG wheel alarm
# nano /etc/sudoers
// Uncomment the Wheel group line
# exit
```
Next we can go ahead and set the static ip for the board as well as change the MAC address. Changing the MAC address is needed as the boards only come with one default MAC address and this causes network issues when multiple boards are used.

```bash
$ sudo systemctl stop dhcpcd.service
$ sudo systemctl disable dhcpcd.service
$ cd /etc/netctl
$ sudo cp examples/ethernet-static ./eth0
$ sudo nano ./eth0
// edit this file to set the desired static IP and save
$ sudo netctl enable eth0
$ sudo netctl start eth0
$ sudo systemctl stop systemd-networkd
$ sudo systemctl disable systemd-networkd
$ sudo reboot
```
Once the board is rebooted, you can now ssh from the static IP.

//IN PROGRESS

## Disclaimer

This project is currently in progress, and as such the documentation is incomplete. If you have any questions regarding this project and repository, please email arihan.srirangapatnam@gmail.com.



