#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is an the script for the pilot study of Project 'ReapDopa', which study the effect
Created on Fri. May 25, 2018.
@author: Chuan-Peng Hu, PHD, Neuroimaging Center, Mainz
@email: hcp4715 at gmail dot com

This script is used for the first stage of the experiment, in which
participant get familiar with the shapes and the rating task later.

In this task, participants will view 20 CS stimuli (geometric shapes) and rate at the end of each block

"""
# from __future__ import absolute_import, division
import psychopy
import wx, os, time, sys,csv
from psychopy import parallel, locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
import numpy as np  # whole numpy lib is available, prepend 'np.'
from numpy import (sin, cos, tan, log, log10, pi, average,
                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle  # Note here that we used the numpy.random module
from itertools import groupby

# define a function to get key
def get_keypress():
    keys = event.getKeys(keyList=['escape'])
    if keys:
        return keys[0]
    else:
        return None

# define a function to exit
def shutdown():
    win.close()
    core.quit()


# get subject information before open windows
expName = 'reapp_consolid_fam'  # from the Builder filename that created this script
expInfo = {'session': '01', 'participantID': 's1', 'gender': '', 'age': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()  # user pressed cancel
expInfo['date'] = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

# get the current directory and change the cd
_thisDir = os.path.dirname(os.path.abspath(__file__))
os.chdir(_thisDir)

# Setup the Window
app = wx.App(False)
display_width = wx.GetDisplaySize()[0]   # get the width of the display
display_height = wx.GetDisplaySize()[1]  # get the height of the display
win = visual.Window(size=[display_width, display_height],     # size of the window, better not full screen when debuggging
                    fullscr=True,       # better False
                    screen=0,
                    allowGUI=True,
                    allowStencil=False,
                    monitor='testMonitor',
                    color=[0,0,0],       # mind the colorSpace
                    colorSpace='rgb',    # chose the colorSpace and change accordingly
                    blendMode='avg',
                    useFBO=True,
                    units='pix')         # important about the units, change the value for defining it accordingly
win.mouseVisible = False # hide the mouse

# strange phenomenon in inpout32.py: Only pins 2-9 (incl) are normally used for data output
def send_code(code):
    '''    This is a function for sending trigger to our parallel port
    :param code: code number
    :return: the code that recognizable for our digitimer and bio-pac

    in behavioural lab 2, pin 2 is digitimer, pin 3 is channel 28, pin 4 is channel 29.
    '''
    # set all the port to zero befor the experiment start
    port = parallel.ParallelPort(0x0378)
    port.setData(0) # set all pins low
    if code == 1:         # marker the start of block
        port.setPin(2, 0) # Send 0 to pin 2, i.e., no shcok
        port.setPin(3, 1) # Send 1 to pin 3 (channel 28), as marker
        port.setPin(4, 1) # Send 1 to pin 4 (channel 29), as marker
        core.wait(0.03)
        port.setPin(2, 0) # pin 2 back to 0
        port.setPin(3, 0) # pin 3 back to 0
        port.setPin(4, 0) # pin 4 back to 0
    elif code == 3:  # CS+
        port.setPin(2, 0) # Send 0 to pin 2, i.e., no shcok
        port.setPin(3, 1) # Send 1 to pin 3, as marker
        port.setPin(4, 0) # Send 0 to pin 4, as marker
        core.wait(0.03)
        port.setPin(2, 0) # pin 2 back to 0
        port.setPin(3, 0) # pin 3 back to 0
        port.setPin(4, 0) # pin 1 back to 0
    elif code == 2:  # CS+
        port.setPin(2, 0) # Send 0 to pin 2, i.e., no shcok
        port.setPin(3, 1) # Send 1 to pin 3, as marker
        port.setPin(4, 0) # Send 0 to pin 4, as marker
        core.wait(0.03)
        port.setPin(2, 0) # pin 2 back to 0
        port.setPin(3, 0) # pin 3 back to 0
        port.setPin(4, 0) # pin 1 back to 0
    elif code == 4:         # CS-
        port.setPin(2, 0) # Send 1 to pin 2, i.e., no shcok
        port.setPin(3, 0) # Send 1 to pin 3, as marker
        port.setPin(4, 1) # Send 0 to pin 4, as marker
        core.wait(0.03)
        port.setPin(2, 0) # pin 2 back to 0
        port.setPin(3, 0) # pin 3 back to 0
        port.setPin(4, 0) # pin 4 back to 0

def send_shocks(code):
    '''    This is a function for sending trigger to elicit the shock
    :param code: code number
    :return: the code that recognizable for our digitimer and bio-pac
        in behavioural lab 2, pin 2 is digitimer, pin 3 is channel 28, pin 4 is channel 29.
    '''
    # set all the port to zero befor the experiment start
    port = parallel.ParallelPort(0x0378)
    port.setData(0) # set all pins low
    if code == 2:         # marker the start of block
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
    else:
        port.setData(0)
        core.wait(0.025*5)
        print('No shock')

# define a function for presenting message
def text_msg(msg,loc,fontheight):
    ''' display a short text message
    '''
    msgCon = visual.TextStim(win,
                    text=msg,
                    font='Arial',
                    height=fontheight,
                    pos=loc,
                    color=black,
                    colorSpace='rgb',
                    opacity=1,
                    depth=0.0,
                    units='pix')
    msgCon.draw()

# define a function for presenting geometrical shapes, three input params: location, size and orientation.
def shapePres(loc,shapeSize,shapeOrient):
    ''' display a short text message
    for a fixed duration
    '''
    curShape = visual.ShapeStim(win,
                    units='pix',
                    lineWidth=1.5,                                           # width of outline
                    lineColor=black, lineColorSpace='rgb',                   # color of outline
                    fillColor=black,fillColorSpace='rgb',                    # color of fill
                    vertices=((-0.5,-0.5),(0.5,-0.5),(0.5,0.5),(-0.5,0.5)),  # the four point of the shape
                    size=shapeSize,                                          # size of the shape, units=pixel
                    pos= loc,                                                # position of the shape
                    ori=shapeOrient,                                         # orientation of the shape
                    opacity=1,
                    contrast=1.0,
                    depth=1.0,
                    interpolate=True,
                    autoLog=None,
                    autoDraw=False)
    curShape.draw()

def erRatings(sessID,blockID,name, blockType):
    ''' This is the function for rating the strategy
    '''
    curER_Rating = visual.RatingScale(win=win,
                                   low = 0,
                                   high = 100,
                                   precision=3,
                                   #tickMarks=(0,100),       # the location of tick marker
                                   tickHeight=1,          # suppress the ticker
                                   markerStart=np.random.choice(np.arange(3.0,7.0,0.1),1),
                                   scale = None,
                                   labels = ('gar nicht erfolgreich', 'sehr erfolgreich'),
                                   stretch = 1.5,
                                   pos=(0.0, -100),          # this is the default setting
                                   leftKeys=['1', 'left'],   # keys for moving left
                                   rightKeys=['2', 'right'], # keys for moving right
                                   acceptKeys=['3','return'],# keys for accept the ratings
                                   noMouse=True,
                                   showValue=False,          # param for showing value or not
                                   name=name)                # the name for current rating
    curER_Rating.slidingInterval = 0.1
    # waiting for response
    escDown = None
    while curER_Rating.noResponse and escDown is None:
        escDown = get_keypress()
        if escDown is not None:
            shutdown()
        # prepare the instruction for rating emotion regulation strategy
        imName = _thisDir + os.sep + 'stim' + os.sep + 'rating_strag.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 100])
        showImage.draw()
        # prepare the scale
        curER_Rating.draw()
        win.flip()
    get_rating = curER_Rating.getRating()
    decision_time = curER_Rating.getRT()

    # write the rating
    resultRec = open(blockFilename,'a+')
    curLine = ','.join(map(str,[sessID,blockID,'strategyRating', blockType,get_rating,decision_time]))
    resultRec.write(curLine)
    resultRec.write('\n')
    resultRec.close()

# define a function for rating the shapes,
def csRatings(sessID,blockID,name, shape):
    ''' This is the function for rating their feelings about shapes
    '''
    curRating = visual.RatingScale(win=win,
                                   low = 0,
                                   high = 100,
                                   precision=3,
                                   #tickMarks=(0,100),       # the location of tick marker
                                   tickHeight=1,            # suppress the ticker
                                   markerStart=np.random.choice(np.arange(3.0,7.0,0.1),1),
                                   scale = None,
                                   labels = ('sehr niedrig', 'sehr hoch'),
                                   stretch = 1.5,
                                   pos=(0.0, -150),          # this is the default setting
                                   leftKeys=['1', 'left'],   # keys for moving left
                                   rightKeys=['2', 'right'], # keys for moving right
                                   acceptKeys=['3','return'],# keys for accept the ratings
                                   noMouse=True,             # use mouse or not
                                   showValue=False,          # param for showing value or not
                                   name=name)                # the name for current rating
    curRating.slidingInterval = 0.1
    escDown = None
    while curRating.noResponse and escDown is None:
        escDown = get_keypress()
        if escDown is not None:
            shutdown()
        imName = _thisDir + os.sep + 'stim' + os.sep + 'rating_shape.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 150])
        showImage.draw()

        if shape == "sq":   # if the shape is square
            shapePres([0, 0], 100,0)
        else:               # if the shape is rho
            shapePres([0, 0], 100, 45)

        curRating.draw()
        win.flip()
    cs_get_rating = curRating.getRating()
    cs_decision_time = curRating.getRT()

    # write the rating
    resultRec = open(blockFilename,'a+')
    curLine = ','.join(map(str,[sessID,blockID,'AnxRating', shape,cs_get_rating,cs_decision_time]))
    resultRec.write(curLine)
    resultRec.write('\n')
    resultRec.close()

# function to run a mini-block
def run_block(sessID,blockID,minblocktype,trialList,trialFile):
    # present instruction for the mini block
    if minblocktype == 'R':
        imName = _thisDir + os.sep + 'stim' + os.sep + 'Reg.jpg'
        imName_c = _thisDir + os.sep + 'stim' + os.sep + 'Reg_s.jpg'
        InstrCont = 'regulation'
    else:
        imName = _thisDir + os.sep + 'stim' + os.sep + 'NoReg.jpg'
        imName_c = _thisDir + os.sep + 'stim' + os.sep + 'NoReg_s.jpg'
        InstrCont = 'NoRegulation'
    showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
    showImage_c = visual.ImageStim(win, image=imName_c,pos=[0, -400]) # keep showing the cue
    # present the the instruction for 10 s
    timer = core.Clock()
    timer.add(10)
    escDown = None
    while timer.getTime() < 0 and escDown is None:
        escDown = get_keypress()
        if escDown is not None:
            shutdown()
        showImage.draw()
        showImage_c.draw()
        win.flip()

    # present fixation for 30 secs
    imName = _thisDir + os.sep + 'stim' + os.sep + 'fixation.jpg'
    showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
    timer = core.Clock()
    timer.add(30)
    escDown = None
    while timer.getTime() < 0 and escDown is None:
        escDown = get_keypress()
        if escDown is not None:
            shutdown()
        showImage.draw()
        showImage_c.draw()
        win.flip()

    # shuffle the trial list, re-shuffle when more then 3 repetitions
    tmp = ['0','1','2','3','4']  # get a temperary list for storing the shuffled trial list
    while True:
        np.random.shuffle(trialList)  # randomizing the trials
        for ii in (range(len(trialList))):
            tmp[ii] = (trialList[ii][0])
        grouped_L = [(k, sum(1 for i in g)) for k,g in groupby(tmp)]
        int(max(grouped_L)[1])
        print(int(max(grouped_L)[1]))
        if int(max(grouped_L)[1]) <= 2:
            break
    # present target for 15 sec.
    for ii in range(len(trialList)):
        if event.getKeys(keyList=["escape"]):
            core.quit()
        curTr = trialList[ii]
        shape, shapeOri, stimType, trig = curTr
        send_code(trig)              # send triggers before start
        waitTime = np.random.randint(4,14,size=1) # randomly choose a time for shoscks
        timer = core.Clock()
        timer.add(waitTime[0])
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            shapePres([0,0],100,shapeOri)
            showImage_c.draw()
            win.flip()
        send_shocks(trig)                         # send shocks at the end of the stimuli presentation
        print('trigger code: ',trig, ". Wait time:", waitTime[0])
        timer = core.Clock()
        timer.add(15-waitTime[0]-5*0.25)
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            shapePres([0,0],100,shapeOri)
            showImage_c.draw()
            win.flip()
        win.flip()
        if ii <6:
            ITI = np.random.randint(4,8,size=1)   # the interval between trials, 4 ~ 8
            ITI = ITI[0]
        else:
            ITI = 0.5

        imName = _thisDir + os.sep + 'stim' + os.sep + 'fixation.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
        timer = core.Clock()
        timer.add(ITI)
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            showImage.draw()
            showImage_c.draw()
            win.flip()

        # write the rating
        resultRec = open(trialFile,'a+')
        curLine = ','.join(map(str,[sessID,blockID,ii+1,shape, shapeOri, stimType, trig,waitTime[0]]))
        resultRec.write(curLine)
        resultRec.write('\n')
        resultRec.close()

    # present fixation
    text_msg("+",(0,0),60)
    win.flip()
    core.wait(1)
    win.flip()

    # if "R" block, asked participant to think about his/her experience in previous block
    if minblocktype == 'R':
        imName = _thisDir + os.sep + 'stim' + os.sep + 'rating_strag_reminder.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
        showImage.draw()
        win.flip()
        timer = core.Clock()
        timer.add(10)
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            showImage.draw()
            win.flip()
        #core.wait(10)    # wait 10 seconds.

        # present fixation for 20 seconds
        imName = _thisDir + os.sep + 'stim' + os.sep + 'fixation.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
        #text_msg("+",(0,0),60)  # present the fixation and wait for ITI
        timer = core.Clock()
        timer.add(20)
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            showImage.draw()
            win.flip()
        erRating = erRatings(sessID,blockID,"str_ratings", InstrCont)   # rating the strategy

    cs1Rating = csRatings(sessID,blockID,"sq_ratings",'sq')         # rating the shape square
    cs2rating = csRatings(sessID,blockID,"ro_ratings",'ro')         # rating the ro

#### real experiemnt starts here.

# define constants
black = [-1, -1, -1]
white = [1, 1, 1]
grey  = [0, 0, 0]

# to go the data folder
if not os.path.exists('data'):os.mkdir('data')

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
trialFilename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participantID'],expInfo['date'],'_trial_fam.txt')
initLine = open(trialFilename,'w')
curLine = ','.join(map(str,['Session','Block','trialOrd', 'shape', 'shapeOri', 'stimType', 'trig','waitTime']))
initLine.write(curLine)
initLine.write('\n')
initLine.close()

blockFilename = _thisDir + os.sep + u'data/%s_%s_%s' % (expInfo['participantID'],expInfo['date'],'_block_fam.txt')
initLine = open(blockFilename,'w')
curLine = ','.join(map(str,['Session','Block','strategyRating', 'blockType', 'Ratings', 'Rating_time']))
initLine.write(curLine)
initLine.write('\n')
initLine.close()

# get the pseudo random list for subjects
reader = csv.reader(open('pseudOrd_d1.csv', 'r'))
pseudorand = {}
for k, v in reader:
   pseudorand[k] = v

# define block params.
blocks = [['R','NR']]
# define trial params.
# randomize the CS+, CS-.
# randCond = np.random.choice([1,2],1)
randCond = pseudorand[expInfo['participantID']]
if randCond ==1:
#           shape, orient, stimType, trigger
    trials = [['sq', 0,  'CS+', 3],   # CS+ with shock
              ['ro', 45, 'CS-', 4]]
else:
    trials = [['ro', 45,  'CS+', 3],
              ['sq', 0, 'CS-', 4]]

# show the instructions

text_msg("Das Experiment beginnt jetzt.", (0, 0),30)
win.flip()
event.waitKeys(maxWait=20.0,keyList=['space']) # wait for participants' response to proceed


# show the instructed fear
if randCond == '1':
    imName = _thisDir + os.sep + 'stim' + os.sep + 'd1_cond1_fam_s.jpg'
    showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
    showImage.draw()
else:
    imName = _thisDir + os.sep + 'stim' + os.sep + 'd1_cond2_fam_s.jpg'
    showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
    showImage.draw()
win.flip()
event.waitKeys(maxWait=20.0,keyList=['space']) # wait for participants' response to proceed

send_code(1)   # start of the experiment, send two codes
for ii in range(len(blocks)):
    SessID = ii + 1
    curSess = blocks[0]
    print('Session: ', SessID)
    for jj in range(len(curSess)):
        blockID = jj + 1
        curBlock = curSess[jj]
        print('blockType:',curBlock, 'blockID:', blockID,)
        run_block(SessID, blockID, curBlock,trials,trialFilename)
    # show the instructions for the first two sessions
        if jj < len(blocks[ii])-1:
            imName = _thisDir + os.sep + 'stim' + os.sep + 'pause.jpg'
            showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
            escDown = None
            timer = core.Clock()
            timer.add(30)
            while timer.getTime() < 0 and escDown is None:
                escDown = get_keypress()
                if escDown is not None:
                    shutdown()

                showImage.draw()
                win.flip()       # present the instruction for resting
            #core.wait(30)     # wait for 30 seconds

# show thanks and goodbye
text_msg("Vielen Dank, wir starten nun mit dem Experiment.", [0, 0],30)
win.flip()
core.wait(1)

# exit
core.quit()
