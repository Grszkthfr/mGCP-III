# !/usr/bin/env python
# -*- coding: utf-8 -*- #

### (PsychoPy) Libraries

import os, csv, random, itertools, datetime
from psychopy import visual, core, event, gui  # PsychoPy Libraries (5/20)


### Setup
### Experiment text modules

experimentName = "mGCP-II"

eveText = ""
welcomeText = u"Herzlich Willkommen!\n\nVielen Dank, dass Sie heute an unserem Versuch zur Aufmerksamkeitsverteilung teilnehmen. Sie helfen uns damit sehr weiter, denn Sie sind ein wichtiger Teil unserer Studie.\nBitte bearbeiten Sie den Versuch so konzentriert und gewissenhaft wie möglich.\n\n\n\t\t\t\t\t\tWeiter mit der <Leertaste>"

instructionText1 = u"Der Versuch besteht aus vier Durchgängen á vier Minuten. Zwischendurch gibt es kleine Pausen.\n\nZuerst legen Sie bitte den Zeigefinger und den Mittelfinger Ihrer dominanten Hand auf die markierten Tasten der Tastatur.\n\nLassen Sie die Finger für die Dauer des Versuchs dort.\n\n\n\t\t\t\t\t\tWeiter mit der <Leertaste>"

instructionText2 = u"Zu Beginn eines Durchganges fixieren Sie bitte das Fixationskreuz.\n\nKurz darauf werden Ihnen Gesichter präsentiert.\n\nAnschließend erscheint ein Buchstabe auf der rechten oder linken Bildschirmhälfte.\n\n\n\t\t\t\t\t\tWeiter mit der <Leertaste>"

instructionText3 = u"Erscheint ein \tE\t drücken Sie bitte die Taste, die mit dem \"E\" gekennzeichnet ist.\n\nErscheint ein \tF\t drücken Sie bitte die Taste, die mit dem \"F\" gekennzeichnet ist.\n______________________________________________________\n\nReagieren Sie bitte so schnell und so sorgfältig wie möglich. Es ist wichtig, dass Sie nach jedem Trial wieder das Fixationskreuz fixieren.\n\nWenn Sie noch Fragen haben wenden Sie sich bitte jetzt an den Versuchsleiter.\n\nWenn Sie alles verstanden haben können Sie den Versuch mit der <Leertaste> starten.\n\nViel Spaß."

warningText = u"Bitte schneller reagieren."

pauseText = u"Pause! Denken Sie daran, weiterhin nach jedem Trial den Blick auf dem Fixationskreuz zu halten.\n\n\nVersuch fortsetzen mit der <Leertaste>"

goodbyeText = u"Fast geschafft!\n\nBitte geben Sie dem Versuchsleiter ein Zeichen, dann erhalten Sie noch ein paar kurze Fragebögen.\n\n\nVielen Dank!"


### Experimental characteristics

expInfo = {'subject': ''}
interStimuliIntervall = .500  # interstimuli Intervall in seconds, time between appearance of cue and target
maxResponseTime = .800  # maximale time to respond to target in seconds
interTrialIntervall = (0.75, 1.25)  # time in seconds between two trials, from ... to, jitter is generated
minReadingTime = 2  # mimimum time text will be presented

responseKeyE = 'u' # response key for "E"
responseKeyF = 'n' # response key for "F"
continueKey = "space" # continue key for instructions
quitKey = "q" # exit key for experiment at any given time


### Experperimental prerequisites

cueDirectory = 'stimuli' + os.path.sep + 'cues'
trialList3 = []
trialList1 = []
trialCounter = 1  # trial counter starting at 1
blockCounter = 1 # block counter starting at 1

window = ""
myText = ""  # required for showText-Funciton


### Functions
### General functions

def wait(seconds):
    try:
        number = float(seconds); core.wait(number, number)  # Wait presentationTime seconds. Maximum accuracy (2nd parameter) is used all the time (i.e. presentationTime seconds).
    except TypeError:
        jitter = random.random() * (seconds[1] - seconds[0]) + seconds[0];
        core.wait(jitter, jitter)
        ##print "Jitter: %.3f sec" %(jitter); #to control for correctness


def getTimestamp(time, format='%Y-%m-%d %H:%M:%S'):
    timeNowString = datetime.datetime.fromtimestamp(time).strftime(format)
    return timeNowString


