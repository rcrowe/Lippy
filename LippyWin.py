
from ctypes import windll, Structure, c_short, c_ushort, byref

class COORD(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("X", c_short),
    ("Y", c_short)]

class SMALL_RECT(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("Left", c_short),
    ("Top", c_short),
    ("Right", c_short),
    ("Bottom", c_short)]

class CONSOLE_SCREEN_BUFFER_INFO(Structure):
  """struct in wincon.h."""
  _fields_ = [
    ("dwSize", COORD),
    ("dwCursorPosition", COORD),
    ("wAttributes", c_ushort),
    ("srWindow", SMALL_RECT),
    ("dwMaximumWindowSize", COORD)]

STD_OUTPUT_HANDLE = -11

FOREGROUND_BLUE      = 0x0001
FOREGROUND_CYAN      = 0x0003
FOREGROUND_RED       = 0x0004
FOREGROUND_YELLOW    = 0x0006
FOREGROUND_INTENSITY = 0x0008

stdout_handle              = windll.kernel32.GetStdHandle(STD_OUTPUT_HANDLE)
SetConsoleTextAttribute    = windll.kernel32.SetConsoleTextAttribute
GetConsoleScreenBufferInfo = windll.kernel32.GetConsoleScreenBufferInfo

default_colours = None

#Library must have output function
def output(level, level_str, client_address):
       
    #Get current terminal colours so we can revert
    default_colours = get()
    
    #Set the correct colour
    colour = None
    
    if level == 1:
        colour = FOREGROUND_CYAN
    elif level == 2:
        colour = FOREGROUND_BLUE | FOREGROUND_INTENSITY
    elif level == 3:
        colour = FOREGROUND_YELLOW
    elif level == 4:
        colour = FOREGROUND_RED
    elif level == 5:
        colour = FOREGROUND_RED | FOREGROUND_INTENSITY
        
    #Set colour
    set(colour)
    
    #Output
    print("\n%s - %s\n" % (level_str, client_address))
    
    #Revert to default colours
    set(default_colours)

def get():
    csbi = CONSOLE_SCREEN_BUFFER_INFO()
    GetConsoleScreenBufferInfo(stdout_handle, byref(csbi))
    return csbi.wAttributes
        
def set(color):
    SetConsoleTextAttribute(stdout_handle, color)