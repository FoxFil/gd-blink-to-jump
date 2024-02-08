# gd-blink-to-jump

This repository is a set of little programs to play Geometry Dash just by moving parts of your face or making sounds!

⚠ In all programs all faces in the camera area are detected, so you can even play with your friend!

⚠ There is a delay in all of the programs. Be careful!
### blink.py 👀

"W" is pressed when you blink. Or you can close your right eye for holding "W". It's a really fun experience so try it out!

### mouth.py 👄

"W" is pressed when you open your mouth. To hold "W" you can simply keep your mouth open.

### voice.py 🔊

"W" is pressed when your voice is higher than a treshold value (line 6). Keep your voice high to hold "W".

### platformer.py 🤩

That one is quite tricky to control! Close your **left** eye to move **right** (D), close your **right** eye to move **left** (A) and open your **mouth** to **jump** (W).

### libraries used 📚

- cv2
- dlib
- imutils
- scipy
- keyboard
- sounddevice (for `voice.py` only)
- matplotlib (for showing a diagram in `voice.py` only)

### creator 🧡

It's me, [FoxFil](https://github.com/FoxFil)! Enjoy!