def getTimestampNow(format='%Y-%m-%d_%H:%M'):
    return getTimestamp(core.getAbsTime(), format)


### Specific functions

def prepare():
    global window
    while True:
        input = gui.DlgFromDict(dictionary=expInfo, title=experimentName)
        if input.OK == False: core.quit()  # user pressed cancel
        if (expInfo[
                'subject'] != ''): break  # if Subject field wasn't specified, display Input-Window again (i.e. don't break the loop)
    # if (expInfo['key Assignment'] != 1): keyAssignment = 0 #keyAssignment = 1: target category1 <=> responseKey1
    # if (keyAssignment == 1): instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key1>", responseKey1.upper()); instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key2>", responseKey2.upper())
    # else: instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key1>", responseKey2.upper()); instructionKeyAssignmentText = instructionKeyAssignmentText.replace("<key2>", responseKey1.upper())

    window = visual.Window([800, 600], monitor="Office207", fullscr=False) # prepare a window for the experiment with resolution and specified monitor
    event.Mouse(visible=False)


def fillList(path):
    faceList = []
    for file in os.listdir(path):
        if file.lower().endswith(
                ".jpg"):  ##or file.lower().endswith(".png") or file.lower().endswith(".gif") or file.lower().endswith(".tif") or file.lower().endswith(".bmp"):
            faceList.append(os.path.join(path, file))  # If the file is an image file, add its relative path STARTING IN THE WORKING DIRECTORY to list of targets
    return faceList

            #RICHTIG: 0: pic_left, 1: pic_top, 2: pic_right, 3: left_cue, 4: target_E, 5: target_left, 6: congruency, 7: number_of_cues
def writeTrialToFile(left_image, top_image, right_image, left, target, targetPos, congruency, number_of_cues, correct, RT):
    # check if file and folder already exist
    if not os.path.isdir('data/raw'):
        os.makedirs('data/raw')  # if this fails (e.g. permissions) you will get an error
    fileName = 'data/raw' + os.path.sep + experimentName + '_' + expInfo['subject'] + '.csv'  # generate file name with name of the experiment and subject

    # open file
    with open(fileName, 'ab') as saveFile:  # 'a' = append; 'w' = writing; 'b' = in binary mode
        fileWriter = csv.writer(saveFile, delimiter=',')  # generate fileWriter
        if os.stat(fileName).st_size == 0:  # if file is empty, insert header
            fileWriter.writerow(('expName', 'subject', 'date', 'block', 'trial', 'left_face', 'top_face', 'right_face', 'left_cue', 'target_E', 'target_left', 'congruency', 'number_of_cues', 'correct_response', 'rt'))

        # write trial
        fileWriter.writerow((experimentName, expInfo['subject'], getTimestampNow(), blockCounter, trialCounter, left_image, top_image, right_image, left, target, targetPos, congruency, number_of_cues, correct, RT))

        '''
        print experimentName
        print VP
        print block
        print trial
        print left_image
        print top_image
        print right_image
        print left
        print target
        print targetPos
        print gazes
        print correct
        print RT
        '''


def showText(window, myText):
    message = visual.TextStim(window, text=myText, height=0.05)
    message.draw()
    window.flip()
    wait(minReadingTime)
    event.clearEvents()
    while True:  # Participant decides when to proceed
        if event.getKeys(continueKey):
            break
        if event.getKeys(quitKey):
            core.quit()

            #RICHTIG wäre: 0: pic_left, 1: pic_top, 2: pic_right, 3: left_cue, 4: target_E, 5: target_left, 6: congruency, 7: number_of_cues
