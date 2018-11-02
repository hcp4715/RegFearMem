# This script is for calibrating the magnitude of electrical shocks
# in Behavioral lab2 of NIC
# The original code is from Laura & ....
# I added more comments.
# --- C-P. Hu, @NIC, hcp4715@gmail.com

from psychopy import parallel, core, visual, event
import wx

port = parallel.ParallelPort(0x0378)
port.setData(0) # set all pins low

# One shock lasts 2 ms (can be changed manually on the digitimer)


# Create a window that fits the screen size
app = wx.App(False)
display_width = wx.GetDisplaySize()[0]
display_height = wx.GetDisplaySize()[1]
win = visual.Window(fullscr=False, allowGUI=False, monitor="testMonitor", color=[50, 50, 50], colorSpace='rgb255',
                    size=(display_width, display_height))

# this was for debugging, using small window instead of full screen.
# win = visual.Window(fullscr=False, allowGUI=False, monitor="testMonitor", color=[50, 50, 50], colorSpace='rgb255',
#                     size=(800, 600))

# Onset of stimulation
stimulation = True

# Draw waiting screen for participants
instruction = visual.TextStim(win, 'Bitte warten Sie auf die Aufforderung Ihrer Versuchsleitung. \n \n'
                              'Um den elektrischen Reiz zu starten, druecken Sie die Leertaste.',
                              color=[200, 200, 200], colorSpace='rgb255', height=0.06)

instruction.draw()
win.flip()

while stimulation:
    # Wait for keys
    keys = event.waitKeys(keyList=['space', 'return', 'escape'])
    for key in keys:
        if key == 'space':
            for i in range(2):    # Anzahl der Minischocks, die einen Gesamtschock ergeben
                port.setPin(2, 1) # Send 1 to pin 2, i.e., shcok
                print("shock 1")
                core.wait(0.025)
                port.setPin(2, 0) # pin 2 back to 0

                core.wait(0.025)
                port.setPin(2, 1) # Send 1 to pin 2, i.e., shcok
                print("shock 2")
                core.wait(0.025)
                port.setPin(2, 0) # pin 2 back to 0

                core.wait(0.025)
                port.setPin(2, 1) # Send 1 to pin 2, i.e., shcok
                print("shock 3")
                core.wait(0.025)
                port.setPin(2, 0) # pin 2 back to 0

        elif key == 'return':
            stimulation = False
        elif key == 'escape':
            stimulation = False
            core.quit()

danke = visual.TextStim(win, 'Vielen Dank. Bitte warten Sie auf Ihre Versuchsleitung.', color=[200, 200, 200],
                        colorSpace='rgb255')
danke.draw()
win.flip()

# Wait for experimenter to quit calibration
keys = event.waitKeys(keyList=['return'])
for key in keys:
    if key == 'return':
        core.quit()
