# WildernessEncounterSim
Simulator for wilderness encounters in OD&D.

Randomly rolls encounters using OD&D (LBB) Vol-3 tables, and reports total EHD (Equivalent Hit Dice) for each. Uses data for EHD produced by the Arena/MonsterMetrics simulator, and documented in the OED Monster Database (http://www.oedgames.com/addons/houserules/index.html).

Specify desired terrain on command-line; output is a thousand encounter EHD values, for external statistical processing.

# Python version

## Python Script
A standalone Python script version is available in the `python/` directory. It works the same as the Java version:

```bash
python3 python/wilderness_encounter_sim.py <terrain>
```

For example:
```bash
python3 python/wilderness_encounter_sim.py Clear
python3 python/wilderness_encounter_sim.py Mountain
python3 python/wilderness_encounter_sim.py Desert
```

Available terrains: Clear, Woods, River, Swamp, Mountain, Desert, City

The script outputs 1000 encounter EHD values, one per line, for external statistical processing.

## Python Notebook
In the python/notebooks folder there is a jupyter notebook implementing this.  It will randomly select a terrain, otherwise set the one you want.

# Blog
See https://deltasdnd.blogspot.com/2021/12/wilderness-simulator-stats.html and other posts for lots of interesting discussion.

