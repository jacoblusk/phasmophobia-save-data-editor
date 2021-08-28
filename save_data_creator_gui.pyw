from typing import *

import argparse
import json

import ctypes
from ctypes.wintypes import *

MAX_PATH = 260
CW_USEDEFAULT = 0x80000000

INVALID_HANDLE_VALUE = ctypes.c_void_p(-1)
INFINITE = ctypes.c_uint(-1)

CLASS_NAME = b"SaveDataCreator"
WINDOW_NAME = b"Save Data Creator"

LONG_PTR = LPARAM
HCURSOR = HANDLE
LRESULT = ctypes.c_long
SIZE_T = ctypes.c_size_t

TEXT_BOX = 501
SAVE_BUTTON = 502
OPEN_BUTTON = 503

WNDPROC = ctypes.WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
WNDENUMPROC = ctypes.WINFUNCTYPE(BOOL, HWND, LPARAM)

def MAKELONG(wLow, wHigh):
    return ctypes.c_long(wLow | wHigh << 16)

def MAKELPARAM(l, h):
    return LPARAM(MAKELONG(l, h).value)

def LOWORD(l):
    return WORD(l & 0xFFFF)

def HIWORD(l):
    return WORD((l >> 16) & 0xFFFF)

class OPENFILENAMEA(ctypes.Structure):
    _fields_ = [
        ('lStructSize', DWORD),
        ('hwndOwner', HWND),
        ('hInstance', HINSTANCE),
        ('lpstrFilter', LPCSTR),
        ('lpstrCustomFilter', LPSTR),
        ('nMaxCustFilter', DWORD),
        ('nFilterIndex', DWORD),
        ('lpstrFile', LPSTR),
        ('nMaxFile', DWORD),
        ('lpstrFileTitle', LPSTR),
        ('nMaxFileTitle', DWORD),
        ('lpstrInitialDir', LPCSTR),
        ('lpstrTitle', LPCSTR),
        ('Flags', DWORD),
        ('nFileOffset', WORD),
        ('nFileExtension', WORD),
        ('lpstrDefExt', LPCSTR),
        ('lCustData', LPARAM),
        ('lpfnHook', ctypes.c_void_p),
        ('lpTemplateName', LPCSTR),
        ('pvReserved', ctypes.c_void_p),
        ('dwReserved', DWORD),
        ('FlagsEx', DWORD)
    ]

LPOPENFILENAMEA = ctypes.POINTER(OPENFILENAMEA)

class RECT(ctypes.Structure):
    _fields_ = [
        ('left', LONG),
        ('top', LONG),
        ('right', LONG),
        ('bottom', LONG),
    ]

LPRECT = ctypes.POINTER(RECT)


class ICONINFO(ctypes.Structure):
    _fields_ = [
        ('fIcon', BOOL),
        ('xHotspot', DWORD),
        ('yHotspot', DWORD),
        ('hbmMask', HBITMAP),
        ('hbmColor', HBITMAP),
    ]

PICONINFO = ctypes.POINTER(ICONINFO)


class LOGFONTA(ctypes.Structure):
    LF_FACESIZE = 32
    _fields_ = [
        ('lfHeight', LONG),
        ('lfWidth', LONG),
        ('lfEscapement', LONG),
        ('lfOrientation', LONG),
        ('lfWeight', LONG),
        ('lfItalic', BYTE),
        ('lfUnderline', BYTE),
        ('lfStrikeOut', BYTE),
        ('lfCharSet', BYTE),
        ('lfOutPrecision', BYTE),
        ('lfClipPrecision', BYTE),
        ('lfQuality', BYTE),
        ('lfPitchAndFamily', BYTE),
        ('lfFaceName', CHAR * LF_FACESIZE)
    ]

LPLOGFONTA = ctypes.POINTER(LOGFONTA)


class NONCLIENTMETRICSA(ctypes.Structure):
    _fields_ = [
        ('cbSize', UINT),
        ('iBorderWidth', ctypes.c_int),
        ('iScrollWidth', ctypes.c_int),
        ('iScrollHeight', ctypes.c_int),
        ('iCaptionWidth', ctypes.c_int),
        ('iCaptionHeight', ctypes.c_int),
        ('lfCaptionFont', LOGFONTA),
        ('iSmCaptionWidth', ctypes.c_int),
        ('iSmCaptionHeight', ctypes.c_int),
        ('lfSmCaptionFont', LOGFONTA),
        ('iMenuWidth', ctypes.c_int),
        ('iMenuHeight', ctypes.c_int),
        ('lfMenuFont', LOGFONTA),
        ('lfStatusFont', LOGFONTA),
        ('lfMessageFont', LOGFONTA),
        ('iPaddedBorderWidth', ctypes.c_int)
    ]

