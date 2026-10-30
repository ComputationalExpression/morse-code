"""Automated checks for Lab 6: Morse Code.

Most checks call your functions directly, with the arguments the README lists,
and compare what they return. The program checks read the operator log at the
end of a run, never the narrative lines, so the story is yours to word. Log
values are matched loosely: any amount of whitespace, any letter case, and the
colon is optional, so `print("Letters:", count)`, `print("Letters: " + str(count))`
and an f-string all read the same.

The button is pressed by a pretend operator with a script of presses, each a
start and an end in seconds. Time passes only when your program calls
time.sleep, so a loop that never sleeps never sees a press end, and the check
stops it. The button is the Pin made with `Pin.IN`, and the other pin is the LED.

When a check fails, the assertion message says what came out wrong and what was
expected. gatorgrade does not show that message itself; it prints the pytest
command to run.
"""

import re
from unittest.mock import patch

import mockro
from machine import Pin

import main as program

# More button reads than this means the program is stuck waiting.
MOST_READS = 20000

DOT = 0.15
DASH = 0.5


class Key:
    """The button and the LED, with a pretend operator at the button.

    `presses` is a list of (start, end) times in seconds, counted from the
    first time the button is read, so a countdown before it shifts nothing. The
    button reads 0 while the clock is inside one of them, and `clock` adds up
    every sleep.
    """

    def __init__(self, presses):
        self.presses = list(presses)
        self.clock = 0.0
        self.reads = 0
        self.first = None
        self.roles = {}
        self.lit = False
        self.on_calls = 0

    def sleep(self, seconds=0, *rest):
        self.clock += seconds

    def who(self, pin):
        if id(pin) not in self.roles:
            self.roles[id(pin)] = self.find(pin)
        return self.roles[id(pin)]

    def find(self, pin):
        for args, _ in mockro.get_recorder().calls("machine.Pin.init"):
            if len(args) >= 4 and args[0] is pin:
                return "button" if args[3] == Pin.IN else "led"
        return None

    def value(self, pin, *rest):
        # mockro passes the Pin twice, then the argument: (pin, pin, x)
        x = rest[-1] if rest and rest[-1] is not pin else None
        part = self.who(pin)
        if part == "button" and x is None:
            return self.read()
        if part == "led" and x is not None:
            self.set(bool(x))
        return 0

    def read(self):
        self.reads += 1
        if self.reads > MOST_READS:
            raise AssertionError(
                f"the button was read {MOST_READS} times with the clock at {self.clock:.1f} seconds, "
                f"so the program was stuck waiting: every loop that watches the button has to sleep"
            )
        if self.first is None:
            self.first = self.clock
        now = self.clock - self.first
        return 0 if any(start <= now < end for start, end in self.presses) else 1

    def on(self, pin, *rest):
        if self.who(pin) == "led":
            self.set(True)

    def off(self, pin, *rest):
        if self.who(pin) == "led":
            self.set(False)

    def set(self, lit):
        self.lit = lit
        if lit:
            self.on_calls += 1


def keyed(letters, start=0.0, between=1.5):
    """Presses for a list of patterns such as ["...", "---"]: `between` seconds of quiet after each."""
    presses = []
    clock = start
    for pattern in letters:
        for symbol in pattern:
            length = DOT if symbol == "." else DASH
            presses.append((clock, clock + length))
            clock += length + 0.3
        clock += between - 0.3
    return presses


def pins():
    return Pin(16, Pin.IN, Pin.PULL_UP), Pin(15, Pin.OUT)


def with_key(key, action):
    """Run `action()` with the button and LED wired to `key` and sleep patched."""
    stubs = [patch("time.sleep", side_effect=key.sleep)]
    if hasattr(program, "sleep"):
        stubs.append(patch.object(program, "sleep", side_effect=key.sleep))
    try:
        with mockro.override(machine_Pin_value=key.value, machine_Pin_on=key.on, machine_Pin_off=key.off):
            for stub in stubs:
                stub.start()
            try:
                return action()
            finally:
                for stub in stubs:
                    stub.stop()
    except AssertionError:
        raise
    except Exception as exc:
        raise AssertionError(f"the program stopped with {type(exc).__name__}: {exc}") from None


def call(key, function, *args_after_pins):
    """Call function(button, led, ...) with fresh pins wired to `key`."""
    mockro.get_recorder().clear()

    def action():
        button, led = pins()
        return function(button, led, *args_after_pins)

    return with_key(key, action)


# The checks pass these books to your functions, so a function has to use its
# parameter, not a dictionary of its own.
CODE = {"S": "...", "O": "---", "A": ".-", "B": "-...", "H": "....", "I": "..", "5": ".....", "SK": "...-.-"}


def test_read_code_book_loads_a_csv_file(tmp_path):
    # Once with a newline at the end of the last line and once without one.
    for ending in ("\n", ""):
        path = tmp_path / "book.csv"
        path.write_text("character,pattern\nQ,--.-\nE,.\nT,-" + ending, encoding="utf-8")
        got = program.read_code_book(str(path))
        want = {"Q": "--.-", "E": ".", "T": "-"}
        assert got == want, (
            f"read_code_book returned {got!r} for a file of Q, E and T, expected {want!r}: skip the header line, "
            f"split each line at the comma, and strip the newline so it is not part of the pattern"
        )


def test_to_morse_looks_up_each_character():
    cases = [("SOS", "... --- ..."), ("sos", "... --- ..."), ("A B", ".- -..."), ("HI5", ".... .. ....."), ("", "")]
    for text, want in cases:
        got = program.to_morse(text, CODE)
        assert got == want, f"to_morse({text!r}, code) returned {got!r}, expected {want!r}: one space between patterns, none at the ends, and characters not in the code book skipped"
    made_up = {"A": "--", "B": "."}
    got = program.to_morse("ab", made_up)
    assert got == "-- .", f"to_morse('ab', {made_up!r}) returned {got!r}, expected '-- .': look each character up in the code parameter"


