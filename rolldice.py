#!/usr/bin/env python3

import sys
import re
import itertools
import numpy as np


class DiceSet:
    """Class containing dice request and results"""
    
    def __init__(self, cmd):
        """Constructeur de classe DiceSet."""
        
        #Initializing data structure
        self.cmd = cmd
        self.rolls = {'dice':[],
                      'mods':[]}
        
        #parsing self.cmd is done in __init__, will move it later
        diceRegex = r"(?i)^(?P<die>(?P<dCount>\d+)d(?P<dType>\d+))?$"
        modRegex = r"(?i)^(?P<mod>[\+\-]\d+)?$"
        
        for substring in self.cmd:          
            #let's first evaluate the rolls 
            diceMatch = re.match(diceRegex, substring)
            modMatch = re.match(modRegex, substring)
            
            if diceMatch is not None:
                self.rolls['dice'] += [{"type":int(diceMatch.group("dType")),
                                  'roll':np.random.randint(1, diceMatch.group("dType"))} 
                                  for d in range(int(diceMatch.group("dCount")))]

            if modMatch is not None:
                self.rolls['mods'].append(int(modMatch.group("mod")))

        self.rolls['total'] = self.calculateTotal()
        self.stats = self.calculateStats()
    
    def calculateTotal(self):
        return sum([d['roll'] for d in self.rolls['dice']]) + sum(self.rolls['mods'])
    
    def calculateStats(self):
        return {
            "min": sum([1 for die in self.rolls['dice']]) + sum(self.rolls["mods"]),
            "median": sum([die["type"]/2 for die in self.rolls["dice"]]) + sum(self.rolls["mods"]),
            "max": sum([die["type"] for die in self.rolls["dice"]]) + sum(self.rolls["mods"])
        }
    
    def getResult(self):
        """Accessor for a TL,DR dice roll info"""
        print(self.rolls['total'])
        
    def getVerboseResult(self):
        """Accessor for detailed roll information"""
        def pprintModifiers(rolls):
            return "".join(["{:+}".format(i) for i in rolls['mods']])
        def pprintDiceRolls(rolls):
            return "".join(["{:+}".format(dice['roll']) for dice in rolls['dice']])[1:]

        if len(self.rolls['mods']) == 0:
            print('Request:\t{} \nAll Rolls:\t{} \nTotal Result:\t{}'.format(
                d.cmd,
                pprintDiceRolls(self.rolls),
                self.rolls['total']))
        else:
            print('Request:\t{} \nAll Rolls:\t{} ({})\nTotal Result:\t{}'.format(
                d.cmd,
                pprintDiceRolls(self.rolls),
                pprintModifiers(self.rolls),
                self.rolls['total']))

    def getStats(self):
        """Accessor for dice set stats"""
        print("Min:\t\t{}\nMedian:\t\t{}\nMax:\t\t{}".format(self.stats["min"], self.stats["median"],self.stats["max"]))

d = DiceSet(sys.argv[1:])

d.getVerboseResult()
d.getStats()