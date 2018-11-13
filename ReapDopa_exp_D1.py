#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This is an the script for the pilot study.

Author      Date           log of changes
=========   =============  ======================
C-P. Hu     May 25, 2018.  Initial version
C-p. Hu     Nov 12, 2018.  Revision after 1st participant.

Input:
     Participant ID, age, gender

Output:
    ERdopa_Pilot_d1_block_sX_2018_XXXX.txt   # the log file for each block (rating)
    ERdopa_Pilot_d1_trial_sX_2018_XXXX.txt   # the log file for each trials (Markers)

Note: this script include sending trigger to digitimer and biopac, please make sure that digitimer is connected with the
the Bio-pac

@author: Chuan-Peng Hu, PhD, Neuroimaging Center, Mainz
@email: hcp4715 at gmail dot com
"""
# from __future__ import absolute_import, division
import psychopy
import wx, os, time, sys,csv
from psychopy import parallel, locale_setup, sound, gui, visual, core, data, event, logging, clock
from psychopy.constants import (NOT_STARTED, STARTED, PLAYING, PAUSED,
                                STOPPED, FINISHED, PRESSED, RELEASED, FOREVER)
#from psychopy.iohub.client import launchHubServer, EventConstants

import numpy as np  # whole numpy lib is available, prepend 'np.'
#from numpy import (sin, cos, tan, log, log10, pi, average,
#                   sqrt, std, deg2rad, rad2deg, linspace, asarray)
from numpy.random import random, randint, normal, shuffle  # Note here that we used the numpy.random module
from itertools import groupby
import random

# define a function to get the ESCAPE key
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

# get the current directory and change the cd
# thisDir = os.path.dirname(os.path.realpath(__file__))
_thisDir = os.getcwd()
os.chdir(_thisDir)

# get subject information before open windows
expName = 'ERdopa_Pilot'  # This name will be part of the output file names.
expInfo = {'session': '01', 'participantID': 's1', 'gender': '', 'age': ''}
dlg = gui.DlgFromDict(dictionary=expInfo, title=expName)
if dlg.OK == False:
    core.quit()                         # user pressed cancel
expInfo['date']    = data.getDateStr()  # add a simple timestamp
expInfo['expName'] = expName

########################### Setup the Window ###############################################################
app = wx.App(False)
display_width  = wx.GetDisplaySize()[0]  # get the width of the display, strange, it is 1536, instead of 1920
display_height = wx.GetDisplaySize()[1]  # get the height of the display
win = visual.Window(size=[display_width, display_height],   # size of the window, better not full screen when debuggging
                    fullscr=True,        # better False when debugging
                    screen=0,            # chose the default monitor
                    allowGUI=True,
                    allowStencil=False,
                    monitor='testMonitor',
                    color=[0,0,0],       # mind the colorSpace
                    colorSpace='rgb',    # chose the colorSpace and change accordingly
                    blendMode='avg',
                    useFBO=True,
                    units='pix')         # important about the units, change the value for defining it accordingly

win.mouseVisible = False # hide the mouse

###################################### define constants ####################################################
black = [-1, -1, -1]
white = [1, 1, 1]
grey  = [0, 0, 0]

##################################### Define the data file ###################################################
# create a folder called "data" if not exits, and change directory to the folder
if not os.path.exists('data'):
    os.mkdir('data')

# Data file name stem = absolute path + name; later add .psyexp, .csv, .log, etc
# define the file name for recording each trial.
trialFilename = _thisDir + os.sep + u'data/%s_%s_%s_%s_%s' % (expInfo['expName'], 'd1_trial',expInfo['participantID'],expInfo['date'],'.txt')

# Write the header for the trial file.
initLine = open(trialFilename,'w')
curLine  = ','.join(map(str,['Session','Block','blockType', 'trialOrd', 'shape', 'stimType', 'trig','waitTime','startTime','endTime','ITI']))
initLine.write(curLine)
initLine.write('\n')
initLine.close()

# Define the file name for logging for block.
blockFilename = _thisDir + os.sep + u'data/%s_%s_%s_%s_%s' % (expInfo['expName'], 'd1_block',expInfo['participantID'],expInfo['date'],'.txt')

# Write the header for the block file
initLine = open(blockFilename,'w')
curLine = ','.join(map(str,['Session','Block','ratingType', 'blockType', 'CS(1+0-)','Ratings', 'Rating_time']))
initLine.write(curLine)
initLine.write('\n')
initLine.close()

######################### Prepare the pseudoraondom list of stimuli between participants ##################
reader = csv.reader(open('pseudOrd_d1.csv', 'r'))
pseudorand = {}
for k, v in reader:
   # k, v = row
   pseudorand[k] = v

########################################## Triggers & Shocks ##########################################################
# Define function for sending the code
# strange phenomenon in inpout32.py: Only pins 2-9 (incl) are normally used for data output
def send_code(code):
    '''    This is a function for sending trigger to our parallel port
    :param code: code number
    :return: the code that recognizable for our digitimer and bio-pac
    
    in behavioural lab 2, pin 2 is digitimer, pin 3 is channel 28, pin 4 is channel 29.
    '''
    # set all the port to zero before the experiment start
    port = parallel.ParallelPort(0x0378)
    port.setData(0) # set all pins low
    if code == 1:         # marker the start of block, both triggers are sent
        port.setPin(2, 0) # Send 0 to pin 2, i.e., no shcok
        port.setPin(3, 1) # Send 1 to pin 3 (channel 28), as marker
        port.setPin(4, 1) # Send 1 to pin 4 (channel 29), as marker
        core.wait(0.03)
        port.setPin(2, 0) # pin 2 back to 0
        port.setPin(3, 0) # pin 3 back to 0
        port.setPin(4, 0) # pin 4 back to 0
    elif code == 3:       # CS+
        port.setPin(2, 0) # Send 0 to pin 2, i.e., no shcok
        port.setPin(3, 1) # Send 1 to pin 3, as marker
        port.setPin(4, 0) # Send 0 to pin 4, as marker
        core.wait(0.03)
        port.setPin(2, 0) # pin 2 back to 0
        port.setPin(3, 0) # pin 3 back to 0
        port.setPin(4, 0) # pin 1 back to 0
    elif code == 2:       # CS+ with shocks
        port.setPin(2, 0) # Send 0 to pin 2, i.e., no shcok
        port.setPin(3, 1) # Send 1 to pin 3, as marker
        port.setPin(4, 0) # Send 0 to pin 4, as marker
        core.wait(0.03)
        port.setPin(2, 0) # pin 2 back to 0
        port.setPin(3, 0) # pin 3 back to 0
        port.setPin(4, 0) # pin 1 back to 0
    elif code == 4:       # CS-
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

###################################### Presenting Stim #################################################################
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
    #win.flip()

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
    #win.flip()

def erRatings(sessID,blockID,name):
    ''' This is the function for rating the strategy
    '''
    curER_Rating = visual.RatingScale(win=win,
                                   low = 0,
                                   high = 100,
                                   precision=3,
                                   #tickMarks=(0,100),      # the location of tick marker
                                   tickHeight=1,            # suppress the ticker
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
    escDown = None
    while curER_Rating.noResponse and escDown is None:
        escDown = get_keypress()
        if escDown is not None:
            shutdown()
        # prepare the instruction for rating emotion regulation strategy
        imName    = _thisDir + os.sep + 'stim' + os.sep + 'rating_strag.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 100])
        showImage.draw()
        # prepare the scale
        curER_Rating.draw()
        win.flip()
    get_rating    = curER_Rating.getRating()
    decision_time = curER_Rating.getRT()

    # write the rating
    resultRec = open(blockFilename,'a+')
    curLine = ','.join(map(str,[sessID,blockID,'StrRating', 1,'NA',get_rating,decision_time]))
    resultRec.write(curLine)
    resultRec.write('\n')
    resultRec.close()

# define a function for rating the shapes,
def csRatings(sessID,blockID,name, shape,blockType,randCond):
    ''' This is the function for rating their feelings about shapes
    '''
    curRating = visual.RatingScale(win=win,
                                   low = 0,
                                   high = 100,
                                   precision=3,
                                   #tickMarks=(0,100),      # the location of tick marker
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
        # prepare the instruction for rating emotion regulation strategy
        imName = _thisDir + os.sep + 'stim' + os.sep + 'rating_shape.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 150])
        showImage.draw()
        if shape == "sq":   # if the shape is square
            shapePres([0, 0], 100,0)
        else:               # if the shape is rho
            shapePres([0, 0], 100, 45)
        curRating.draw()
        win.flip()
    cs_get_rating    = curRating.getRating()
    cs_decision_time = curRating.getRT()
  # write the rating
    # recode the CS+ and CS-
    if (randCond == '1' and shape == 'sq') | (randCond == '2' and shape == 'ro'):
        CStype = 1    # define the CS+
    elif (randCond == '1' and shape == 'ro') | (randCond == '2' and shape == 'sq'):
        CStype = 0    # define the CS-

    # recode the block type
    if blockType == 'R':
        blockTypeCode = 1
    else:
        blockTypeCode = 0
    resultRec = open(blockFilename,'a+')
    # ['Session','Block','ratingType', 'blockType', 'CS(1+0-)','Ratings', 'Rating_time']
    curLine = ','.join(map(str,[sessID,blockID,'AnxRating', blockTypeCode, CStype,cs_get_rating,cs_decision_time]))
    resultRec.write(curLine)
    resultRec.write('\n')
    resultRec.close()

# function to run a mini-block
def run_block(sessID,blockID,minblocktype,trialList,trialFile,randCond, T0):
    # present instruction for the mini block
    if minblocktype == 'R':
        blockType = 1
        imName = _thisDir + os.sep + 'stim' + os.sep + 'Reg.jpg'
        imName_c = _thisDir + os.sep + 'stim' + os.sep + 'Reg_s.jpg'
        InstrCont = 'regulation'
    else:
        blockType = 0
        imName = _thisDir + os.sep + 'stim' + os.sep + 'NoReg.jpg'
        imName_c = _thisDir + os.sep + 'stim' + os.sep + 'NoReg_s.jpg'
        InstrCont = 'NoRegulation'
    showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
    showImage_c = visual.ImageStim(win, image=imName_c,pos=[0, -400]) # keep showing the cure under the lower part of the screeen
    # present the the intruction for 10 s
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
    # win.flip()

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
    if len(trialList) == 7:
        tmp = ['0','1','2','3','4','5','6']      # get a temporary list for storing the shuffled trial list
    else:
        tmp = ['0','1','2','3','4','5','6','7']  # get a temporary list for storing the shuffled trial list

    while True:
        np.random.shuffle(trialList)             # randomizing the trials
        for ii in (range(len(trialList))):
            tmp[ii] = (trialList[ii][0])
        grouped_L = [(k, sum(1 for i in g)) for k,g in groupby(tmp)]
        int(max(grouped_L)[1])
        print(int(max(grouped_L)[1]))
        if int(max(grouped_L)[1]) <= 2:
            break
    ### present target for 15 sec.

    # define the ITI before the loop started
    ITItemp = np.arange(5,10)                         # get the range
    ITI = np.random.choice(ITItemp,len(trialList)-1)  # random choice in the range
    np.random.shuffle(ITI)                            # suffle
    ITI= np.append(ITI,0)                           # append the last element

    # start the loop
    for ii in range(len(trialList)):
        curTr = trialList[ii]
        shape, shapeOri, stimType, trig = curTr
        send_code(trig)                            # send triggers before start
        print('trigger code: ',trig)
        win.flip()
        waitTime = np.random.randint(4,14,size=1)  # randomly choose a time for shocks
        timer = core.Clock()
        timer.add(waitTime[0])
        escDown = None
        T_c = core.getTime()                       #  get the time when trial started
        T_s = T_c - T0
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            shapePres([0,0],100,shapeOri,)
            showImage_c.draw()
            win.flip()
        print('waiting time: ',waitTime[0])
        send_shocks(trig)                          # send shocks after wait 4 ~ 14 seconds
        timer = core.Clock()
        timer.add(15 - waitTime[0]- 5*0.025)       # Wait for the rest of the time.
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            shapePres([0,0],100,shapeOri)
            showImage_c.draw()
            win.flip()
        win.flip()
        T_c = core.getTime()                       # Get the current time
        T_end = T_c - T0                           # Get the time when the trial ended
        #if ii < (len(trialList)-1):
        ITI_c = ITI[ii]                            # the interval between trials, 8 ~ 12 (ii start with 0, index start from 0)
        #ITI = ITI[0]
        #else:
        #    ITI_c = 0.5                              # ITI for last trial of each mini-block

        # present the fixation and wait for ITI_c
        imName = _thisDir + os.sep + 'stim' + os.sep + 'fixation.jpg'
        showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
        timer = core.Clock()
        timer.add(ITI_c)
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            showImage.draw()
            showImage_c.draw()
            win.flip()

        # write the trial information
        resultRec = open(trialFile,'a+')
        # re-code the stimType: CS+ =1; CS- =0;
        if stimType == 'CS+':
            stimCS = 1
        elif stimType == 'CS-':
            stimCS = 0
        # ['Session','Block','blockType', 'trialOrd', 'shape', 'stimType', 'trig','waitTime','startTime','endTime','ITI']
        curLine = ','.join(map(str,[sessID,blockID,blockType,ii+1,shape, stimCS, trig,waitTime[0],T_s,T_end,ITI_c]))
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
        timer = core.Clock()   # wait 30 seconds for participants to think about their strategy
        timer.add(30)
        escDown = None
        while timer.getTime() < 0 and escDown is None:
            escDown = get_keypress()
            if escDown is not None:
                shutdown()
            showImage.draw()
            win.flip()

        erRating = erRatings(sessID,blockID,"str_ratings")   # rating the strategy

    cs1Rating = csRatings(sessID,blockID,"sq_ratings",'sq',minblocktype,randCond)         # rating the shape square
    cs2rating = csRatings(sessID,blockID,"ro_ratings",'ro',minblocktype,randCond)         # rating the ro

# short break between blocks
    if (sessID == 1 and blockID == 1) or ( 4 > sessID > 1 and blockID < 3):   # within session rest: 10 seconds
        imName = _thisDir + os.sep + 'stim' + os.sep + 'pause_s.jpg'
        waitDur = 30                                                          # short break for the mini blocks within a session
    elif (sessID == 1 and blockID == 2) or (sessID == 2 and blockID == 3):    # between session rest: 60 secons
        imName = _thisDir + os.sep + 'stim' + os.sep + 'pause_l.jpg'
        waitDur = 60                                                          # long breaks between blocks
    elif sessID == 3 and blockID == 3:                                        # End of the experiment
        imName = _thisDir + os.sep + 'stim' + os.sep + 'fixation.jpg'
        waitDur = 5
    showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
    escDown = None
    timer = core.Clock()
    timer.add(waitDur)
    while timer.getTime() < 0 and escDown is None:
        escDown = get_keypress()
        if escDown is not None:
            shutdown()
        showImage.draw()
        win.flip()       # present the instruction for resting

################################# The Real experiemnt starts here ##################################################
# define block params.
blocks = [['R','NR'],
          ['NR','R','NR'],
          ['R','NR','R']]
# define trial params.
# randomize the CS+, CS-.
# randCond = np.random.choice([1,2],1)
randCond = pseudorand[expInfo['participantID']]

if randCond == '1':   # judge the condition
    print('random order 1')
    CSplus_1 = ['sq', 0,  'CS+', 2]  # CS+ with shocks
    CSplus_2 = ['sq', 0,  'CS+', 3]  # CS+ without shocks
    CSminus  = ['ro', 45, 'CS-', 4]  # CS-
else:
    print('random roder 2')
    CSplus_1 = ['ro', 45, 'CS+', 2] # CS+ with shock
    CSplus_2 = ['ro', 45, 'CS+', 3]
    CSminus  = ['sq', 0,  'CS-', 4]

# show the instructions
text_msg("Das Experiment beginnt jetzt.", (0, 0),30)
win.flip()

event.waitKeys(maxWait=20.0,keyList=['space']) # wait for participants' response to proceed

# show the instructed fear
if randCond == '1':
    imName = _thisDir + os.sep + 'stim' + os.sep + 'd1_cond1_s.jpg'
else:
    imName = _thisDir + os.sep + 'stim' + os.sep + 'd1_cond2_s.jpg'

showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
showImage.draw()
win.flip()

event.waitKeys(maxWait=20.0,keyList=['space']) # wait for participants' response to proceed

twoShockId = random.choice([2,3])              # random choose a block for two shocks

send_code(1)                                   # start of the experiment, send two codes
T0 = core.getTime()                            # get the time of experiment started

for ii in range(len(blocks)):
    SessID = ii + 1
    curSess = blocks[ii]
    # print('Session: ', SessID)

    for jj in range(len(curSess)):
        blockID = jj + 1
        curBlock = curSess[jj]
        #print('blockType:',curBlock, 'blockID:', blockID,)
        
        if twoShockId == 2:
            # print('Session 1 block 2 will have two shocks')
            twoShockSes = 1
            twoShockBlock = 2
        else:
            # print('Session 2 block 1 will have two shocks')
            twoShockSes = 2
            twoShockBlock = 1

        if SessID == twoShockSes and blockID == twoShockBlock:
            trials = [CSplus_1]*2+[CSplus_2]*3+[CSminus]*3
        else:
            trials = [CSplus_1]+[CSplus_2]*3+[CSminus]*3
        run_block(SessID, blockID, curBlock,trials,trialFilename,randCond, T0)

    # pause between blocks
    # if ii < len(blocks) -1:
    #    imName = _thisDir + os.sep + 'stim' + os.sep + 'pause_s.jpg'
    #    showImage = visual.ImageStim(win, image=imName,pos=[0, 0])
    #    escDown = None
    #    timer = core.Clock()
    #    timer.add(10)
    #    while timer.getTime() < 0 and escDown is None:
    #        escDown = get_keypress()
    #        if escDown is not None:
    #            shutdown()
    #        showImage.draw()
    #        win.flip()       # present the instruction for resting

# show thanks and goodbye
send_code(1)                          # End of the experiment, send two codes
text_msg("Vielen Dank", [0, 0],50)
win.flip()
core.wait(1)

# exit
shutdown()
