"""Morse Code.

CMPSC 100: Computational Expression, Lab 6

You are a telegraph operator. Your push button is the telegraph key and the
built-in LED is the sounder. Short presses are dots and long presses are
dashes; a letter is a pattern of them, and a pause of one second ends the
letter. A dictionary is the code book that turns a pattern into a letter, and
the same book turns a message into patterns. The book is read from the file
morse.csv.

Every message this program prints is yours to word, and every variable name
is yours to choose. The function names and their parameters stay as the README
lists them, because the automated checks call each function directly. The
checks also read the operator log at the end.

Author: TODO
"""

from machine import Pin
from time import sleep

# read_code_book is started for you with its docstring: the line in triple
# quotes right under def, which says what the function returns. Write a
# docstring like it for every function you add.


def read_code_book(filename):
    """Return a dictionary from each character in the CSV file to its pattern."""
    # TODO 1: build the dictionary from the file, one entry per line:
    #   - start with an empty dictionary (`book`, for example)
    #   - open the file with `with open(filename) as file`, and call
    #     file.readline() once to skip the header line
    #   - loop over the lines of the file. line.strip() removes the newline at
    #     the end of a line, and .split(",") breaks what is left into a list:
    #     the character at position 0 and its pattern at position 1
    #   - assign the pattern to the dictionary, with the character as the key
    #   - return the dictionary after the with block


# TODO 2: below the function and outside it, store the dictionary that
# read_code_book returns for "morse.csv" in a variable (`CODE`, for example).
# Each key is a character and each value is its pattern, such as "S": "..."

# TODO 3: add two signals to the code book by assigning to new keys: "AR" is
# ".-.-." and "SK" is "...-.-"

# TODO 4: build the code book backwards, so that each pattern is a key and its
# value is the character:
#   - start a second empty dictionary (`LETTERS`, for example)
#   - write a for loop over the code book. On every trip/iteration the loop
#     variable holds one key, a character
#   - look up that character's pattern in the code book, and assign the
#     character to the second dictionary with the pattern as the key
#   - keep this below TODO 3, so that AR and SK are flipped too

# TODO 5: write a function `to_morse(text)` that returns the patterns for the
# characters of text, separated by single spaces:
#   - start the result as an empty string
#   - loop over text.upper(), one character on each trip/iteration
#   - use `in` to check whether the character is a key of the code book, and
#     skip it if it is not (a space, for example)
#   - add its pattern to the result with +=, with a space before it unless the
#     result is still empty
# to_morse("sos") returns "... --- ..."

# TODO 6: write a function `from_morse(pattern)` that returns the character
# for a pattern from the backwards book, or "?" when the pattern is not one of
# its keys. Check with `in` before the lookup

# TODO 7: write a function `press_length(button, led)` that returns how many
# tenths of a second the button stays down. Count the trips/iterations of a
# while loop that runs while the button is pressed and sleeps 0.1 seconds on
# each one. The LED is on during the press and off after it. PULL_UP makes a
# press read 0

# TODO 8: write a function `to_symbol(length)` that returns "." when length is
# less than 3 and "-" otherwise

# TODO 9: write a function `read_letter(button, led)` that returns the pattern
# of one letter:
#   - start the pattern as an empty string, and wait until the button is first
#     pressed, sleeping 0.01 seconds on each trip/iteration of the wait
#   - repeat until the letter is finished (a True or False variable can
#     remember that):
#       - add the symbol for the next press to the pattern, using
#         press_length and to_symbol
#       - count the quiet tenths of a second after the press: start a counter
#         at 0, and while the button reads 1 and the counter is less than 10,
#         sleep(0.1) and add 1 to the counter. A press or a full second stops
#         this loop
#       - if the counter reached 10, nothing was pressed for a second, so the
#         letter is finished
#   - return the pattern


def main():
    button = Pin(16, Pin.IN, Pin.PULL_UP)
    led = Pin("LED", Pin.OUT)

    print("=" * 50)
    print("MORSE CODE")
    print("=" * 50)

    # TODO 10: ask the operator's name, and tell them to key a message that
    # ends with SK

    # TODO 11: count down before the first letter with a for loop over
    # range(3, 0, -1). On every trip/iteration, print the count, then turn the
    # LED on, sleep(0.5), turn it off and sleep(0.5). After the loop, tell the
    # operator to start keying

    # TODO 12: read letters with read_letter and decode each one with
    # from_morse until the letter is SK. Print each pattern with its letter,
    # and add every letter except SK to the message with +=

    # TODO 13: print the operator log shown in the README: the OPERATOR LOG
    # line with the name between two lines of "=", then the Message, Letters
    # and Morse lines. Morse is to_morse of the message


if __name__ == "__main__":
    main()
