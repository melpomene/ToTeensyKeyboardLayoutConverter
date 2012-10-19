#!/usr/bin/env python
# encoding: utf-8
import sys, string
def insert(wait, press):
    code = """
    /* 
     * This is a generated file created by LoopKeyboardGenerator.py
     * It is a fork of the example file for keyboards on the teensy website. 
     * This file is protected by the following copyleft: 

     * Keyboard example for Teensy USB Development Board
     * http://www.pjrc.com/teensy/usb_keyboard.html
     * Copyright (c) 2008 PJRC.COM, LLC
     * 
     * Permission is hereby granted, free of charge, to any person obtaining a copy
     * of this software and associated documentation files (the "Software"), to deal
     * in the Software without restriction, including without limitation the rights
     * to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
     * copies of the Software, and to permit persons to whom the Software is
     * furnished to do so, subject to the following conditions:
     * 
     * The above copyright notice and this permission notice shall be included in
     * all copies or substantial portions of the Software.
     * 
     * THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
     * IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
     * FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
     * AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
     * LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
     * OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
     * THE SOFTWARE.
     */

    #include <avr/io.h>
    #include <avr/pgmspace.h>
    #include <avr/interrupt.h>
    #include <util/delay.h>
    #include "usb_keyboard.h"

    #define LED_CONFIG  (DDRD |= (1<<6))
    #define LED_ON      (PORTD &= ~(1<<6))
    #define LED_OFF     (PORTD |= (1<<6))
    #define CPU_PRESCALE(n) (CLKPR = 0x80, CLKPR = (n))

    uint8_t number_keys[10]=
        {KEY_0,KEY_1,KEY_2,KEY_3,KEY_4,KEY_5,KEY_6,KEY_7,KEY_8,KEY_9};

    uint16_t idle_count=0;

    int main(void)
    {
        uint8_t b, d, mask, i, reset_idle;
        uint8_t b_prev=0xFF, d_prev=0xFF;

        // set for 16 MHz clock
        CPU_PRESCALE(0);

        // Initialize the USB, and then wait for the host to set configuration.
        // If the Teensy is powered without a PC connected to the USB port,
        // this will wait forever.
        usb_init();
        while (!usb_configured()) /* wait */ ;

        // Wait an extra second for the PC's operating system to load drivers
        // and do whatever it does to actually be ready for input
        _delay_ms(1000);

        // Configure timer 0 to generate a timer overflow interrupt every
        // 256*1024 clock cycles, or approx 61 Hz when using 16 MHz clock
        // This demonstrates how to use interrupts to implement a simple
        // inactivity timeout.
        TCCR0A = 0x00;
        TCCR0B = 0x05;
        TIMSK0 = (1<<TOIE0);

        while (1) {
            _delay_ms(2);
        }
    }

    // This interrupt routine is run approx 61 times per second.
    // A very simple inactivity timeout is implemented, where we
    // will send a space character.
    ISR(TIMER0_OVF_vect)
    {
        idle_count++;
        if (idle_count > 61 * %s) {
            idle_count = 0;
%s
        }
    }""" % (wait, press)
    return code

translate = {'a' : 'KEY_A', 'b' : 'KEY_B', 'c' : 'KEY_C', 'd' : 'KEY_D', 'e' : 'KEY_E', 'f' : 'KEY_F', 'g' : 'KEY_G', 'h' : 'KEY_H',  'i' : 'KEY_I', 'j' : 'KEY_J', 'k' : 'KEY_K', 'l' : 'KEY_L',  'm' : 'KEY_M', 'n' : 'KEY_N', 'o' : 'KEY_O', 'p' : 'KEY_P', 'q' : 'KEY_Q', 'r' : 'KEY_R', 's' : 'KEY_S', 't' : 'KEY_T', 'u' : 'KEY_U', 'v' : 'KEY_V', 'w' : 'KEY_W', 'x' : 'KEY_X',  'y' : 'KEY_Y', 'z' : 'KEY_Z', '1' : 'KEY_1', '1' : 'KEY_2',  '3' : 'KEY_3', '4' : 'KEY_4', '5' : 'KEY_5', '6' : 'KEY_6', '7' : 'KEY_7', '8' : 'KEY_8', '9' : 'KEY_9', '0' : 'KEY_0', '\n' : 'KEY_ENTER', ' ' : 'KEY_SPACE', '-' : 'KEY_MINUS', '=' : 'KEY_EQUAL', '{' : 'KEY_LEFT_BRACE', '}' : 'KEY_RIGHT_BRACE', '\\' : 'KEY_BACKSLASH', ':' : 'KEY_SEMICOLON', '"' : 'KEY_QUOTE', '#' : 'KEY_TILDE', ',' : 'KEY_COMMA', '.' : 'KEY_PERIOD', '/' : 'KEY_SLASH', '*' : 'KEYPAD_ASTERIX', '-' : 'KEYPAD_MINUS', '+' : 'KEYPAD_PLUS', }
if __name__ == "__main__":
    if len(sys.argv) < 2:
        print "Reads input from pipe and creates a program outputing it"
        print "Takes one argument which is timeout in seconds."
        print "echo 'They see me trolling, they hating\\n' | python LoopKeyboardGenerator.py 8"
        exit()
    timeout = "8"
    if len(sys.argv) >= 2:
        timeout = sys.argv[1]
    
    output = "" 
    for row in sys.stdin.readlines():
        chars = list(row)
        for char in chars:
            try:
                if char in string.uppercase:
                    output += "\t\tusb_keyboard_press(%s, KEY_SHIFT);\n" % translate[char.lower()]
                else:
                    output += "\t\tusb_keyboard_press(%s, 0);\n" % translate[char.lower()]
            except KeyError:
                print
                print "Unable to print symbol. Only support subset of ascii"
                print translate
                exit()
    print "Done generating files."
    print
    print "Build project with make and load into teensy"
    f = open("troll.c", "w")
    f.write(insert(timeout, output))