def showTrial(left_face, top_face, right_face, left, target, congruency, targetPos, number_of_cues):  

    # Preparation
    FixationCross = visual.TextStim(window, text=u"+", font='Arial', pos=[0, 0], height=30, units=u'pix', color='white')
    SlowWarning = visual.TextStim(window, text=warningText, font='Arial', pos=[0, 0], height=30, units=u'pix', color='white')

    # target & position
    if (target == '1'):  # target E
        correctKey = responseKeyE
        wrongKey = responseKeyF
        if (targetPos == '1'):  # target left
            Target = visual.TextStim(window, text='E', font='Arial', pos=[-.65, 0])
            ##print '1'
        elif (targetPos == '0'):  # target right
            Target = visual.TextStim(window, text='E', font='Arial', pos=[.65, 0])
            ##print '2'
        else:
            print '>>> Error target E needs to be somewhere!!'
    elif (target == '0'):  # target F
        correctKey = responseKeyF
        wrongKey = responseKeyE
        if (targetPos == '1'):  # target left
            Target = visual.TextStim(window, text='F', font='Arial', pos=[-.65, 0])
            ##print '3'
        elif (targetPos == '0'):  # target right
            Target = visual.TextStim(window, text='F', font='Arial', pos=[.65, 0])
            ##print '4'
        else:
            print '>>> Error target F needs to be somewhere!'
    else:
        print '>>> Error, target needs to be something! ' + target

    reactionTime = core.Clock()
    FixationCross = visual.TextStim(window, text=u"+", font='Arial', pos=[0, 0], height=30, units=u'pix', color='white')
    FixationCross.draw()
    window.flip()
    wait(interTrialIntervall)  # show fixationCross interTrialIntervall-seconds prior to beginning
    FixationCross.draw()

    if (number_of_cues == '3'):
        LeftImage = visual.ImageStim(window, units='cm', size=(75, 100), pos=(-60.622, -35))  # size in mm
        # TopImage = visual.ImageStim(window, units= 'norm', size = (0.28125,0.5), pos = (0, 0.5))
        TopImage = visual.ImageStim(window, units='cm', size=(75, 100), pos=(0, 70))
        RightImage = visual.ImageStim(window, units='cm', size=(75, 100), pos=(60.622, -35))

        LeftImage.setImage(left_face)
        LeftImage.draw()

        TopImage.setImage(top_face)
        TopImage.draw()

        RightImage.setImage(right_face)
        RightImage.draw()

    elif (number_of_cues == '1'): 
        CentralImage = visual.ImageStim(window, units='cm', size=(75,100),pos=(0, 0))
        CentralImage.setImage(top_face) # Take top-picture as central cue.
        CentralImage.draw()

    else:
        print "neither central nor triple cue?!"

    window.flip() # draw all faces
    wait(interStimuliIntervall) # wait interStimuliIntervall milliseconds

    if (number_of_cues == '3'):
        LeftImage.draw()
        TopImage.draw()
        RightImage.draw()
        FixationCross.draw() #fixation cross remains visible


    elif (number_of_cues == '1'):
        CentralImage.draw()

    else:
        print "Error after Target onset!"

    Target.draw() # draw/prepare target
    # FixationCross.draw() # show fixation cross during target presentation

    window.flip() # flip all faces with target
    reactionTime.reset() # reaction time resets
    event.clearEvents()

    while (reactionTime.getTime() <= maxResponseTime): # Participant decides when to proceed, after onset of target!
        if event.getKeys(correctKey):
            correctResponse = 1
            RT = reactionTime.getTime()
            ##print 'correct'
            ##print reactionTime.getTime()
            break

        elif event.getKeys(wrongKey):
            correctResponse = 0
            RT = reactionTime.getTime()
            ##print 'NOT correct'
            ##print reactionTime.getTime()
            break

        if event.getKeys(quitKey):
            print 'quit'
            core.quit()

    while (reactionTime.getTime() > maxResponseTime):  # after maxResponseTime runs out
        if (event.getKeys(correctKey)) or (event.getKeys(wrongKey)):
            correctResponse = 99
            RT = 99

            SlowWarning.draw()
            window.flip()
            wait(1.5)

            break
        if event.getKeys(quitKey):
            print 'quit'
            core.quit()
    #print blockCounter, ' ', trialCounter, ' ', left, targetPos, congruency, str(correctResponse), ' ', str(RT)

    # print what is returned to writeTrialToFile-Function
    ##print left_face.split('\\')[-1], top_face.split('\\')[-1], right_face.split('\\')[-1], target, targetPos, correctResponse, RT)

#RICHTIG wäre: 0: pic_left, 1: pic_top, 2: pic_right, 3: left_cue, 4: target_E, 5: target_left, 6: congruency, 7: number_of_cues
    return writeTrialToFile(left_face.split('Rafd090_')[-1], top_face.split('Rafd090_')[-1], right_face.split('Rafd090_')[-1], left, target, targetPos, congruency, number_of_cues, correctResponse, RT)


