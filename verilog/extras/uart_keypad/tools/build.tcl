set root [file normalize [file join [file dirname [info script]] ..]]
cd $root
create_project uart_keypad_test build/vivado -part xc7s75fgga484-1 -force
add_files [glob src/*.v]
add_files -fileset constrs_1 constraints/uart_keypad_test.xdc
add_files -fileset sim_1 sim/tb_uart_keypad.sv
set_property top uart_keypad_test [get_filesets sources_1]
set_property top tb_uart_keypad [get_filesets sim_1]
set_property xsim.simulate.runtime all [get_filesets sim_1]
launch_simulation -scripts_only
set simdir [file normalize build/vivado/uart_keypad_test.sim/sim_1/behav/xsim]
set env(PATH) "C:/AMDDesignTools/2026.1/Vivado/bin;$env(PATH)"
cd $simdir
exec cmd /c compile.bat > compile-console.log 2>@1
exec cmd /c elaborate.bat > elaborate-console.log 2>@1
exec cmd /c xsim.bat tb_uart_keypad_behav -runall -log standalone.log > simulation-console.log 2>@1
set f [open standalone.log r]
set result [read $f]
close $f
if {[string first "UART_KEYPAD_PASS" $result]<0} {error "XSim did not pass: $result"}
cd $root
file copy -force $simdir/standalone.log evidence/xsim.log
launch_runs synth_1 -jobs 4
wait_on_run synth_1
if {[get_property PROGRESS [get_runs synth_1]] ne "100%"} {error "Synthesis failed"}
launch_runs impl_1 -to_step write_bitstream -jobs 4
wait_on_run impl_1
if {[get_property PROGRESS [get_runs impl_1]] ne "100%"} {error "Implementation failed"}
open_run impl_1
report_timing_summary -file build/timing.rpt
report_drc -file build/drc.rpt
report_io -file build/io.rpt
set paths [get_timing_paths -delay_type min_max -max_paths 10]
foreach path $paths {if {[get_property SLACK $path]<0} {error "Timing failed"}}
puts "UART_TEST_BIT=[file normalize build/vivado/uart_keypad_test.runs/impl_1/uart_keypad_test.bit]"
close_project
