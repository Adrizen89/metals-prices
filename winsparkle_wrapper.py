import ctypes
from ctypes import wintypes


# Chemin vers le fichier DLL de WinSparkle
WINS_PARKLE_DLL_PATH = './WinSparkle.dll'

# Charger la DLL
winsparkle_dll = ctypes.windll.LoadLibrary(WINS_PARKLE_DLL_PATH)

# Définition des types de retour et d'arguments pour les fonctions de WinSparkle
winsparkle_dll.win_sparkle_set_appcast_url.restype = None
winsparkle_dll.win_sparkle_set_appcast_url.argtypes = [wintypes.LPCWSTR]

winsparkle_dll.win_sparkle_init.restype = None

winsparkle_dll.win_sparkle_cleanup.restype = None

winsparkle_dll.win_sparkle_check_update_without_ui.restype = None

# Définition des fonctions Python qui appellent les fonctions DLL
def initialize_winsparkle(appcast_url):
    winsparkle_dll.win_sparkle_set_appcast_url(appcast_url)
    winsparkle_dll.win_sparkle_init()
    
def cleanup_winsparkle():
    winsparkle_dll.win_sparkle_cleanup()

def check_update_without_ui():
    winsparkle_dll.win_sparkle_check_update_without_ui()