def MakeTrialList3(path):

    # get a list with faces from directory
    temporaryTrialList = fillList(path)

    # complete list with faces with permutations in combination of three BUT still left-right cues included as identical faces in single trial!
    temporaryTrialList = list(itertools.permutations(temporaryTrialList, 3))

    for i in range(len(temporaryTrialList)):
        ##for j in range(len(temporaryTrialList[i])):
        x = ','.join(map(str, temporaryTrialList[i]))
        #print x

        # Exclude, two different directional cues in a single trial, and single faces appearing multiple times
        if not ('left' in x and 'right' in x):

            # coding trials
            if 'left' in x:

                # How many gaze cues by counting the appearance of the words "left" and "right"?
                number_of_cues = temporaryTrialList[i][0].count('left')
                number_of_cues += temporaryTrialList[i][1].count('left')
                number_of_cues += temporaryTrialList[i][2].count('left')

                #left_cue: yes, target_E: yes, target_left: yes, congruency: yes, number_of_cues: 3
                x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '1', '1', str(number_of_cues)

                # left_cue: yes, target_E: yes, target_left: no, congruency: no, number_of_cues: 3
                x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '1', '0', '0', str(number_of_cues)  

                # left_cue: yes, target_E: no, target_left: yes, congruency: yes, number_of_cues: 3
                x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '1', '1', str(number_of_cues)  

                # left_cue: yes, target_E: no, target_left: no, congruency: no, number_of_cues: 3
                x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '1', '0', '0', '0', str(number_of_cues)  

                if number_of_cues == 3:  # without there would only 96 trials (against 288 in the other conditions)
                    trialList3.append(x1)
                    trialList3.append(x2)
                    trialList3.append(x3)
                    trialList3.append(x4)

            elif 'right' in x:

                # How many gaze cues?
                number_of_cues= temporaryTrialList[i][0].count('right')
                number_of_cues += temporaryTrialList[i][1].count('right')
                number_of_cues += temporaryTrialList[i][2].count('right')

                # left_cue: no, target_E: yes, target_left: yes, congruency: no, number_of_cues: 3 
                x1 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', '1', '1', '0', str(number_of_cues) 

                x2 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', '1', '0', '1', str(number_of_cues)

                x3 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', '0', '1', '0', str(number_of_cues)
###FEHLER:
                x4 = temporaryTrialList[i][0], temporaryTrialList[i][1], temporaryTrialList[i][2], '0', '0', '0', '0', str(number_of_cues)

                if number_of_cues == 3:  # without there would only 96 trials (against 288 in the other conditions)
                    trialList3.append(x1)
                    trialList3.append(x2)
                    trialList3.append(x3)
                    trialList3.append(x4)

    # Check number of Trials
    testCues3 = 0
    for i in range(len(trialList3)):
        if trialList3[i][7] == '3':
            testCues3 += 1
        else:
            print "WTF @ testCues3?!"

    # Check number of Trials
    testCong3 = 0
    testIncong3 = 0
    for i in range(len(trialList3)):
        if trialList3[i][6] == '1':
            testCong3 += 1
        else:
            testIncong3 += 1

    # Check number of Trials
    testTarLeft3 = 0
    testTarRight3 = 0
    for i in range(len(trialList3)):
        if trialList3[i][5] == '1':
            testTarLeft3 += 1
        else:
            testTarRight3 += 1

    # Check number of Trials
    testCueLeft3 = 0
    testCueRight3 = 0
    for i in range(len(trialList3)):
        if trialList3[i][4] == '1':
            testCueLeft3 += 1
        else:
            testCueRight3 += 1

    print '3 Trials with three gaze cue: ', testCues3, ' of 48 trials'
    print '3 Trials with congruent trials: ', testCong3, ' of 24 congruent trials , ', testIncong3, ' of 24 incongruent trials.'
    print '3 Trials with target left: ', testTarLeft3, ' of 24 target-left trials, ', testTarRight3, ' of 24 target-right trials.'
    print '3 Trials with cue left: ', testCueLeft3, ' of 24 cue-left trials, ', testCueRight3, ' of 24 cue-right trials.'

    return trialList3

