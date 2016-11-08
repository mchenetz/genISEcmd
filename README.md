# genISEcmd
Python Script to autoconfigure ports for ISE. This script will discover VLANs and add them to the dead action vlan config.

Here is a script I wrote for the USER PORTS piece of the ISE Config. It will accomplish the following:

*	Connect to the switch you want to generate a ISE config on.
*	Parse all access ports
    *	Check access ports for any routers and skip if router
    *	Check for APs and configure the port for AP
    *	Configure fail open VLAN by determining access VLAN

To run the script you must download python 3 from python.org and install it. You must then add two packages from the command line:

`Pip install ciscoconfparse`

`Pip install netmiko`

After everything is installed then run the script from the command line with the following command:

`Python genisecmd.py [Switch IP] [username] [password]`


Disclaimer:
*** This will only generate port configuration! You will still need to add Global config when configuring ISE. Please check the work and verify too. Don’t rely on this only ***

