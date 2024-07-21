from __future__ import annotations

import base64
import re
import typing
from typing import List

if typing.TYPE_CHECKING:
    from .terminal import Terminal


class ANSI:
    BEL = "\x07"
    BS = "\x08"
    HT = "\x09"
    LF = "\x0a"
    FF = "\x0c"
    CR = "\x0d"
    ESC = "\x1b"


class OutputParser:
    def __init__(self, terminal: Terminal):
        self.terminal = terminal
        self.buf = ""
        self.escape_sequence = ""
        self.in_escape_sequence = False

    def parse(self, buf: str) -> List[str]:
        self.buf += buf
        return self.parse_ansi()

    def parse_ansi(self) -> List[str]:
        output = []
        i = 0
        while i < len(self.buf):
            char = self.buf[i]

            if self.in_escape_sequence:
                self.escape_sequence += char
                if self.is_escape_sequence_complete(char):
                    self.handle_escape_sequence(self.escape_sequence)
                    self.in_escape_sequence = False
                    self.escape_sequence = ""
                i += 1
                continue

            match char:
                case ANSI.BEL:
                    self.terminal._bell()
                case ANSI.BS:
                    self.terminal._backspace()
                case ANSI.HT:
                    self.terminal._tab()
                case ANSI.LF:
                    self.terminal._newline()
                case ANSI.FF:
                    self.terminal._formfeed()
                case ANSI.CR:
                    self.terminal._carriage_return()
                case ANSI.ESC:
                    self.in_escape_sequence = True
                    self.escape_sequence = char
                case _:
                    output.append(char)

            i += 1

        self.buf = ""
        return output

    def is_escape_sequence_complete(self, char: str) -> bool:
        if self.escape_sequence.startswith(ANSI.ESC + "["):  # CSI
            return char.isalpha()
        elif self.escape_sequence.startswith(ANSI.ESC + "]"):  # OSC
            return char == ANSI.BEL or (
                len(self.escape_sequence) >= 2
                and self.escape_sequence[-2:] == ANSI.ESC + "\\"
            )
        elif self.escape_sequence.startswith(ANSI.ESC + "P"):  # DCS
            return (
                len(self.escape_sequence) >= 2
                and self.escape_sequence[-2:] == ANSI.ESC + "\\"
            )
        else:
            return len(self.escape_sequence) == 2  # Simple escape sequences

    def handle_escape_sequence(self, sequence: str):
        if sequence.startswith(ANSI.ESC + "["):  # CSI
            self.handle_csi_sequence(sequence)
        elif sequence.startswith(ANSI.ESC + "]"):  # OSC
            self.handle_osc_sequence(sequence)
        elif sequence.startswith(ANSI.ESC + "P"):  # DCS
            self.handle_dcs_sequence(sequence)
        else:
            self.handle_simple_escape_sequence(sequence)

    def handle_csi_sequence(self, sequence: str):
        match = re.match(r"\x1b\[(\d*;?)*([A-Za-z])", sequence)
        if match:
            params = match.group(1).split(";") if match.group(1) else []
            command = match.group(2)

            match command:
                case "@":  # Insert Characters
                    self.terminal._insert_characters(params)
                case "A":  # Cursor Up
                    self.terminal._cursor_up(params)
                case "B":  # Cursor Down
                    self.terminal._cursor_down(params)
                case "C":  # Cursor Forward
                    self.terminal._cursor_forward(params)
                case "D":  # Cursor Backward
                    self.terminal._cursor_backward(params)
                case "E":  # Cursor Next Line
                    self.terminal._cursor_next_line(params)
                case "F":  # Cursor Previous Line
                    self.terminal._cursor_previous_line(params)
                case "G":  # Cursor Horizontal Absolute
                    self.terminal._cursor_horizontal_absolute(params)
                case "H" | "f":  # Cursor Position
                    self.terminal._cursor_position(params)
                case "I":  # Cursor Forward Tabulation
                    self.terminal._cursor_forward_tabulation(params)
                case "J":  # Erase in Display
                    self.terminal._erase_in_display(params)
                case "K":  # Erase in Line
                    self.terminal._erase_in_line(params)
                case "L":  # Insert Lines
                    self.terminal._insert_lines(params)
                case "M":  # Delete Lines
                    self.terminal._delete_lines(params)
                case "P":  # Delete Characters
                    self.terminal._delete_characters(params)
                case "S":  # Scroll Up
                    self.terminal._scroll_up(params)
                case "T":  # Scroll Down
                    self.terminal._scroll_down(params)
                case "X":  # Erase Characters
                    self.terminal._erase_characters(params)
                case "Z":  # Cursor Backward Tabulation
                    self.terminal._cursor_backward_tabulation(params)
                case "`":  # Character Position Absolute
                    self.terminal._character_position_absolute(params)
                case "a":  # Character Position Relative
                    self.terminal._character_position_relative(params)
                case "b":  # Repeat Preceding Character
                    self.terminal._repeat_preceding_character(params)
                case "c":  # Send Device Attributes
                    self.terminal._send_device_attributes(params)
                case "d":  # Line Position Absolute
                    self.terminal._line_position_absolute(params)
                case "e":  # Line Position Relative
                    self.terminal._line_position_relative(params)
                case "g":  # Tab Clear
                    self.terminal._tab_clear(params)
                case "h":  # Set Mode
                    self.terminal._set_mode(params)
                case "l":  # Reset Mode
                    self.terminal._reset_mode(params)
                case "m":  # Select Graphic Rendition (SGR)
                    self.handle_sgr(params)
                case "n":  # Device Status Report
                    self.terminal._device_status_report(params)
                case "p":  # Set Keyboard String / Set Conformance Level
                    self.terminal._set_keyboard_string(params)
                case "q":  # Set Cursor Style (DECSCUSR)
                    self.terminal._set_cursor_style(params)
                case "r":  # Set Scrolling Region
                    self.terminal._set_scrolling_region(params)
                case "s":  # Save Cursor Position
                    self.terminal._save_cursor_position()
                case "t":  # Window Manipulation
                    self.terminal._window_manipulation(params)
                case "u":  # Restore Cursor Position
                    self.terminal._restore_cursor_position()
                case "x":  # Request Terminal Parameters
                    self.terminal._request_terminal_parameters(params)
                case "{":  # Select Locator Events
                    self.terminal._select_locator_events(params)
                case "|":  # Request Locator Position
                    self.terminal._request_locator_position(params)
                case _:
                    print(f"Unhandled CSI sequence: {sequence}")

    def handle_osc_sequence(self, sequence: str):
        # Handle Operating System Command sequences
        # OSC sequences start with ESC ] and end with BEL (^G) or ST (ESC \)
        if sequence.endswith("\x07"):
            osc_content = sequence[2:-1]  # Remove ESC ] at start and BEL at end
        elif sequence.endswith("\x1b\\"):
            osc_content = sequence[2:-2]  # Remove ESC ] at start and ESC \ at end
        else:
            print(f"Malformed OSC sequence: {sequence}")
            return

        parts = osc_content.split(";")
        osc_code = parts[0]

        match osc_code:
            case "0" | "1" | "2":
                # Set window title and icon name
                title = ";".join(parts[1:])
                self.terminal._set_window_title(title)
            case "3":
                # Set X property on top-level window
                prop, value = parts[1], ";".join(parts[2:])
                self.terminal._set_x_property(prop, value)
            case "4":
                # Change/query color palette
                self.handle_color_palette(parts[1:])
            case "5":
                # Change/query special color number
                self.handle_special_color(parts[1:])
            case "6":
                # Enable/disable special color number
                self.terminal._set_color_mode(parts[1])
            case "7":
                # Query/set current directory
                self.terminal._set_current_directory(";".join(parts[1:]))
            case "8":
                # Create/update hyperlink
                self.handle_hyperlink(parts[1:])
            case "9":
                # iTerm2 Growl notification
                self.terminal._send_notification(";".join(parts[1:]))
            case "10":
                # Set foreground color (deprecated)
                self.terminal._set_foreground_color(parts[1])
            case "11":
                # Set background color (deprecated)
                self.terminal._set_background_color(parts[1])
            case "12":
                # Set cursor color
                self.terminal._set_cursor_color(parts[1])
            case "13":
                # Set mouse foreground color
                self.terminal._set_mouse_fore_color(parts[1])
            case "14":
                # Set mouse background color
                self.terminal._set_mouse_back_color(parts[1])
            case "15":
                # Set Tektronix foreground color
                self.terminal._set_tek_fore_color(parts[1])
            case "16":
                # Set Tektronix background color
                self.terminal._set_tek_back_color(parts[1])
            case "17":
                # Set highlight background color
                self.terminal._set_highlight_bg_color(parts[1])
            case "18":
                # Set Tektronix cursor color
                self.terminal._set_tek_cursor_color(parts[1])
            case "19":
                # Set highlight foreground color
                self.terminal._set_highlight_fg_color(parts[1])
            case "46":
                # Change log file
                self.terminal._set_log_file(parts[1])
            case "50":
                # Set font
                self.terminal._set_font(";".join(parts[1:]))
            case "51":
                # Set emoji font
                self.terminal._set_emoji_font(";".join(parts[1:]))
            case "52":
                # Manipulate selection data
                self.handle_selection_data(parts[1:])
            case "104":
                # Reset color palette
                self.terminal._reset_color_palette()
            case "105":
                # Reset special color
                self.terminal._reset_special_color(parts[1])
            case "110":
                # Reset foreground color
                self.terminal._reset_foreground_color()
            case "111":
                # Reset background color
                self.terminal._reset_background_color()
            case "112":
                # Reset cursor color
                self.terminal._reset_cursor_color()
            case "113":
                # Reset mouse foreground color
                self.terminal._reset_mouse_fore_color()
            case "114":
                # Reset mouse background color
                self.terminal._reset_mouse_back_color()
            case "115":
                # Reset Tektronix foreground color
                self.terminal._reset_tek_fore_color()
            case "116":
                # Reset Tektronix background color
                self.terminal._reset_tek_back_color()
            case "117":
                # Reset highlight color
                self.terminal._reset_highlight_bg_color()
            case "118":
                # Reset Tektronix cursor color
                self.terminal._reset_tek_cursor_color()
            case "119":
                # Reset highlight foreground color
                self.terminal._reset_highlight_fg_color()
            case _:
                print(f"Unknown OSC sequence: {sequence}")

    def handle_color_palette(self, params: List[str]):
        # Handle color palette changes
        if len(params) == 1:
            # Query color
            color_index = int(params[0])
            self.terminal._query_color(color_index)
        elif len(params) == 2:
            # Set color
            color_index = int(params[0])
            color_spec = params[1]
            self.terminal._set_color(color_index, color_spec)

    def handle_special_color(self, params: List[str]):
        # Handle special color changes
        if len(params) == 1:
            # Query special color
            color_name = params[0]
            self.terminal._query_special_color(color_name)
        elif len(params) == 2:
            # Set special color
            color_name = params[0]
            color_spec = params[1]
            self.terminal._set_special_color(color_name, color_spec)

    def handle_hyperlink(self, params: List[str]):
        # Handle hyperlink creation/update
        if len(params) >= 2:
            params_dict = dict(
                param.split("=") for param in params[0].split(":") if "=" in param
            )
            uri = params[1]
            self.terminal._set_hyperlink(params_dict, uri)

    def handle_selection_data(self, params: List[str]):
        # Handle selection data manipulation
        if len(params) == 2:
            clipboard = params[0]
            data = params[1]
            if data.startswith("?"):
                self.terminal._query_selection_data(clipboard)
            else:
                decoded_data = self.base64_decode(data)
                self.terminal._set_selection_data(clipboard, decoded_data)

    def base64_decode(self, data: str) -> str:
        return base64.b64decode(data).decode("utf-8")

    def handle_dcs_sequence(self, sequence: str):
        # Handle Device Control String sequences
        # DCS sequences start with ESC P and end with ST (String Terminator, which is ESC \)
        dcs_content = sequence[2:-2]  # Remove ESC P at start and ESC \ at end

        if dcs_content.startswith("$q"):
            # DECRQSS (Request Status String)
            self.handle_decrqss(dcs_content[2:])
        elif dcs_content.startswith("+q"):
            # Request Terminfo String
            self.handle_request_terminfo(dcs_content[2:])
        elif dcs_content.startswith("1$r"):
            # DECCIR (Cursor Information Report)
            self.handle_deccir(dcs_content[3:])
        elif dcs_content.startswith("$t"):
            # DECRSPS (Restore Presentation State)
            self.handle_decrsps(dcs_content[2:])
        elif dcs_content.startswith(">|"):
            # DECREGIS (ReGIS graphics)
            self.handle_regis(dcs_content[2:])
        elif dcs_content.startswith("="):
            # DECPFK (Program Function Key)
            self.handle_decpfk(dcs_content[1:])
        elif dcs_content.startswith("+p"):
            # DECPKA (Program Key Action)
            self.handle_decpka(dcs_content[2:])
        elif dcs_content.startswith("$s"):
            # DECSCA (Select Character Attributes)
            self.handle_decsca(dcs_content[2:])
        elif re.match(r"\d+\*\|", dcs_content):
            # DECUDK (User Defined Keys)
            self.handle_decudk(dcs_content)
        else:
            print(f"Unknown DCS sequence: {sequence}")

    def handle_decrqss(self, param: str):
        # DECRQSS - Request Status String
        # The terminal should respond with a status report
        if param == "m":
            self.terminal._report_sgr_attributes()
        elif param == "r":
            self.terminal._report_margins()
        # Add more DECRQSS parameters as needed

    def handle_request_terminfo(self, param: str):
        # Request Terminfo String
        # The terminal should respond with the requested terminfo capability
        self.terminal._report_terminfo(param)

    def handle_deccir(self, param: str):
        # DECCIR - Cursor Information Report
        # The terminal should report cursor position and page size
        self.terminal._report_cursor_info()

    def handle_decrsps(self, param: str):
        # DECRSPS - Restore Presentation State
        # Restores a previously saved presentation state
        self.terminal._restore_presentation_state(param)

    def handle_regis(self, param: str):
        # DECREGIS - ReGIS graphics
        # Handles ReGIS (Remote Graphic Instruction Set) commands
        self.terminal._process_regis(param)

    def handle_decpfk(self, param: str):
        # DECPFK - Program Function Key
        # Programs a function key
        key, string = param.split("/")
        self.terminal._program_function_key(key, string)

    def handle_decpka(self, param: str):
        # DECPKA - Program Key Action
        # Programs a key to perform a specific action
        key, action = param.split("/")
        self.terminal._program_key_action(key, action)

    def handle_decsca(self, param: str):
        # DECSCA - Select Character Attributes
        # Sets the character protection attribute
        self.terminal._set_character_attributes(param)

    def handle_decudk(self, param: str):
        # DECUDK - User Defined Keys
        # Defines a string to be returned when a particular key is pressed
        match = re.match(r"(\d+)\*\|(.*)", param)
        if match:
            clear_flag = match.group(1)
            definitions = match.group(2).split(";")
            self.terminal._define_user_keys(clear_flag, definitions)

    def handle_simple_escape_sequence(self, sequence: str):
        # Handle simple two-character escape sequences
        match sequence:
            case "\x1bD":  # Index (IND)
                # Moves the cursor down one line, scrolling if necessary
                self.terminal._index()
            case "\x1bM":  # Reverse Index (RI)
                # Moves the cursor up one line, scrolling if necessary
                self.terminal._reverse_index()
            case "\x1bE":  # Next Line (NEL)
                # Moves the cursor to the beginning of the next line, scrolling if necessary
                self.terminal._next_line()
            case "\x1b7":  # Save Cursor (DECSC)
                # Saves the current cursor position, character attribute, character set, and origin mode selection
                self.terminal._save_cursor()
            case "\x1b8":  # Restore Cursor (DECRC)
                # Restores the previously saved cursor position, character attribute, character set, and origin mode selection
                self.terminal._restore_cursor()
            case "\x1bH":  # Horizontal Tab Set (HTS)
                # Sets a tab stop at the current cursor position
                self.terminal._set_tab_stop()
            case "\x1bN":  # Single Shift Select of G2 Character Set (SS2)
                # Temporarily shifts to G2 character set for the next character
                self.terminal._shift_to_g2()
            case "\x1bO":  # Single Shift Select of G3 Character Set (SS3)
                # Temporarily shifts to G3 character set for the next character
                self.terminal._shift_to_g3()
            case "\x1b=":  # Application Keypad (DECKPAM)
                # Switches the keypad to application mode
                self.terminal._set_keypad_application_mode()
            case "\x1b>":  # Normal Keypad (DECKPNM)
                # Switches the keypad to numeric mode
                self.terminal._set_keypad_numeric_mode()
            case "\x1bc":  # Full Reset (RIS)
                # Resets the terminal to its initial state
                self.terminal._full_reset()
            case "\x1b#3":  # Double-Height Letters, Top Half (DECDHL)
                # Selects top half of double-height characters
                self.terminal._set_double_height_top()
            case "\x1b#4":  # Double-Height Letters, Bottom Half (DECDHL)
                # Selects bottom half of double-height characters
                self.terminal._set_double_height_bottom()
            case "\x1b#5":  # Single-Width Line (DECSWL)
                # Sets normal single-width characters
                self.terminal._set_single_width()
            case "\x1b#6":  # Double-Width Line (DECDWL)
                # Sets double-width characters
                self.terminal._set_double_width()
            case "\x1b#8":  # Screen Alignment Pattern (DECALN)
                # Fills the screen with 'E' characters for screen focus and alignment
                self.terminal._screen_alignment_test()
            case _:
                # Unknown escape sequence, you might want to log this or handle it in some way
                print(f"Unknown escape sequence: {sequence}")

    def handle_sgr(self, params: List[str]):
        # Handle Select Graphic Rendition

        for param in params:
            match param:
                case "0":  # Reset / Normal
                    self.terminal._reset_attributes()
                case "1":  # Bold or increased intensity
                    self.terminal._set_bold()
                case "2":  # Faint, decreased intensity or second colour
                    self.terminal._set_faint()
                case "3":  # Italic
                    self.terminal._set_italic()
                case "4":  # Underline
                    self.terminal._set_underline()
                case "5":  # Slow Blink
                    self.terminal._set_slow_blink()
                case "6":  # Rapid Blink
                    self.terminal._set_rapid_blink()
                case "7":  # Reverse video
                    self.terminal._set_reverse_video()
                case "8":  # Conceal
                    self.terminal._set_conceal()
                case "9":  # Crossed-out
                    self.terminal._set_crossed_out()
                case "10":  # Primary (default) font
                    self.terminal._set_primary_font()
                case (
                    "11" | "12" | "13" | "14" | "15" | "16" | "17" | "18" | "19"
                ):  # Alternative font
                    self.terminal._set_alternative_font(int(param) - 10)
                case "20":  # Fraktur (rarely used)
                    self.terminal._set_fraktur()
                case "21":  # Doubly underlined or Bold off
                    self.terminal._set_doubly_underlined()
                case "22":  # Normal colour or intensity
                    self.terminal._reset_intensity()
                case "23":  # Not italic, not Fraktur
                    self.terminal._reset_italic_fraktur()
                case "24":  # Underline off
                    self.terminal._reset_underline()
                case "25":  # Blink off
                    self.terminal._reset_blink()
                case "27":  # Inverse off
                    self.terminal._reset_inverse()
                case "28":  # Reveal (conceal off)
                    self.terminal._reset_conceal()
                case "29":  # Not crossed out
                    self.terminal._reset_crossed_out()
                case (
                    "30" | "31" | "32" | "33" | "34" | "35" | "36" | "37"
                ):  # Set foreground color
                    self.terminal._set_foreground_color(int(param) - 30)
                case "38":  # Set foreground color (next arguments are 5;n or 2;r;g;b)
                    self.terminal._set_foreground_color_extended(
                        params[params.index("38") + 1 :]
                    )
                    break
                case "39":  # Default foreground color
                    self.terminal._reset_foreground_color()
                case (
                    "40" | "41" | "42" | "43" | "44" | "45" | "46" | "47"
                ):  # Set background color
                    self.terminal._set_background_color(int(param) - 40)
                case "48":  # Set background color (next arguments are 5;n or 2;r;g;b)
                    self.terminal._set_background_color_extended(
                        params[params.index("48") + 1 :]
                    )
                    break
                case "49":  # Default background color
                    self.terminal._reset_background_color()
                case (
                    "90" | "91" | "92" | "93" | "94" | "95" | "96" | "97"
                ):  # Set bright foreground color
                    self.terminal._set_bright_foreground_color(int(param) - 90)
                case (
                    "100" | "101" | "102" | "103" | "104" | "105" | "106" | "107"
                ):  # Set bright background color
                    self.terminal._set_bright_background_color(int(param) - 100)
                case _:
                    if param.startswith("38;2;") or param.startswith(
                        "48;2;"
                    ):  # 24-bit color
                        parts = param.split(";")
                        if len(parts) == 5:
                            if parts[0] == "38":
                                self.terminal._set_foreground_color_rgb(
                                    int(parts[2]), int(parts[3]), int(parts[4])
                                )
                            elif parts[0] == "48":
                                self.terminal._set_background_color_rgb(
                                    int(parts[2]), int(parts[3]), int(parts[4])
                                )
                    elif param.startswith("38;5;") or param.startswith(
                        "48;5;"
                    ):  # 256 color
                        parts = param.split(";")
                        if len(parts) == 3:
                            if parts[0] == "38":
                                self.terminal._set_foreground_color_256(int(parts[2]))
                            elif parts[0] == "48":
                                self.terminal._set_background_color_256(int(parts[2]))
                    else:
                        print(f"Unhandled SGR parameter: {param}")
