#!/usr/bin/env python3
"""
Simulator for OD&D wilderness encounters.

@author   Daniel R. Collins (dcollins@superdan.net)
@since    2021-12-05
Ported to Python by GitHub Copilot
"""

import sys
import os
from dice import Dice
from table import Table


class WildernessEncounterSim:
    """Wilderness encounter simulator."""
    
    # Constants
    NUM_ENCOUNTERS = 1000
    MONSTER_NUM_COL = 1
    MONSTER_HDN_COL = 12
    MONSTER_EHD_COL = 13
    
    def __init__(self):
        """Constructor."""
        Dice.initialize()
        
        # Load tables from CSV files
        # Adjust paths to be relative to script location
        script_dir = os.path.dirname(os.path.abspath(__file__))
        parent_dir = os.path.dirname(script_dir)
        
        self.main_table = Table(os.path.join(parent_dir, "WildMainTable.csv"))
        self.sub_table = Table(os.path.join(parent_dir, "WildSubTable.csv"))
        self.monster_table = Table(os.path.join(parent_dir, "MonsterDatabase.csv"))
        
        self.terrain = None
        self.terrain_index = None
        self.exit_after_args = False
    
    def print_banner(self):
        """Print program banner."""
        print("OED Wilderness Encounter Simulator")
        print("----------------------------------")
    
    def print_usage(self):
        """Print usage."""
        print("Usage: WildernessEncounterSim.py terrain")
        print()
    
    def parse_args(self, args):
        """
        Parse arguments.
        @param args Command line arguments (excluding script name)
        """
        if len(args) != 1:
            self.exit_after_args = True
        else:
            self.terrain = args[0]
            self.terrain_index = self.main_table.get_col_from_name(self.terrain)
            if self.terrain_index < 1:
                print(f"Unknown terrain: {self.terrain}", file=sys.stderr)
                self.exit_after_args = True
    
    def sub_table_fixup(self, table, sub):
        """
        Special fixups to determine exact subtable.
        @param table Terrain name
        @param sub Subtable name
        @return Fixed subtable name
        """
        # Find men subtable by terrain
        if sub == "Men":
            if table == "Mountain":
                return "Men Mountain"
            if table == "Desert":
                return "Men Desert"
            if table == "River":
                return "Men Water"
            return "Men Typical"
        return sub
    
    def monster_fixup(self, mon_name):
        """
        Special fixups to determine exact monster type.
        @param mon_name Monster name
        @return Fixed monster name
        """
        # Find giant subtype
        if mon_name == "Giant":
            roll = Dice.roll(10)
            if roll <= 6:
                return "Giant, Hill"
            elif roll == 7:
                return "Giant, Stone"
            elif roll == 8:
                return "Giant, Frost"
            elif roll == 9:
                return "Giant, Fire"
            elif roll == 10:
                return "Giant, Cloud"
        
        # Find dragon subtype
        if mon_name == "Dragon":
            roll = Dice.roll(6)
            if roll == 1:
                return "Dragon, White"
            elif roll == 2:
                return "Dragon, Black"
            elif roll == 3:
                return "Dragon, Green"
            elif roll == 4:
                return "Dragon, Blue"
            elif roll == 5:
                return "Dragon, Red"
            elif roll == 6:
                return "Dragon, Gold"
        
        # Find specific giant animal
        if mon_name == "Giant Snake":
            return "Giant Snake, Constrictor"
        if mon_name == "Giant Beetle":
            return "Giant Beetle, Bombardier"
        if mon_name == "Giant Ant":
            return "Giant Ant, Worker"
        if mon_name == "Sea Monster":
            return "Sea Monster, Small"
        if mon_name == "Hydra":
            return "Hydra, 10 Heads"
        if mon_name == "Roc":
            return "Roc, Small"
        
        return mon_name
    
    def handle_npc_type(self, type_name):
        """
        Special handling for NPC types.
        @param type_name NPC type name
        @return Total EHD of encounter (0 if not NPC)
        """
        npc_level = 0
        if type_name == "Wizard":
            npc_level = 11
        elif type_name == "Necromancer":
            npc_level = 10
        elif type_name == "Lord":
            npc_level = 9
        elif type_name == "Superhero":
            npc_level = 8
        elif type_name == "Patriarch":
            npc_level = 8
        elif type_name == "Evil High Priest":
            npc_level = 8
        
        if npc_level == 0:
            return 0
        else:
            return npc_level + self.get_npc_entourage()
    
    def get_npc_entourage(self):
        """
        Get value of NPC entourage.
        @return Total EHD of entourage.
        """
        total = 0
        number = Dice(2, 6).roll_dice()
        for _ in range(number):
            total += Dice.roll(4)
        return total
    
    def ehd_fixup(self, mon_name, ehd):
        """
        Special fixups to determine estimated EHD.
        @param mon_name Monster name
        @param ehd Current EHD value
        @return Fixed EHD value
        """
        # Fill in null EHDs with estimated value
        if ehd == 0:
            if mon_name == "Dragon, Gold":
                return 40
        return ehd
    
    def str_to_int(self, s):
        """
        Convert a string to an integer.
        Invalid integer strings return 0.
        @param s String to convert
        @return Integer value or 0
        """
        try:
            return int(s)
        except (ValueError, TypeError):
            return 0
    
    def str_to_dbl(self, s):
        """
        Convert a string to a double.
        Invalid strings return 0.
        @param s String to convert
        @return Float value or 0
        """
        try:
            return float(s)
        except (ValueError, TypeError):
            return 0.0
    
    def roll_encounter_by_monster(self, monster_name):
        """
        Roll up an encounter for a given monster type.
        @param monster_name Monster name
        @return Total EHD of encounter
        """
        # Special handling for NPC types
        npc_value = self.handle_npc_type(monster_name)
        if npc_value > 0:
            return npc_value
        
        # Find index in monster table
        monster_index = self.monster_table.get_row_from_name(monster_name)
        if monster_index < 1:
            print(f"Unknown monster: {monster_name}", file=sys.stderr)
            return 0
        
        # Roll number appearing
        num_dice = Dice(self.monster_table.get_entry(monster_index, self.MONSTER_NUM_COL))
        number = num_dice.roll_dice()
        
        # Get the EHD value
        ehd = self.str_to_int(self.monster_table.get_entry(monster_index, self.MONSTER_EHD_COL))
        ehd = self.ehd_fixup(monster_name, ehd)
        if ehd == 0:
            print(f"Monster with null EHD: {monster_name}", file=sys.stderr)
        
        # Compute the product
        total_ehd = number * ehd
        hit_dice_num = self.str_to_dbl(self.monster_table.get_entry(monster_index, self.MONSTER_HDN_COL))
        if hit_dice_num <= 1.0:
            total_ehd //= 4  # sweep attack effect
        
        return total_ehd
    
    def roll_encounter_by_sub_table(self, table_name):
        """
        Roll encounter for a named subtable.
        @param table_name Subtable name
        @return Total EHD of encounter
        """
        # Get subtable column
        col_index = self.sub_table.get_col_from_name(table_name)
        if col_index < 1:
            print(f"Unknown subtable: {table_name}", file=sys.stderr)
            return 0
        
        # Roll monster name, look up monster
        monster_name = self.sub_table.get_random_entry_on_col(col_index)
        monster_name = self.monster_fixup(monster_name)
        return self.roll_encounter_by_monster(monster_name)
    
    def roll_encounter_by_terrain(self):
        """
        Roll encounter for the object terrain.
        @return Total EHD of encounter
        """
        # Roll subtable name, look up subtable
        sub_table_name = self.main_table.get_random_entry_on_col(self.terrain_index)
        sub_table_name = self.sub_table_fixup(self.terrain, sub_table_name)
        return self.roll_encounter_by_sub_table(sub_table_name)
    
    def run_sim(self):
        """Main object method."""
        for _ in range(self.NUM_ENCOUNTERS):
            total_ehd = self.roll_encounter_by_terrain()
            print(total_ehd)


def main():
    """Main application method."""
    sim = WildernessEncounterSim()
    sim.parse_args(sys.argv[1:])
    
    if sim.exit_after_args:
        sim.print_usage()
    else:
        sim.run_sim()


if __name__ == "__main__":
    main()
