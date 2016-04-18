# Introduction #

This document describes building and configuring a Virtual Machine Environment running classcomm from scratch.  This document describes the processes using VirtualBox and Ubuntu Linux.  In the future we will look at classcomm on and Ubunutu Enterprise Cloud or Amazon EC2.

First, please download and install the latest free [Oracle VirtualBox](http://virtualbox.org) for your host operating system, before continuing.

# Download and Install Guest OS #
**Estimated Total Time: 2 hours (30 min for download and 1.5 hr for install)**<br />
Before we can configure classcomm to run on a virtual host, we need to create and install our virtual host.  While any Operating System could be used here, we are tailoring these instructions for the server release of Ubuntu 10.10 64-bit which will be the latest release until 11.04 in April of 2011.  Download the 64-bit [server iso](http://www.ubuntu.com/server/get-ubuntu/download) and launch Oracle VM VirtualBox.

### Create New Virtual Machine ###
**Estimated Time: 10 minutes**
  1. Click New to begin a New Virtual Machine Wizard and select next.
  1. Choose a name like "classcomm\_release" and Operating System to "Linux" and version to "Ubuntu (64 bit)" and click Next.
  1. Set the Base Memory to appropriate Size (example: 512MB) and click Next.
  1. Check "Boot Hard Disk" and "Create new hard disk" and click Next twice.
  1. Select "Dynamically expanding storage" and click Next.
  1. If you wish, change the location/name of your new hard disk.
  1. Select a maximum size for your disk of at least 4 GB.  We recommend using a higher value such as 8 GB--this is the value our dev images are set at.
  1. Finish creating your new virtual machine.

Now we have a configured virtual machine and are now ready to install the Ubuntu guest operating system.

### Point to Installation Media ###
**Estimated Time: 5 minutes**
  1. Highlight the name of your virtual machine (Example: classcomm\_release) and click settings.
  1. Navigate to the Storage section: Under IDE controller it may say 'Empty' or 'Host Drive _:'  Make sure to set it as 'Host Drive_:'
  1. Click the icon next to 'Host Drive _:' to Open Virtual Media Manager.
  1. Click Add under 'CD/DVD Images' and navigate to the ISO you downloaded.  Choose Select, Click OK to leave settings menu._

### Install Guest OS ###
**Estimated Time: 45 minutes**
  1. Highlight your new virtual machine and click start.
  1. Select OK and acknolwedge any warnings about mouse placement or color depth.
  1. Select language (default: English).
  1. Select Install Ubuntu Server.
  1. Continue to fill out the install forms.  We suggest you do not detect keyboard layout, and instead select USA (or appropriate) from the list.  Use Tab to toggle between form elements.
  1. Change your hostname from ubuntu to classcomm-release or something more appropriate for your organization.
  1. Set your timezone.
  1. Partioning: 'Guided-Use Entire Disk and setup LVM.'  Select Disk.  Write changes to the disk.  Continue with default (full) disk size.
  1. Create default account; we recommend using a familiar username, but user 'classcomm' could work.  Secure and remember the password--you will use it to administer the new system and install classcomm.
  1. Leave the HTTP proxy blank and Continue.
  1. Install Security Updates Automatically.
  1. Select Selection: Add "OpenSSH server" and Continue.
  1. Install Grub Bootloader -- Yes
  1. Finish the installation and reboot into your new system.
  1. Unmount the installation media inside the Virtual Media Manager to prevent it from loading the installer again.

Now you have a fresh install of Ubuntu Server and are able to login using the credentials (username/password) you created during the install..  Try out your new host by running some unix commands.


### Configure and Verify Networking ###
**Estimated Time: 30 minutes**<br />

We have a working system, but to interact with it better we want need more network configuration for Internet and local access.

  1. Shutdown your virtual machine if running.  For example, the command `sudo halt` will do this.
  1. Highlight virtual machine, Click Settings and go to Network tab.
  1. Set Adapter 1 as Enabled, Attached-to Host-only Adapter.
  1. Set Adapter 2 as Enabled, Attached-to NAT.
  1. Click OK to Save, and now start up your virtual machine again.
  1. Login once started, Now add our second interface to the networking configuration by editing the file:
```
# nano is a text editor ctrl+s to save and ctrl+x to exit
sudo nano /etc/network/interfaces
```
  1. Adding the following lines to the end:
```
# The secondary network interface
auto eth1
iface eth1 inet dhcp
```
  1. And Restarting networking by running the command:
```
sudo /etc/init.d/networking restart
```
  1. Once restarted, check that IP address of the eth0 and eth1 adapters.  Look for a eth0 with 192.168.56.X IP, and a eth1 with 10.0.X.X IP.  The 192.168.56.X address gets you access from the host to the guest, and the 10.0.X.X address gives the guest access to the Internet. View IP config info:
```
ifconfig | less
```
  * piping to less allows you to view text before moving on; Use enter to go forward, and q to quit.
  * IF eth0 or eth1 is showing up without an associated 192.168.56.X IP address, try restarting networking again by repeating the previous two commands.


# Get Working With SSH #
**Linux Users:**
Simply user ssh from the terminal to connect to your running virtual host at the at the 192.168.56.X address that your guest OS has acquired on eth0.

**Windows Users:**
There are other programs (cygwin, msys and Putty) that make administering a virtual machine much easier than working directly in the virtual box console because you can get more text on the screen and you can copy and paste between your host and guest without adding extra software.

Cygwin (like msys) is a Linux-like environment for Windows.  It can be installed with OpenSSH and then used to connect using ssh to the virtual host at the 192.168.56.X address that your guest OS has acquired on eth0.

Putty is specifically an ssh client for Windows.  [Get Putty](http://www.chiark.greenend.org.uk/~sgtatham/putty/download.html) and launch the program to connect using ssh to the virtual host at the 192.168.56.X address that your guest OS has acquired on eth0.

# Install classcomm #

Congratulations, you now have a VirtualBox Host ready for [ClasscommInstall](ClasscommInstall.md).  Please proceed to the [ClasscommInstall](ClasscommInstall.md) install guide.