def test_from_morse_looks_up_a_pattern():
    cases = [(".-", "A"), ("...", "S"), ("...-.-", "SK"), ("-.-.", "?"), (".......", "?"), ("", "?")]
    for pattern, want in cases:
        got = program.from_morse(pattern, CODE)
        assert got == want, f"from_morse({pattern!r}, code) returned {got!r}, expected {want!r}: the character whose pattern matches, or ? when no character has that pattern"
    made_up = {"A": "--", "B": "."}
    for pattern, want in (("--", "A"), (".-", "?")):
        got = program.from_morse(pattern, made_up)
        assert got == want, f"from_morse({pattern!r}, {made_up!r}) returned {got!r}, expected {want!r}: search the code parameter"


def test_press_length_counts_tenths_of_a_second_and_lights_the_led():
    for press, want in (((0.0, 0.25), 3), ((0.0, 0.65), 7)):
        key = Key([press])
        got = call(key, program.press_length)
        assert got == want, (
            f"a press of {press[1]} seconds returned {got} from press_length, expected {want}: "
            f"sleep(0.1) and add 1 for every trip/iteration the button reads 0"
        )
        assert key.on_calls >= 1, "the LED never came on during the press: call led.on() while the button reads 0"
        assert not key.lit, "the LED was left on after the press: call led.off() when the button is released"


def test_to_symbol_chooses_a_dot_or_a_dash():
    for length, want in ((1, "."), (2, "."), (3, "-"), (4, "-"), (9, "-")):
        got = program.to_symbol(length)
        assert got == want, f"to_symbol({length}) returned {got!r}, expected {want!r}: a dot is under 3 tenths of a second"


def test_read_letter_returns_one_pattern_after_a_pause():
    # Two letters in one script: the first call must stop at the pause, and the second must start fresh.
    for letters in ([".-", "-..."], ["...", "-"], ["....-"]):
        key = Key(keyed(letters))
        mockro.get_recorder().clear()

        def action():
            button, led = pins()
            return [program.read_letter(button, led) for _ in letters]

        got = with_key(key, action)
        assert got == letters, f"keying {letters} gave {got} from read_letter, expected {letters}: a second without a press ends a letter"
    check_pauses()


def check_pauses():
    # 0.8 seconds between the dot and the dash is under a second, so one letter.
    key = Key([(0.0, DOT), (DOT + 0.8, DOT + 0.8 + DASH)])
    got = call(key, program.read_letter)
    assert got == ".-", f"a dot, 0.8 seconds, then a dash gave {got!r} from read_letter, expected '.-': only a full second ends the letter"
    # 1.3 seconds is more than a second, so the dash belongs to the next letter.
    key = Key([(0.0, DOT), (DOT + 1.3, DOT + 1.3 + DASH)])
    mockro.get_recorder().clear()

    def action():
        button, led = pins()
        return program.read_letter(button, led), program.read_letter(button, led)

    got = with_key(key, action)
    assert got == (".", "-"), f"a dot, 1.3 seconds, then a dash gave {got} from two calls, expected ('.', '-')"


def log_value(out, label):
    """Return the value printed after `label` in the operator log, normalized."""
    starts = [line.start() for line in re.finditer(r"^\s*OPERATOR\s+LOG", out, re.IGNORECASE | re.MULTILINE)]
    if not starts:
        return None
    words = r"\s+".join(re.escape(word) for word in label.split())
    match = re.search(rf"^[ \t]*{words}[ \t]*:?[ \t]*([^\n]*)", out[starts[-1]:], re.IGNORECASE | re.MULTILINE)
    if match is None:
        return None
    return " ".join(match.group(1).split()).upper()


def run_program(capsys, letters, name="JJ"):
    key = Key(keyed(letters))
    mockro.get_recorder().clear()
    with patch("builtins.input", side_effect=lambda prompt="": name):
        try:
            with_key(key, program.main)
        except AssertionError as error:
            raise AssertionError(
                f"{error}. If the message never ended at SK, check that main adds SK to the code book "
                f"and keeps reading letters until from_morse returns SK"
            ) from None
    out, err = capsys.readouterr()
    assert err == "", "the program wrote to the error stream:\n" + err
    return out


def expect(out, label, want, context):
    if log_value(out, "OPERATOR LOG") is None:
        raise AssertionError(f'no "OPERATOR LOG" line was printed ({context})')
    got = log_value(out, label)
    if got is None:
        raise AssertionError(f'no "{label}" line was printed after OPERATOR LOG ({context})')
    assert got == want.upper(), f'the "{label}" line said {got}, expected {want} ({context})'


def test_the_program_decodes_a_message_until_sk(capsys):
    sos = ["...", "---", "...", "...-.-"]
    out = run_program(capsys, sos)
    context = f"keyed {sos}"
    expect(out, "OPERATOR LOG", "JJ", context)
    expect(out, "Message", "SOS", context)
    expect(out, "Letters", "3", context)
    expect(out, "Morse", "... --- ...", context)
    # H, I, a pattern the book does not have, then SK: the unknown one is a ?
    unknown = ["....", "..", ".......", "...-.-"]
    out = run_program(capsys, unknown, name="Sam")
    context = f"keyed {unknown}"
    expect(out, "OPERATOR LOG", "Sam", context)
    expect(out, "Message", "HI?", context)
    expect(out, "Letters", "3", context)
    expect(out, "Morse", ".... ..", context)
