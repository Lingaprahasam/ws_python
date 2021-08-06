from pywinauto.application import Application
app = Application(backend="uia").start('notepad++.exe')

# describe the window inside Notepad.exe process
dlg_spec = app.UntitledNotepad
# wait till the window is really open
actionable_dlg = dlg_spec.wait('visible')