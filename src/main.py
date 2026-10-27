"""Morse Code.

CMPSC 100: Computational Expression, Lab 6

You are a telegraph operator. Your push button is the telegraph key and the
built-in LED is the sounder. Short presses are dots and long presses are
dashes; a letter is a pattern of them, and a pause of one second ends the
letter. A dictionary is the code book that turns a pattern into a letter, and
the same book turns a message into patterns. The book is read from the file
morse.csv.

Every message this program prints is yours to word. The automated checks read
only the operator log at the end, and call your functions directly.

Author: TODO
"""

from machine import Pin
from time import sleep

# TODO 1: write a function `read_code_book(filename)` that returns a
# dictionary from each character in the CSV file to its pattern. Set `book` to
# an empty dictionary. Open the file with `with open(filename) as file`, call
# file.readline() once to skip the header line, and loop over the lines of the
# file. For each line, save line.strip().split(",") to `parts` (strip removes
# the newline at the end of the line), then assign parts[1] to `book` under the
# key parts[0]. Return `book` after the with block

# TODO 2: set `CODE` to the dictionary that read_code_book returns for
# "morse.csv". Each key is a character and each value is its pattern of dots
# and dashes, such as "S": "..."

# TODO 3: add two signals to the book by assigning to new keys: "AR" is
# ".-.-." and "SK" is "...-.-". Assigning to a key that is not in a dictionary
# adds an entry

# TODO 4: build the book backwards. Set `LETTERS` to an empty dictionary, then
# write a for loop over `CODE`. On every trip/iteration, with `character`
# holding the key, assign `character` to `LETTERS` under the pattern
# CODE[character] as the key. Place this after TODO 3, so that AR and SK are
# flipped too

# TODO 5: write a function `to_morse(text)` that returns the patterns for the
# characters of text, separated by single spaces. Start `result` as an empty
# string and loop over text.upper(). Add a character's pattern to `result` with
# +=, only if the character is in CODE, and with a space before it unless
# `result` is still empty, so a space or a ? is skipped. to_morse("sos") returns "... --- ..."

# TODO 6: write a function `from_morse(pattern)` that returns the character
# for a pattern from LETTERS, or "?" when the pattern is not a key of LETTERS.
# Check with `in` before the lookup

# TODO 7: write a function `press_length(button, led)` that returns how many
# tenths of a second the button stays down. Set `length` to 0, and while
# button.value() is 0: led.on(), sleep(0.1), and add 1 to `length`. When the
# loop ends, led.off() and return `length`. PULL_UP makes a press read 0

# TODO 8: write a function `to_symbol(length)` that returns "." when length is
# less than 3 and "-" otherwise

# TODO 9: write a function `read_letter(button, led)` that returns the pattern
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

    # TODO 10: ask the user's name, save it to a variable called `name`, and
    # print a line asking the operator to key a message ending with SK

    # TODO 11: count down before the first letter with a for loop over
    # range(3, 0, -1). On every trip/iteration, print the count, then turn the
    # LED on, sleep(0.5), turn it off and sleep(0.5). After the loop, print a
    # line telling the operator to start keying

    # TODO 12: set `message` to an empty string and `letter` to an empty
    # string. While `letter` is not "SK": save read_letter(button, led) to
    # `pattern`, save from_morse(pattern) to `letter`, print the pattern and the
    # letter, and if `letter` is not "SK", add it to `message` with +=

    # TODO 13: print a blank line, a line of 50 "=", "OPERATOR LOG:" followed by
    # the name, and another line of 50 "=". Then print these lines, each a
    # label followed by its value:
    # Message: `message`
    # Letters: how many characters `message` holds
    # Morse: to_morse(message)


if __name__ == "__main__":
    main()
