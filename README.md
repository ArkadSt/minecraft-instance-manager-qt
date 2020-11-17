# minecraft-instance-manager-qt

This is the PyQt5 version of the program minecraft-instance-manager.
minecraft-instance-manager is the program makes possible to have multiple instances of Minecraft with their own set of mods, resourcepacks, etc.

### List of contributors
ArkadSt - developer  
ra1nlox - developer

## Dependencies
minecraft_instance_manager needs **PyQt5** package in order to work.  
It can be easily installed by performing `pip install PyQt5`

## Launch
You need Python3 (https://www.python.org/downloads/) in order to run this program.
If you have installed Python3, you can run the program by executing this command in console:

```
Linux, MacOS: python3 minecraft-im.py
Windows:      python minecraft-im.py
```

***NB! On Windows this program requires administrative priveleges because on Windows only administrators can create symlinks. You can either run it from admin console, or it will just ask you for admin rights.***

## How does this program work

The active instance folder is used as a Minecraft folder.
Minecraft folder is stored here:

```
Windows:    %appdata%\.minecraft
Linux:      ~/.minecraft
MacOS:      ~/Library/Application Support/minecraft
```

The Minecraft folder becomes a symlink, targeted at the active instance folder.

## How to manage Minecraft instances
Instance folder can be managed just like a normal Minecraft folder.
Minecraft instances are stored here:

```
Windows:    %appdata%\.minecraft-instance-manager\instances
Linux:      ~/.minecraft-instance-manager/instances
MacOS:      ~/Library/Application Support/minecraft-instance-manager/instances
```
*On MacOS you can access `~/Library/Application Support/` using Spotlight. Just type `~/Library/Application Support/` into the prompt*

After creating, the instance folder already has such folders as `mods`, `resourcepacks`, `saves`.
Install everything you need there.

By modifying the Minecraft folder you modify the active Minecraft instance. The active instance can be chosen using **minecraft-instance-manager**. Other operations can be performed using **minecraft-instance-manager** or manually as well (by renaming, deleting or manually creating instance folders). My utility just makes the management part easier (I hope).

___
*P.S. **minecraft-instance-manager** adds `instance_name.mp3` in the root of the created instance folder, which is only needed for identification of the active instance if you go directly to Minecraft folder for example. It is safe to be removed if you don't want it there.*