def MakeTrialList1(path):
    # get a list with female faces from directory
    temporaryTrialList = fillList(path)
    temporaryTrialList = list(itertools.permutations(temporaryTrialList, 1))

    for i in range(len(temporaryTrialList)):
        ##for j in range(len(temporaryTrialList[i])):
        x = ','.join(map(str, temporaryTrialList[i]))
        print x

        # coding trials
        if 'left' in x:

            #0: pic_left, 1: pic_top, 2: pic_right, 3: left_cue: yes, 4: target_E: yes, 5: target_left: yes, 6: congruency: yes, 7: number_of_cues: 1
            x1 = '99', temporaryTrialList[i][0], '99', '1', '1', '1', '1', '1'

            # left_cue: yes, target_E: yes, target_left: no, congruency: no, number_of_cues: 1
            x2 = '99', temporaryTrialList[i][0], '99', '1', '1', '0', '0', '1'  

            # left_cue: yes, target_E: no, target_left: yes, congruency: yes, number_of_cues: 1
            x3 = '99', temporaryTrialList[i][0], '99', '1', '0', '1', '1', '1'  

            # left_cue: yes, target_E: no, target_left: no, congruency: no, number_of_cues: 1
            x4 = '99', temporaryTrialList[i][0], '99', '1', '0', '0', '0', '1'  

            trialList1.append(x1)
            trialList1.append(x2)
            trialList1.append(x3)
            trialList1.append(x4)
            
            trialList1.append(x1)
            trialList1.append(x2)
            trialList1.append(x3)
            trialList1.append(x4)

        elif 'right' in x:

            # left_cue: no, target_E: yes, target_left: yes, congruency: no, number_of_cues: 3 
            x1 = '99',temporaryTrialList[i][0],  '99', '0', '1', '1', '0', '1'

            x2 = '99', temporaryTrialList[i][0], '99', '0', '1', '0', '1', '1'

            x3 = '99', temporaryTrialList[i][0], '99', '0', '0', '1', '0', '1'
###FEHLER:
            x4 = '99', temporaryTrialList[i][0], '99', '0', '0', '0', '0', '1'

            trialList1.append(x1)
            trialList1.append(x2)
            trialList1.append(x3)
            trialList1.append(x4)
            
            trialList1.append(x1)
            trialList1.append(x2)
            trialList1.append(x3)
            trialList1.append(x4)

    # Check number of Trials                
    testCues1 = 0
    for i in range(len(trialList1)):
        if trialList1[i][7] == '1':
            testCues1 += 1
        else:
            print "WTF @ testCues1?!"
            

    # Check number of Trials                
    testCong1 = 0
    testIncong1 = 0
    for i in range(len(trialList1)):
        if trialList1[i][6] == '1':
            testCong1 += 1
        else:
            testIncong1 += 1
            

    # Check number of Trials                
    testTarLeft1 = 0
    testTarRight1 = 0
    for i in range(len(trialList1)):
        if trialList1[i][5] == '1':
            testTarLeft1 += 1
        else:
            testTarRight1 += 1

    # Check number of Trials                
    testCueLeft1 = 0
    testCueRight1 = 0
    for i in range(len(trialList1)):
        if trialList1[i][4] == '1':
            testCueLeft1 += 1
        else:
            testCueRight1 += 1

    print '1 Trials with one gaze cue: ', testCues1, ' of 48 trials.'
    print '1 Trials with congruent trials: ', testCong1, ' of 24 congruent trials , ', testIncong1, ' of 24 incongruent trials.'
    print '1 Trials with target left: ', testTarLeft1, ' of 24 target-left trials, ', testTarRight1, ' of 24 target-right trials.'
    print '1 Trials with cue left: ', testCueLeft1, ' of 24 cue-left trials, ', testCueRight1, ' of 24 cue-right trials.'


    return trialList1


