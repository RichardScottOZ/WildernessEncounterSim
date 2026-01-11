#!/usr/bin/env python3
"""
Dice group for random rolls.

@author   Daniel R. Collins (dcollins@superdan.net)
@since    2014-05-20
@version  1.4
Ported to Python by GitHub Copilot
"""

import random
import re


class Dice:
    """Class representing a group of dice with modifiers."""
    
    # Class-level random generator
    _random = None
    
    def __init__(self, *args):
        """
        Constructor with multiple signatures:
        - Dice(sides): one die with given sides
        - Dice(num, sides): number of dice with given sides
        - Dice(num, sides, add): with addition modifier
        - Dice(num, sides, mul, add): with all modifiers
        - Dice(string): parse from dice notation string
        """
        if len(args) == 1:
            if isinstance(args[0], str):
                # Constructor from string
                self._parse_string(args[0])
            else:
                # One die only
                self.number = 1
                self.sides = args[0]
                self.multiplier = 1
                self.addition = 0
        elif len(args) == 2:
            self.number = args[0]
            self.sides = args[1]
            self.multiplier = 1
            self.addition = 0
        elif len(args) == 3:
            self.number = args[0]
            self.sides = args[1]
            self.multiplier = 1
            self.addition = args[2]
        elif len(args) == 4:
            self.number = args[0]
            self.sides = args[1]
            self.multiplier = args[2]
            self.addition = args[3]
        else:
            self.number = 0
            self.sides = 0
            self.multiplier = 1
            self.addition = 0
    
    def _parse_string(self, s):
        """
        Parse dice notation string.
        RegEx code from @user1803551 on StackExchange:
        http://stackoverflow.com/questions/35020687/
        how-to-parse-dice-notation-with-a-java-regular-expression
        """
        self.number = 0
        self.sides = 0
        self.multiplier = 1
        self.addition = 0
        
        pattern = re.compile(r'([1-9]\d*)?d([1-9]\d*)([/x][1-9]\d*)?([+-]\d+)?')
        m = pattern.match(s)
        
        if m:
            self.number = int(m.group(1)) if m.group(1) else 1
            self.sides = int(m.group(2))
            
            if m.group(3):
                positive = m.group(3).startswith('x')
                val = int(m.group(3)[1:])
                self.multiplier = val if positive else -val
            
            if m.group(4):
                positive = m.group(4).startswith('+')
                val = int(m.group(4)[1:])
                self.addition = val if positive else -val
        else:
            # Accept a constant number (no "d")
            try:
                self.addition = int(s)
            except ValueError:
                self.addition = 0
    
    @classmethod
    def initialize(cls):
        """Initialize the dice random generator."""
        cls._random = random.Random()
    
    @classmethod
    def roll(cls, sides):
        """
        Roll one die from a static context.
        @return The die-roll.
        """
        if cls._random is None:
            cls.initialize()
        return cls._random.randint(1, sides)
    
    def _adjust_roll(self, roll):
        """
        Apply adjustments after raw dice roll.
        @return Roll after modifiers.
        """
        if self.multiplier >= 0:
            roll *= self.multiplier
        else:
            roll = (roll - 1) // (-self.multiplier) + 1
        roll += self.addition
        return roll
    
    def roll_dice(self):
        """
        Rolls the dice.
        @return The dice-roll.
        """
        total = 0
        for _ in range(self.number):
            total += Dice.roll(self.sides)
        return self._adjust_roll(total)
    
    def bound_roll(self, floor):
        """
        Rolls the dice with specified floor.
        @return The bounded dice-roll.
        """
        return max(self.roll_dice(), floor)
    
    def min_roll(self):
        """
        Compute the minimum possible roll.
        @return Minimum possible roll.
        """
        return self._adjust_roll(self.number)
    
    def max_roll(self):
        """
        Compute the maximum possible roll.
        @return Maximum possible roll.
        """
        return self._adjust_roll(self.number * self.sides)
    
    def avg_roll(self):
        """
        Compute average roll.
        @return Average roll.
        """
        return (self.min_roll() + self.max_roll()) // 2
    
    def modify_add(self, mod):
        """Modify the addition field."""
        self.addition += mod
    
    def __str__(self):
        """Identify this object as a string."""
        if self.number > 0:
            s = f"{self.number}d{self.sides}"
            if self.multiplier != 1:
                s += self._format_multiplier(self.multiplier)
            if self.addition != 0:
                s += self._format_bonus(self.addition)
            return s
        else:
            return str(self.addition)
    
    @staticmethod
    def _format_bonus(bonus):
        """Format additive bonus with sign."""
        return f"+{bonus}" if bonus >= 0 else str(bonus)
    
    @staticmethod
    def _format_multiplier(mult):
        """Format multiplicative bonus with sign."""
        return f"x{mult}" if mult >= 0 else f"/{-mult}"


# Initialize on module load
Dice.initialize()