LPNONCLIENTMETRICSA = ctypes.POINTER(NONCLIENTMETRICSA)


class POINT(ctypes.Structure):
    _fields_ = [
        ('x', LONG),
        ('y', LONG)
    ]


class MSG(ctypes.Structure):
    _fields_ = [
        ('hwnd', HWND),
        ('message', UINT),
        ('wParam', WPARAM),
        ('lParam', LPARAM),
        ('time', DWORD),
        ('pt', POINT),
        ('lPrivate', DWORD)
    ]

LPMSG = ctypes.POINTER(MSG)


class WNDCLASSA(ctypes.Structure):
    _fields_ = [
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', ctypes.c_int),
        ('cbWndExtra', ctypes.c_int),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', LPCSTR),
        ('lpszClassName', LPCSTR)
    ]

LPWNDCLASSA = ctypes.POINTER(WNDCLASSA)

def LPVOID_errcheck(result, func, args):
    if not result:
        raise ctypes.WinError()
    return result

def Win32API_errcheck(result, func, args):
    if not result:
        raise ctypes.WinError()

GetDlgItem = ctypes.windll.user32.GetDlgItem
GetDlgItem.argtypes = [HWND, ctypes.c_int]
GetDlgItem.restype = HWND
GetDlgItem.errcheck = LPVOID_errcheck

RegisterClassA = ctypes.windll.user32.RegisterClassA
RegisterClassA.argtypes = [LPWNDCLASSA]
RegisterClassA.restype = ATOM
RegisterClassA.errcheck = LPVOID_errcheck

DefWindowProcA = ctypes.windll.user32.DefWindowProcA
DefWindowProcA.argtypes = [HWND, UINT, WPARAM, LPARAM]
DefWindowProcA.restype = LRESULT

CreateWindowExA = ctypes.windll.user32.CreateWindowExA
CreateWindowExA.argtypes = [DWORD, LPCSTR, LPCSTR, DWORD, ctypes.c_int,
                            ctypes.c_int, ctypes.c_int, ctypes.c_int,
                            HWND, HMENU, HINSTANCE, LPVOID]
CreateWindowExA.restype = HWND
CreateWindowExA.errcheck = LPVOID_errcheck

ShowWindow = ctypes.windll.user32.ShowWindow
ShowWindow.argtypes = [HWND, ctypes.c_int]
ShowWindow.restype = BOOL

GetMessageA = ctypes.windll.user32.GetMessageA
GetMessageA.argtypes = [LPMSG, HWND, UINT, UINT]
GetMessageA.restype = BOOL

TranslateMessage = ctypes.windll.user32.TranslateMessage
TranslateMessage.argtypes = [LPMSG]
TranslateMessage.restype = BOOL

DispatchMessageA = ctypes.windll.user32.DispatchMessageA
DispatchMessageA.argtypes = [LPMSG]
DispatchMessageA.restype = BOOL

PostQuitMessage = ctypes.windll.user32.PostQuitMessage
PostQuitMessage.argtypes = [ctypes.c_int]
PostQuitMessage.restype = None

DestroyWindow = ctypes.windll.user32.DestroyWindow
DestroyWindow.argtypes = [HWND]
DestroyWindow.restype = BOOL
DestroyWindow.errcheck = Win32API_errcheck

SetWindowTextA = ctypes.windll.user32.SetWindowTextA
SetWindowTextA.argtypes = [HWND, LPCSTR]
SetWindowTextA.restype = BOOL
SetWindowTextA.errcheck = Win32API_errcheck

try:
    GetWindowLongPtrA = ctypes.windll.user32.GetWindowLongPtrA
except:
    GetWindowLongPtrA = ctypes.windll.user32.GetWindowLongA
GetWindowLongPtrA.argtypes = [HWND, ctypes.c_int]
GetWindowLongPtrA.restype = LONG_PTR
GetWindowLongPtrA.errcheck = LPVOID_errcheck

try:
    SetWindowLongPtrA = ctypes.windll.user32.SetWindowLongPtrA
except:
    SetWindowLongPtrA = ctypes.windll.user32.SetWindowLongA
SetWindowLongPtrA.argtypes = [HWND, ctypes.c_int, LONG_PTR]
SetWindowLongPtrA.restype = LONG_PTR
GetWindowLongPtrA.errcheck = LPVOID_errcheck

