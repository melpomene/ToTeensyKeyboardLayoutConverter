Generate keypress sequences for teensy from stdin
=================================================

This python script generates C files that compile to the teensy micro controller.

It will translate what it finds on stdin to keypresses on the teensy that will loop. 

Call it like 

    echo 'They see me trolling, they hating\n' | python LoopKeyboardGenerator.py 8
    make

and load the resulting troll.hex file into your teensy. This will cause the teensy to loop the input

    They see me trolling, they hating

imitating a keyboard device. 

Just steal my dictionary if you want to generate something else from stdin, it's simple!

I just built this as an example since I did not have the patience to translate every keypress I wanted to send manually. 

They usb_keyboard.c and usb_keyboard.h are forks from the teensy tutorial. 
