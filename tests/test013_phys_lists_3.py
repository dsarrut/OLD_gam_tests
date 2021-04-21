#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import gam
from test013_phys_lists_base import create_pl_sim

# create simulation
sim = create_pl_sim()

# keep only ion sources
sim.source_manager.user_info_sources.pop('gamma')

# change physics
p = sim.get_physics_info()
p.physics_list_name = 'G4EmStandardPhysics_option4'
p.enable_decay = True
p.apply_cuts = True  # default
cuts = p.production_cuts
mm = gam.g4_units('mm')
cuts.world.electron = 0.1 * mm
cuts.b1.electron = 0.01 * mm

# initialize
sim.initialize()

print('Phys list cuts:')
print(sim.physics_manager.dump_cuts())

# start simulation
# sim.set_g4_verbose(True)
# sim.apply_g4_command("/tracking/verbose 1")
gam.source_log.setLevel(gam.DEBUG)
sim.start()

# Gate mac/main_3.mac
stats = sim.get_actor('Stats')
stats_ref = gam.read_stat_file('./gate_test13_phys_lists/output/stat_3.txt')
is_ok = gam.assert_stats(stats, stats_ref, tolerance=0.1)

gam.test_ok(is_ok)
