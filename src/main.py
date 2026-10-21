"""Morse Code.

CMPSC 100: Computational Expression, Lab 6

You are a telegraph operator. Your push button is the telegraph key and the
built-in LED is the sounder. Short presses are dots and long presses are
dashes; a letter is a pattern of them, and a pause of one second ends the
letter. A dictionary is the code book that turns a pattern into a letter, and
the same book turns a message into patterns.

Every message this program prints is yours to word. The automated checks read
only the operator log at the end, and call your functions directly.

Author: TODO
"""

from machine import Pin
from time import sleep

# The code book: each key is a character, and its value is the pattern of dots
# and dashes the operator keys for it
CODE = {
    "A": ".-", "B": "-...", "C": "-.-.", "D": "-..", "E": ".", "F": "..-.",
    "G": "--.", "H": "....", "I": "..", "J": ".---", "K": "-.-", "L": ".-..",
    "M": "--", "N": "-.", "O": "---", "P": ".--.", "Q": "--.-", "R": ".-.",
    "S": "...", "T": "-", "U": "..-", "V": "...-", "W": ".--", "X": "-..-",
    "Y": "-.--", "Z": "--..",
    "0": "-----", "1": ".----", "2": "..---", "3": "...--", "4": "....-",
    "5": ".....", "6": "-....", "7": "--...", "8": "---..", "9": "----.",
}

# TODO 1: add two signals to the book by assigning to new keys: "AR" is
# ".-.-." and "SK" is "...-.-". Assigning to a key that is not in a dictionary
# adds an entry

# TODO 2: build the book backwards. Set `LETTERS` to an empty dictionary, then
# write a for loop over `CODE`. On every trip/iteration, with `character`
# holding the key, assign `character` to `LETTERS` under the pattern
# CODE[character] as the key. Place this after TODO 1, so that AR and SK are
# flipped too

# TODO 3: write a function `to_morse(text)` that returns the patterns for the
# characters of text, separated by single spaces. Start `result` as an empty
# string and loop over text.upper(). Add a character's pattern only if the
# character is in CODE, with a space before it unless `result` is still empty,
# so a space or a ? is skipped. to_morse("sos") returns "... --- ..."

# TODO 4: write a function `from_morse(pattern)` that returns the character
# for a pattern from LETTERS, or "?" when the pattern is not a key of LETTERS.
# Check with `in` before the lookup

# TODO 5: write a function `press_length(button, led)` that returns how many
# tenths of a second the button stays down. Set `length` to 0, and while
# button.value() is 0: led.on(), sleep(0.1), and add 1 to `length`. When the
# loop ends, led.off() and return `length`. PULL_UP makes a press read 0

# TODO 6: write a function `to_symbol(length)` that returns "." when length is
# less than 3 and "-" otherwise

# TODO 7: write a function `read_letter(button, led)` that returns the pattern
# of one letter:
#   - set `pattern` to an empty string
#   - while button.value() is 1: sleep(0.01), so nothing happens until the
#     first press
#   - set `finished` to False, then repeat while not `finished`:
#       - add to_symbol(press_length(button, led)) to `pattern`
#       - set `quiet` to 0, then while button.value() is 1 and `quiet` is less
#         than 10: sleep(0.1) and add 1 to `quiet`
#       - if `quiet` equals 10, nothing was pressed for a second, so set
#         `finished` to True
#   - return `pattern`


def main():
    button = Pin(16, Pin.IN, Pin.PULL_UP)
    led = Pin("LED", Pin.OUT)

    print("=" * 50)
    print("MORSE CODE")
    print("=" * 50)

    # TODO 8: ask the user's name, save it to a variable called `name`. Set
    # `message` to an empty string and `letter` to an empty string. While
    # `letter` is not "SK": save read_letter(button, led) to `pattern`, save
    # from_morse(pattern) to `letter`, print the pattern and the letter, and if
    # `letter` is not "SK", add it to `message`

    # TODO 9: print a blank line, a line of 50 "=", "OPERATOR LOG:" followed by
    # the name, and another line of 50 "=". Then print these lines, each a
    # label followed by its value:
    # Message: `message`
    # Letters: how many characters `message` holds
    # Morse: to_morse(message)


if __name__ == "__main__":
    main()