def TrialFromTrialListPicker(i):

    # bei geraden VP nummern
    if float(expInfo['subject']) % 2 == 1:

        if blockCounter == 1:
            #0: pic_left, 1: pic_top, 2: pic_right, 3: left_cue: yes, 4: target_E: yes, 5: target_left: yes, 6: congruency: yes, 7: number_of_cues: 1
            return showTrial(trialList3[i][0], trialList3[i][1], trialList3[i][2], trialList3[i][3], trialList3[i][4], trialList3[i][5], trialList3[i][6], trialList3[i][7])
        
        elif blockCounter == 2:
            return showTrial(trialList1[i][0], trialList1[i][1], trialList1[i][2], trialList1[i][3], trialList1[i][4], trialList1[i][5], trialList1[i][6], trialList1[i][7])
        
        elif blockCounter == 3:
            return showTrial(trialList3[i][0], trialList3[i][1], trialList3[i][2], trialList3[i][3], trialList3[i][4], trialList3[i][5], trialList3[i][6], trialList3[i][7])
        
        elif blockCounter == 4:
            return showTrial(trialList1[i][0], trialList1[i][1], trialList1[i][2], trialList1[i][3], trialList1[i][4], trialList1[i][5], trialList1[i][6], trialList1[i][7])

        else:
            print "Error no triallist picked for odd subject id"

    elif float(expInfo['subject']) % 2 == 0:

        if blockCounter == 1:

            #0: pic_left, 1: pic_top, 2: pic_right, 3: left_cue: yes, 4: target_E: yes, 5: target_left: yes, 6: congruency: yes, 7: number_of_cues: 1
            return showTrial(trialList1[i][0], trialList1[i][1], trialList1[i][2], trialList1[i][3], trialList1[i][4], trialList1[i][5], trialList1[i][6], trialList1[i][7])

        elif blockCounter == 2:
            return showTrial(trialList3[i][0], trialList3[i][1], trialList3[i][2], trialList3[i][3], trialList3[i][4], trialList3[i][5], trialList3[i][6], trialList3[i][7])

        elif blockCounter == 3:
            return showTrial(trialList1[i][0], trialList1[i][1], trialList1[i][2], trialList1[i][3], trialList1[i][4], trialList1[i][5], trialList1[i][6], trialList1[i][7])

        elif blockCounter == 4:
            return showTrial(trialList3[i][0], trialList3[i][1], trialList3[i][2], trialList3[i][3], trialList3[i][4], trialList3[i][5], trialList3[i][6], trialList3[i][7])
        else:
            print "Error no triallist picked for even subject id"
    else:
        print expInfo['subject'], "Error subject id not even/odd!"


def Block(trials1, trials3, randomize=True):
    global trialCounter, blockCounter

    while blockCounter <= 4:
        
        if len(trials1) == len(trials3):
            #for i in [1,2,3,4]: #for testing
            for i in range(len(trials1)):  # for each trial, go to trialPicker, add +1 for Trialcounter
                if (randomize):
                    random.shuffle(trials1)
                    random.shuffle(trials3)
                                        
                TrialFromTrialListPicker(i)  # run trial i
                print '> trialCounter: ', trialCounter
                trialCounter += 1
                

        else: 
            print "Triallist of unequal length!"

        blockCounter += 1

        if (blockCounter < 5):
            showText(window, pauseText)
            print '>>> blockCounter: ', blockCounter


def run():
    
    trialList3 = MakeTrialList3(cueDirectory)
    trialList1 = MakeTrialList1(cueDirectory)

    prepare()
    print [expInfo['subject']]

    showText(window, eveText)
    showText(window, welcomeText)
    showText(window, instructionText1)
    showText(window, instructionText2)
    showText(window, instructionText3)

    writeTriallistToFile(trialList1)
    writeTriallistToFile(trialList3)


    Block(trialList1, trialList3)

    showText(window, goodbyeText)

    # Closing Section
    window.close()
    core.quit()

def writeTriallistToFile(listOfTrials):
    #if not os.path.isdir('triallist'): #exist the path?! if not...
    #    os.makedirs('triallist')
    fileName = 'triallist' + '.csv'

    with open(fileName, 'ab') as saveFile: #'a' = append; 'w' = writing; 'b' = in binary mode
        fileWriter = csv.writer(saveFile, delimiter=',')
        if os.stat(fileName).st_size == 0: #if file is empty, insert header
            fileWriter.writerow(('pic_left', 'pic_top', 'pic_right', 'left_cue', 'target_E', 'target_left', 'congruency', 'number_of_cues')) #1=ja
        for i in range(len(listOfTrials)):
            fileWriter.writerow(listOfTrials[i])

 #0: pic_left, 1: pic_top, 2: pic_right, 3: left_cue: yes, 4: target_E: yes, 5: target_left: yes, 6: congruency: yes, 7: number_of_cues: 1

run()



