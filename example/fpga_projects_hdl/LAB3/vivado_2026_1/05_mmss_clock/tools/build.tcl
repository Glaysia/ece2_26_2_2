set design_top lab3_mmss_clock
set simulation_top tb_mmss_counter
set constraint_file constraints/lab3_mmss_clock.xdc
source [file join [file dirname [info script]] vivado_batch.tcl]
