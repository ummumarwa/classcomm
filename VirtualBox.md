# Introduction #

Oracle's VirtualBox is virtualization software that is freely available as Open Source Software under the terms of the GNU General Public License (GPL). You can download the software from the [VirtualBox Website](http://www.virtualbox.org/).


# Purpose and Branch Out #

VirtualBox allows us to install, run and configure guest operating systems virtually on any modern computer.  This aids in development and deployment of web software because we can configure a base development image (See: CreateFromScratch and InstallClasscomm) and from there test different additional 3rd party Django Apps without worrying about corrupting the system or bringing down production.  Simply configure a base development or release image and mirror that image to test multiple instances.  We recommend that new developers checkout classcomm and push development changes inside of a Virtual Machine running in VirtualBox.  This is the standard safe way to work on classcomm without side effects to your main environment.

> Additionally there are interesting tools emerging for managing VirtualBox instances.

  * [php VirtualBox AJAX web interface](http://code.google.com/p/phpvirtualbox/)  This will prove useful for managing several instances of classcomm running on Virtual Box.  We offer these tools and solutions as an alternative to running classcomm on any EC2 type cloud which also should be supported.