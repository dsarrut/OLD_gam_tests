#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gam

# create the simulation
sim = gam.Simulation()

# main options
ui = sim.user_info
ui.g4_verbose = False
ui.g4_verbose_level = 1
ui.visu = True
ui.number_of_threads = 1
ui.random_engine = 'MersenneTwister'
ui.random_seed = 'auto'

# set the world size like in the Gate macro
m = gam.g4_units('m')
world = sim.world
world.size = [3 * m, 3 * m, 3 * m]

# add a simple waterbox volume
waterbox = sim.add_volume('Box', 'Waterbox')
cm = gam.g4_units('cm')
waterbox.size = [40 * cm, 40 * cm, 40 * cm]
waterbox.translation = [0 * cm, 0 * cm, 25 * cm]
waterbox.material = 'G4_WATER'

# physic list # FIXME will be changed
# print('Phys lists :', sim.get_available_physicLists())

# default source for tests
keV = gam.g4_units('keV')
mm = gam.g4_units('mm')
Bq = gam.g4_units('Bq')
source = sim.add_source('Generic', 'Default')
source.particle = 'gamma'
source.energy.mono = 80 * keV
source.direction.type = 'momentum'
source.direction.momentum = [0, 0, 1]
source.activity = 200000 * Bq

# runs
sec = gam.g4_units('second')
sim.run_timing_intervals = [[0, 0.5 * sec], [0.5 * sec, 1.0 * sec]]

# add stat actor
sim.add_actor('SimulationStatisticsActor', 'Stats')

# create G4 objects
sim.initialize()

# start simulation
# sim.apply_g4_command("/run/verbose 1")
sim.start()

stats = sim.get_actor('Stats')
stats.counts.run_count = 1

# gate_test4_simulation_stats_actor
# Gate mac/main.mac
stats_ref = gam.read_stat_file('./gate/gate_test004_simulation_stats_actor/output/stat.txt')
is_ok = gam.assert_stats(stats, stats_ref, tolerance=0.03)

gam.test_ok(is_ok)