SystemParametersInfoA = ctypes.windll.user32.SystemParametersInfoA
SystemParametersInfoA.argtypes = [UINT, UINT, LPVOID, UINT]
SystemParametersInfoA.restype = BOOL
SystemParametersInfoA.errcheck = Win32API_errcheck

SendMessageA = ctypes.windll.user32.SendMessageA
SendMessageA.argtypes = [HWND, UINT, WPARAM, LPARAM]
SendMessageA.restype = LRESULT

GetClientRect = ctypes.windll.user32.GetClientRect
GetClientRect.argtypes = [HWND, LPRECT]
GetClientRect.restype = BOOL
GetClientRect.errcheck = Win32API_errcheck

GetModuleHandleA = ctypes.windll.kernel32.GetModuleHandleA
GetModuleHandleA.argtypes = [LPCSTR]
GetModuleHandleA.restype = HMODULE
GetModuleHandleA.errcheck = LPVOID_errcheck

CreateFontIndirectA = ctypes.windll.gdi32.CreateFontIndirectA
CreateFontIndirectA.argtypes = [LPLOGFONTA]
CreateFontIndirectA.restype = HFONT
CreateFontIndirectA.errcheck = LPVOID_errcheck

EnumChildWindows = ctypes.windll.user32.EnumChildWindows
EnumChildWindows.argtypes = [HWND, WNDENUMPROC, LPARAM]
EnumChildWindows.restype = BOOL

GetSaveFileNameA = ctypes.windll.comdlg32.GetSaveFileNameA
GetSaveFileNameA.argtypes = [LPOPENFILENAMEA]
GetSaveFileNameA.restype = BOOL

CommDlgExtendedError = ctypes.windll.comdlg32.CommDlgExtendedError
CommDlgExtendedError.argtypes = None
CommDlgExtendedError.restype = DWORD

GetOpenFileNameA = ctypes.windll.comdlg32.GetOpenFileNameA
GetOpenFileNameA.argtypes = [LPOPENFILENAMEA]
GetOpenFileNameA.restype = BOOL

GetWindowTextLengthA = ctypes.windll.user32.GetWindowTextLengthA
GetWindowTextLengthA.argtypes = [HWND]
GetWindowTextLengthA.restype = INT
GetClientRect.errcheck = Win32API_errcheck

GetWindowTextA = ctypes.windll.user32.GetWindowTextA
GetWindowTextA.argtypes = [HWND, LPSTR, INT]
GetWindowTextA.restype = INT
GetWindowTextA.errcheck = Win32API_errcheck

class Scrambler:
    _KEY = "CHANGE ME TO YOUR OWN RANDOM STRING"

    @staticmethod
    def scramble(data: bytearray):
        for i in range(0, len(data)):
            data[i] = data[i] ^ ord(Scrambler._KEY[i % len(Scrambler._KEY)])

class UnityPlayerPerfs:
    _KEY_OVERRIDES: List[Tuple[str, str]] = [
        ('my_total_exp',              'myTotalExp'),
        ('emf_reader_inventory',      'EMFReaderInventory'),
        ('uv_flashlight_inventory',   'UVFlashlightInventory'),
        ('dslr_camera_inventory',     'DSLRCameraInventory'),
        ('ir_light_sensor_inventory', 'IRLightSensorInventory'),
        ('evp_recorder_inventory',    'EVPRecorderInventory'),
        ('completed_training',        'completedTraining')
    ]

    def __init__(self):
        self.my_total_exp:                   int = 0
        self.players_money:                  int = 0
        self.emf_reader_inventory:           int = 0
        self.flash_light_inventory:          int = 0
        self.camera_inventory:               int = 0
        self.lighter_inventory:              int = 0
        self.candle_inventory:               int = 0
        self.uv_flashlight_inventory:        int = 0
        self.crucifix_inventory:             int = 0
        self.dslr_camera_inventory:          int = 0
        self.evp_recorder_inventory:         int = 0
        self.salt_inventory:                 int = 0
        self.sage_inventory:                 int = 0
        self.tripod_inventory:               int = 0
        self.strong_flashlight_inventory:    int = 0
        self.motion_sensor_inventory:        int = 0
        self.sound_sensor_inventory:         int = 0
        self.sanity_pills_inventory:         int = 0
        self.thermometer_inventory:          int = 0
        self.ghost_writing_book_inventory:   int = 0
        self.ir_light_sensor_inventory:      int = 0
        self.parabolic_microphone_inventory: int = 0
        self.glowstick_inventory:            int = 0
        self.head_mounted_camera_inventory:  int = 0
        self.completed_training:             int = 0

    @staticmethod
    def _snake_to_camel(snake: str):
        return ''.join([a.title() for a in snake.split('_')])

    @staticmethod
    def _format_entry(key: str, value: Any):
        return {
            "Key": key,
            "Value": value
        }

    @staticmethod
    def _is_overrided_key(key: str):
        for t in UnityPlayerPerfs._KEY_OVERRIDES:
            if t[0] == key:
                return t[1]
        return None

    def to_phasmophobia_json_format(self):
        data_container: Dict[str, List[Dict[str, Union[str, int, float, bool]]]] = {
            "StringData": [],
            "IntData": [],
            "FloatData": [],
            "BoolData": [],
        }

        player_perfs_vars = vars(self)
        reformatted_player_perfs_vars = {}

        for k, v in player_perfs_vars.items():
            overrided_key = UnityPlayerPerfs._is_overrided_key(k)
            if overrided_key:
                reformatted_player_perfs_vars[overrided_key] = v
            else:
                reformatted_player_perfs_vars[UnityPlayerPerfs._snake_to_camel(k)] = v

        player_perfs_vars = reformatted_player_perfs_vars
        for k, v in player_perfs_vars.items():
            if isinstance(v, str):
                container = data_container["StringData"]
            elif isinstance(v, int):
                container = data_container["IntData"]
            elif isinstance(v, float):
                container = data_container["FloatData"]
            elif isinstance(v, bool):
                container = data_container["BoolData"]
            else:
                raise ValueError(f"{k} contains an unsupported type.")

            container.append(
                UnityPlayerPerfs._format_entry(k, v)
            )

        return json.dumps(data_container, indent=4)

