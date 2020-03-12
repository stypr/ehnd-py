# coding: utf-8

"""
trans.py

Translation Engine
"""

import os
import re
from ctypes import WinDLL, c_char_p, c_int, c_wchar_p
from ctypes.wintypes import BOOL

class TransEngine:
    """
    TransEngine class

    Introduces basic methods for translation
    """
    trans_dir = ""
    start = None
    trans = None

    def encode_text(self, text):
        """ (TransEngine, str) -> str

        Convert unicode literal to character
        """
        return re.sub(
            r"(?i)(?<!\\)(?:\\\\)*\\u([0-9a-f]{4})",
            lambda m: chr(int(m.group(1), 16)),
            text,
        )

    def decode_text(self, text):
        """ (TransEngine, str) -> str

        Convert special characters to unicode literal
        """
        char_range = [161, 733, 65510]
        char_range += range(8319, 8602)
        char_range += [8719, 8764, 8857]
        char_range += range(9312, 9850)
        char_range += range(12800, 12928)
        char_range += range(13184, 13278)
        char_range += range(65282, 65287)

        for _char in char_range:
            _char_c = chr(_char)
            if _char_c in text:
                text = text.replace(_char_c, "\\u" + str(hex(_char))[2:])
        return text

    def initialize(self):
        """
        Initialize argument and return types for DLL functions
        """
        if not (self.start and self.trans):
            return Exception("%s failed to load pointers."  % (self.__class__.__name__,))

        self.start.argtypes = [c_char_p, c_char_p]
        self.start.restype = BOOL
        self.trans.argtypes = [c_int, c_wchar_p]
        self.trans.restype = c_wchar_p
        self.start(
            "CSUSER123455".encode(),
            os.path.join(self.trans_dir, "Dat").encode()
        )

    def translate(self, src_text):
        """ (TransEngine, str) -> str

        Translate text and return translated string
        """
        trans_obj = self.trans(0, self.decode_text(src_text))
        return self.encode_text(trans_obj)


class TransEngineKRJP(TransEngine):
    """
    TransEngineKRJP

    Korean to Japanese Engine
    """
    def __init__(self, trans_dir):
        # set TransEZ dir
        self.trans_dir = trans_dir

        # load DLL, load ptr
        engine = WinDLL(os.path.join(trans_dir, "ehnd-kor.dll"))
        self.start = engine.K2J_InitializeEx
        self.trans = engine.K2J_TranslateMMNTW
        self.initialize()


class TransEngineJPKR(TransEngine):
    """
    TransEngineJPKR

    Japanese to Korean Engine
    """

    def __init__(self, trans_dir):
        # set TransEZ dir
        self.trans_dir = trans_dir

        # load DLL, load ptr
        engine = WinDLL(os.path.join(trans_dir, "ehnd.dll"))
        self.start = engine.J2K_InitializeEx
        self.trans = engine.J2K_TranslateMMNTW
        self.initialize()
