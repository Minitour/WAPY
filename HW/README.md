# Installing Ubuntu on Intel Compute Stick with Atom Core

### Pre-requirements for installation

To install Ubuntu on Intel compute stick we will need a bootable 'USB' drive with at least '2GB' of storage, keyboard, mouse and a USB hub.

We will also need to make the USB drive bootable and we will do that with 'Rufus'. The installation of 'Rufus' is in this repo under HW folder.

1.  Open Rufus.
2.  Select under device the USB drive.
3.  Hit select button to select the image of the Ubuntu you want to install.
4.  Click on Start.

> There will be some warnings about erasing everything from the USB drive.

Now the USB is ready for installation.


### Installation

Connect the USB we mounted to the hub and boot the Compute Stick. Hit F2 until you get into the Bios.

> If you are having trouble entering into the Bios, follow this [link](https://www.youtube.com/watch?v=Q7UogsfKdM8) to boot into through the system.

When the Bios is loaded hit the right arrow to get into the Configurations, then go the Select Operation System Option and hit enter.
Select the 'Ubuntu' system from the list and hit F10 key to save & exit.
Now as the system loads hit the F10 key, then select the USB drive with the Ubuntu system.

Finally choose Install Ubuntu.

> You can first try running ubuntu without installing, instead of Installing Ubuntu, choose 'try ubuntu without installing'


### Configuring the installation

At the first page in the installation process you will need to configure the language of the system (Recommended English(US)), and hit continue.

Next choose 'Minimal Installation' which will install Web browser and some basic utils.

Check the 'Download update while installing ubuntu' and 'install third party software for graphics and wifi hardware and additional media formats' boxes.

In the third page check the 'erase disk and install ubuntu' box and also the 'check the use LVM with the new ubuntu installation' box for future integration.

> There will be a popup window, hit continue.

Now select your timezone.

In the last page you will need to provide some names and password for the system.

1. Name
2. Computer name
3. Username
4. Password (and confirm password)

and finally check the 'login automatically' box and hit continue.


The installation process will take about 25 minutes.