@WNDPROC
def WindowProc(hwnd, uMsg, wParam, lParam):
    if uMsg == 0x2: #WM_QUIT
        PostQuitMessage(0)
    if uMsg == 0x16: #WM_CLOSE
        DestroyWindow(hwnd)
    if uMsg == 0x0111: #WM_NOTIFY
        control_id = LOWORD(wParam).value
        notification_code = HIWORD(wParam).value
        control_hwnd = lParam

        if control_id == SAVE_BUTTON:
            source_text = b"saveData.txt"
            text_buffer = ctypes.create_string_buffer(MAX_PATH)
            ctypes.memmove(text_buffer, source_text, len(source_text))

            openfilename = OPENFILENAMEA()
            openfilename.lStructSize = ctypes.sizeof(OPENFILENAMEA)
            openfilename.hwndOwner = None
            openfilename.lpstrFile = ctypes.cast(text_buffer, ctypes.c_char_p)
            openfilename.nMaxFile = ctypes.sizeof(text_buffer)
            openfilename.lpstrFilter = b"All Files (*.*)\0*.*\0Text File (*.txt)\0"
            openfilename.nFilterIndex = 2
            openfilename.lpstrFileTitle = None
            openfilename.nMaxFileTitle = 0
            openfilename.lpstrInitialDir = None
            openfilename.Flags = 0x00000002

            result = GetSaveFileNameA(ctypes.byref(openfilename))
            if result == 0:
                print("CommDlgExtendedError: ", CommDlgExtendedError())
            else:
                hwnd_textbox = GetDlgItem(hwnd, TEXT_BOX)
                textbox_length = GetWindowTextLengthA(hwnd_textbox)

                textbox_text = ctypes.create_string_buffer(textbox_length + 1)
                GetWindowTextA(hwnd_textbox, textbox_text, textbox_length + 1)

                save_json = json.loads(textbox_text.value.decode('ascii'))
                with open(text_buffer.value.decode('ascii'), 'wb') as save_file:
                    save_data = bytearray(json.dumps(save_json).replace(' ', '').encode('ascii'))
                    Scrambler.scramble(save_data)
                    save_file.write(save_data)
        elif control_id == OPEN_BUTTON:
            text_buffer = ctypes.create_string_buffer(MAX_PATH)

            openfilename = OPENFILENAMEA()
            openfilename.lStructSize = ctypes.sizeof(OPENFILENAMEA)
            openfilename.hwndOwner = None
            openfilename.lpstrFile = ctypes.cast(text_buffer, ctypes.c_char_p)
            openfilename.nMaxFile = ctypes.sizeof(text_buffer)
            openfilename.lpstrFilter = b"All Files (*.*)\0*.*\0Text File (*.txt)\0*.txt\0"
            openfilename.nFilterIndex = 2
            openfilename.lpstrFileTitle = None
            openfilename.nMaxFileTitle = 0
            openfilename.lpstrInitialDir = None
            openfilename.Flags = 0x00000800 | 0x00001000
            result = GetOpenFileNameA(ctypes.byref(openfilename))
            if not result:
                print("CommDlgExtendedError: ", CommDlgExtendedError())
            else:
                textbox_hwnd = GetDlgItem(hwnd, TEXT_BOX)
                with open(text_buffer.value.decode('ascii'), 'rb') as save_file:
                    save_data = bytearray(save_file.read())
                    Scrambler.scramble(save_data)
                    save_data_json = save_data.decode('ascii')
                    json_data = json.loads(save_data_json)

                    SetWindowTextA(
                        textbox_hwnd,
                        json.dumps(json_data, indent=4).replace('\n','\r\n').encode('ascii')
                    )


    return DefWindowProcA(hwnd, uMsg, wParam, lParam)

