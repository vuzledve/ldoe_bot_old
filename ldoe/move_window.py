import win32gui

#hwnd = win32gui.FindWindow("notepad", None)
hwnd = win32gui.FindWindow("Qt5154QWindowOwnDCIcon", None )
print("hwnd: (%d)" % (hwnd))

x0, y0, x1, y1 = win32gui.GetWindowRect(hwnd)
w = x1 - x0
h = y1 - y0
win32gui.MoveWindow(hwnd, 0, 0, 960, 540, True)
print("Window %s:" % win32gui.GetWindowText(hwnd))
print("\t    Size: (%d, %d)" % (w, h))