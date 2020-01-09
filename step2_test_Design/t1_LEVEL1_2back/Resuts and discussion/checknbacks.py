#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Aug 30 21:29:29 2018

Name: function -startTrial(block,exp)

@author: kishore, 217BM1284, MEI LAB, NITR
Project: Biosignal Processing (EEG and Cognition)
"""
#fN3 ---------------startTrial(Block,exp)
from expyriment import stimuli, misc   #design,control, io,
def startTrial(b,exp):
    numelTrial=len(b.trials)
    print(numelTrial)
    mem=[0,0,0]
    response_key = [misc.constants.K_SPACE]

    hit,miss,incorrect_=0,0,0 #for final correct and incorrect responsed
    for b in exp.blocks:
        #------------monitoring variables
        Ncount=0 # counting nbacks in  the block && reset Ncount for next block
        totcount,memcount=0,0
        n_mem = numelTrial-3+1 # since 121
        #keyprflag=1 #flag intially set
        #----------monitoring variables...[end]
        #leftovertime=0

        for t in b.trials:
            keyprflag=1 # flag initially set
            memcount+=1
            #t.stimuli[0].preload()
            fixcross = stimuli.FixCross(size=(40,40),colour=misc.constants.C_WHITE)
            fixcross.present()
            exp.clock.wait(500)#-t.stimuli[0].preload) #remove #
            t.stimuli[0].present()  # Presenting the stimulus onscreen

            if memcount==1 or memcount==2: #no need of key_response
                """rt=exp.keyboard.wait(keys=response_key,duration=3000) #remove #
                try:
                    leftovertime=3000-rt[1]   #LEFT OVER TIME AFTER KEYPRESS ::ADJUST TIME FOR NEXT STIMULI
                    print(leftovertime)
                    exp.clock.wait(leftovertime)
                except:
                    print(None)"""
                exp.clock.wait(3000)

            if memcount == 1:
                mem[0]=t.factor_dict['COLOR']
                keyprflag=0
                #print(mem[0])
                #mem[0]=t.stimuli[0]
            if memcount == 2:
                mem[1]=t.factor_dict['COLOR']#t.stimuli[0]
                keyprflag=0

            if memcount == 3:
                mem[2]=t.factor_dict['COLOR']

                memcount=2
                n_mem-=1
                # 3 memories here
                #print(mem)

                #...CHECKING nback or not...[start]
                if mem[0]==mem[2]:  #Counting nback in stimuli
                    Ncount+=1
                    nbackoccured=True
                else:
                    nbackoccured=False #.....CHECK COMPLETE

                #if keyprflag==1:
                #    keyprflag=0
                    #print("keyprflag reset") #remove#
                rt=exp.keyboard.wait(keys=response_key,duration=3000) #remove #

                if rt[0]!=None:
                    #print("keyprflag set") #remove#
                    keyprflag=1
                    leftovertime=3000-rt[1]   #LEFT OVER TIME AFTER KEYPRESS <ADJUST TIME FOR NEXT STIMULI>
                    exp.clock.wait(leftovertime)
                    #print(rt)
                    #print(leftovertime)
                else:
                    keyprflag=0

                if nbackoccured==True and keyprflag==1:
                    print('HIT')
                    keyprflag=0
                    hit+=1
                elif nbackoccured==True and keyprflag==0:
                    print('MISS')
                    miss+=1
                elif nbackoccured==False:
                    print(-1)
                    if keyprflag==1:
                        print('incorrect')
                        incorrect_+=1
                 #   keyprflag=0 #reset flag
                #...compare...[end]
                print(mem) # put#
                if n_mem != 0:
                    mem[0]=mem[1]
                    mem[1]=mem[2] #b is a list

    #Evaluating % correct
    print("***RESULT: -------------\n*** -H:" + str(hit) + "->M:" + str(miss) + "-> I:" + str(incorrect_))
    correctpercent = hit/(hit+incorrect_+miss) * 100
    #incorrectpercent=incorrect
    print("*** fN startTrial: nbacks = %d nos."%Ncount)
    #print("*** %d % Correct"%correctpercent)
    print("*** Correct "+str(correctpercent)+"% \n----------------------[trial end]")
