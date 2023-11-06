import ctypes

# Charger le fichier .dll
winsparkle = ctypes.cdll.LoadLibrary('./WinSparkle.dll')

def initialize_winsparkle(appcast_url):
    winsparkle.win_sparkle_set_appcast_url(appcast_url.encode('utf-8'))
    winsparkle.win_sparkle_init()
    
def cleanup_winsparkle():
    winsparkle.win_sparkle_cleanup()