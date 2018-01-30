# Alexa_TiVo_Control
Controlling your TiVo using an Amazon Echo & a Raspberry Pi is pretty easy to set up using this code.

This code runs on top of a program that is called Fauxmo, a program that emulates a Belkin WeMo device. The Belkin WeMo is a smart outlet, so our code turns our Raspberry Pi into a fake smart outlet, allowing us to turn ON or turn OFF any code we program.

The program I created allows our Raspberry Pi to TelNet into our TiVo and change the channels, or perform remote control actions.

Steps Required:
----------------------------------------------------------------------------------
1: Setup your TiVo to allow it to be controlled via a network connection

2: Download code on your raspberry pi (your pi needs Python installed to run) 

3: Edit downloaded code (Your TV channel numbers will be different than the code)

4: Have Alexa discover new devices (so it learns what channels are programmed)

5: Setup your Pi to start our program everytime the pi boots up

Step 1: TiVo Setup (TiVo HD Instructions).
----------------------------------------------------------------------------------
Hit your TiVo Remote button and go to Messages & Settings

Choose Settings

Choose Remote, CableCard, & Devices

Choose Network Remote Control

Choose Enable

Press Thumbs Up, Thumbs Up, Thumbs Up

Your TiVo can now be controlled via TelNet commands over port 31339

Step 1: Tivo Setup (TiVo Bolt Instructions)
----------------------------------------------------------------------------------
Hit your TiVo Remote button and go to Messages & Settings

Choose Remote, CableCard, & Devices

Choose Network Remote Control

Choose Allow Network-based remote controls

Step 2: Download Code
----------------------------------------------------------------------------------
First verify that your Raspberry Pi is running Python. (This programming language is required to run our code.)

On your pi, type: python 

If Python is installed, the pi will show which version is installed. Hit Control+D to exit the Python infomation screen

next type the following

git clone https://github.com/shrocky2/Quick_Alexa_TiVo.git

-- if you get an error "git: command not found", install git by typing: sudo apt-get install git

this will download our code to a directory called "Quick_Alexa_TiVo" (minus the quotation marks), change to this directory

type: cd Quick_Alexa_TiVo

There are 2 files that you DON'T need to modify, "fauxmo.py" & "debounce_handler.py", so just forget they exist.


Step 3: Edit Code to Match your Channel Situation
----------------------------------------------------------------------------------
The TiVo.py file needs to be edited to personalize the TV channels that Alexa can change on the TiVo.

Alexa can only learn 12 new devices at a given time. (Alexa only searches for new 'devices' for 20 seconds, which is only enough time to learn 12 devices.)

To edit the program enter the following: sudo nano TiVo.py

Near the Top, you will see TV Stations followed by their Channel Number. Edit to your liking.

Just below that section, you will see a similar section, only change the TV Stations to match the changes in the above section.

Just below that code (still in the TiVo.py file), you need to find the line that says "TiVo_IP_Address"

Change the IP Address the address of your TiVo, I Suggest you give your TiVo a Static IP Address (As well as your Raspberry Pi)

(hit Control + X to Save Changes)

Step 4: Have Alexa discover new devices
----------------------------------------------------------------------------------
Repeating what I said before, Alexa can only learn 12 new devices at a given time. (Alexa only searches for new 'devices' for 20 seconds, which is only enough time to learn 12 devices.)

type: python TiVo.py

--if you get an error about REQUESTS not installed, type: sudo apt-get install python-requests

Speak to Alexa, "Alexa discover devices"

Alexa should have learned all 12 channels (she'll call them devices)

Test the program with Alexa...Just say "Alexa, turn on N.B.C." or "Alexa, turn Comedy Central on"

Step 5: Setup your pi to start our program everytime the pi boots up
----------------------------------------------------------------------------------
type: sudo nano /etc/rc.local

At the very bottom, right above "exit 0" type the following:

sudo python /home/pi/Quick_Alexa_TiVo/TiVo.py &

Make sure you add the ampersand (&) at the end of that line. This symbol tells our code to run in the background and allow the system to run other programs, otherwise other programs may NOT start up.

(hit Control + X to Save Changes)

Finally we can reboot the system, type the following:

sudo reboot

The End, Enjoy your Alexa Controlled TiVo
----------------------------------------------------------------------------------
