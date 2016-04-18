# Introduction #

Details necessary on deploying a classcomm virtual box appliance.  First, please download and install the latest [VirtualBox](http://virtualbox.org) before continuing.


## Initial Setup ##

Most IT systems professionals would install classcomm by first CreateFromScratch and second ClasscommInstall.  However it is possible to import an existing ovf appliance--if you are interested in this option I can push you out a fresh copy.  Here are instructions ...

### How-to Import Existing ovf Appliance ###
Open Virtualbox and now we want to import the ovf appliance:
  * Select File -> Import Appliance and choose the _classcomm.ovf_ file and **import**.

Now, we need to verify settings of the new virtual machine; With classcomm highlighted click settings.
  * Under System, Motherboard tab: adjust down the base memory when you read warnings.
  * Under System, Processor tab: check that "Enable PAE/NX" is enabled.
  * Under Network, verify adapter 1 is enabled and a host-only adapter.
  * Under Network, verify adapter 2 is enabled and attached-to NAT.

Exit settings by clicking OK


## Verify Working Network ##
Now start the new virtual machine.  Once started login with the default credentials:
classcomm/pass. Run the command:
```
ifconfig
```
We should see eth0, eth1 and lo, but it is likely that only lo is listed initially.  We need to clear out the network rules and reboot to see the changes.
```
sudo rm /etc/udev/rules.d/70-persistent-net.rules
sudo reboot
```
Once back up, login again and run ifconfig looking for the IP address of the eth0 adapter.  Look for a 192.168.56.X IP address (it is likely that X is 101)
```
ifconfig | less
```
  * piping to less allows you to view text before moving on; use enter to go forward and q to quit.
  * If eth0 is showing up but does not have an associated 192.168.56.X IP address, you may need to restart networking.  Run the following command sequence until ifconfig shows the IP address:
```
sudo service networking restart
ifconfig | less
```
Once the IP address is obtained try opening a browser and connecting to the IP address.
```
http://192.168.56.X
EX: If my IP is 192.168.56.101, I try http://192.168.56.101
```
We should see an "It Works!" page.


## Connecting to Classcomm ##
Once we have verified our web server is online, we can use the classcomm app.
The app home is: http://192.168.56.*X*/classcomm/handin/
This can be administered at: http://192.168.56.*X*/classcomm/admin/

The default username is classcomm and the default password is pass.


## Secure Your Instance ##
You are running an instance of freely available software.  While ultimately you are more secure running in a virtual environment such as virtual box, there are default passwords in place that should be made unique to your instance to prevent any possible hacking attempt.
  1. Most important--secure downloads by creating new secret pass.  Edit two files and adjust the secret pass (keep it consistent across files):
```
# nano is a text editor ctrl+s to save and ctrl+x to exit
# Look for line AuthTokenSecret and adjust to new secret pass in file:
nano /etc/apache2/httpd.conf
# Look for line AUTH_TOKEN_PASS and adjust to new secret pass (same) in file:
nano /var/django_projects/classcomm/settings.py
```
  1. Change the system password for our classcomm user:
```
passwd
```
  1. Change our classcomm user password on the web app.

## Configure Port Forwarding ##
At this point, our service is only accessible on our host machine.  In order to access our working web service from any network location we need to configure port forwarding for our virtual machine.  This will direct traffic on a host port to a port on the virtual machine allowing other machines on the network to use the classcomm service.  Inside of a command prompt, navigate to the virtualbox install directory, and execute:
```
cd C:\"Program Files\Sun\xVM VirtualBox
VBoxManage setextradata "classcomm" "VBoxInternal/Devices/pcnet/1/LUN#0/Config/apache/HostPort" 8080
VBoxManage setextradata "classcomm" "VBoxInternal/Devices/pcnet/1/LUN#0/Config/apache/GuestPort" 80\
VBoxManage setextradata "classcomm" "VBoxInternal/Devices/pcnet/1/LUN#0/Config/apache/Protocol" TCP
```
Shutdown your virtual machine and close VirtualBox for the new settings to take affect!
  * Change 8080 to another port if you already have a service running on the host machines port 8080 (this is unlikely)
  * You can’t use a host port lower than 1024 without running VirtualBox with escalated privileges.
  * To verify your settings try:
```
VBoxManage getextradata "classcomm" enumerate
```
  * To unset a setting try removing the argument, such as:
```
VBoxManage setextradata "classcomm" "VBoxInternal/Devices/pcnet/1/LUN#0/Config/apache/Protocol"
```
Now you are able to access the web service on the network by visiting the IP address of the host running VirtualBox and appending the port.  Example: http://192.168.0.143:8080
If you have a firewall on the computer it may be necessary to open the port before connections will be allowed.


## Beyond Apache ##

There is a ton of work being done in the space of web servers, and while we feel Apache2 is a hardened choice that best suits our need now, we are not opposed to other web servers and may choose a different default in the future.

[Twisted](http://twistedmatrix.com/trac/wiki/TwistedProject) is a networking engine written in Python, supporting numerous protocols. It contains a web server, numerous chat clients, chat servers, mail servers, and more.

[Eventlet](http://wiki.secondlife.com/wiki/Eventlet) is a networking library written in Python. It achieves high scalability and concurrency by using [non-blocking io and coroutines](http://www.python.org/dev/peps/pep-0342/).