@WNDENUMPROC
def EnumChildProc(hwnd, lParam):
    result = SendMessageA(hwnd, 0x0030, WPARAM(lParam),
                          MAKELPARAM(1, 0))
    return True

if __name__ == "__main__":
    hinstance = GetModuleHandleA(None)

    window_class = WNDCLASSA()
    window_class.style = 0x0001 | 0x0002
    window_class.lpfnWndProc = WindowProc
    window_class.hInstance = hinstance
    window_class.lpszClassName = CLASS_NAME
    window_class.hbrBackground = HBRUSH(5)
    RegisterClassA(ctypes.byref(window_class))

    hwnd_main = CreateWindowExA(
        0,
        CLASS_NAME,
        WINDOW_NAME,
        0x00000000 | 0x00C00000
        | 0x00080000 | 0x00020000,
        CW_USEDEFAULT, CW_USEDEFAULT, 600, 480,
        None,
        None,
        hinstance,
        None
    )

    client_rect = RECT()
    GetClientRect(hwnd_main, ctypes.byref(client_rect))

    #0x00000200
    hwnd_st_u = CreateWindowExA(
        0,
        b"Edit",
        b"test",
        0x40000000 | 0x10000000 | 0x0000 | 0x0004 | 0x0040 | 0x00800000 | 0x00200000,
        10, 10,
        client_rect.right - client_rect.left - 20,
        client_rect.bottom - client_rect.top - 30 - 23,
        hwnd_main,
        HMENU(TEXT_BOX),
        GetWindowLongPtrA(hwnd_main, -6),
        None
    )

    button_width = 100
    button_height = 23
    hwnd_save_button = CreateWindowExA(
        0,
        b"BUTTON",
        b"Save As...",
        0x00010000 | 0x10000000 | 0x40000000 | 0x00000000,
        client_rect.right - client_rect.left - button_width - 10,
        client_rect.bottom - client_rect.top - button_height - 10,
        button_width, button_height,
        hwnd_main,
        HMENU(SAVE_BUTTON),
        GetWindowLongPtrA(hwnd_main, -6),
        None
    )

    hwnd_open_button = CreateWindowExA(
        0,
        b"BUTTON",
        b"Open...",
        0x00010000 | 0x10000000 | 0x40000000 | 0x00000000,
        10,
        client_rect.bottom - client_rect.top - button_height - 10,
        button_width, button_height,
        hwnd_main,
        HMENU(OPEN_BUTTON),
        GetWindowLongPtrA(hwnd_main, -6),
        None
    )

    default_player_perfs = UnityPlayerPerfs()
    default_player_perfs.completed_training = 1

    SetWindowTextA(
        hwnd_st_u,
        default_player_perfs.to_phasmophobia_json_format().replace('\n','\r\n').encode('ascii')
    )

    ShowWindow(hwnd_main, 5)

    metrics = NONCLIENTMETRICSA()
    metrics.cbSize = ctypes.sizeof(NONCLIENTMETRICSA)
    # SPI_GETNONCLIENTMETRICS = 0x0029
    SystemParametersInfoA(0x0029, metrics.cbSize, ctypes.byref(metrics), 0)
    font = CreateFontIndirectA(ctypes.byref(metrics.lfMenuFont))

    EnumChildWindows(hwnd_main, EnumChildProc,
                     LPARAM(ctypes.cast(font, ctypes.c_void_p).value))

    msg = MSG()
    while (bRet := GetMessageA(ctypes.byref(msg), None, 0, 0)) != 0:
        if bRet == -1:
            break
        TranslateMessage(ctypes.byref(msg))
        DispatchMessageA(ctypes.byref(msg))
