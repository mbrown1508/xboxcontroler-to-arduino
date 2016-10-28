main.py
=======

This is a simple program that reads in a xbox controler input and sends the information to an arduino using the serial port. It is based of the Xbox controler library here - https://github.com/FRC4564/Xbox

Requires that xboxdrv be installed first:

    sudo apt-get install xboxdrv

To test the driver, issue the following command and see if the controller inputs are recognized

    sudo xboxdrv --detach-kernel-driver

See http://pingus.seul.org/~grumbel/xboxdrv/ for details on xboxdrv

You can run the sample code to test the xbox.py class.

    sudo python sample.py

Example arduino program usage:

	TBA

Note:
Running with sudo privileges to allow xboxdrv necessary control over USB devices.
If you want, you can provide your user account with the proper access, so you needn't use sudo.

First, add your user to the root group. Here's how to do this for the user ‘pi’

    sudo usermod -a -G root pi

Create a permissions file using the nano text editor.

    sudo nano /etc/udev/rules.d/55-permissions-uinput.rules

Enter the following rule and save your entry.

    KERNEL=="uinput", MODE="0660", GROUP="root"
