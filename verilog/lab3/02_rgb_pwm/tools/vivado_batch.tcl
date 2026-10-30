# Variables design_top, simulation_top and constraint_file are set by build.tcl.
set project_root [file normalize [file join [file dirname [info script]] ..]]
set build_dir [file join $project_root build vivado]
file mkdir $build_dir

create_project -force lab3_batch $build_dir -part xc7s75fgga484-1
set rtl_files [concat [glob -nocomplain [file join $project_root src *.v]] \
                      [glob -nocomplain [file join $project_root src *.sv]]]
set tb_files [concat [glob -nocomplain [file join $project_root sim *.v]] \
                     [glob -nocomplain [file join $project_root sim *.sv]]]
if {[llength $rtl_files] == 0} { error "No RTL files found" }
add_files -norecurse $rtl_files
add_files -fileset sim_1 -norecurse $tb_files
add_files -fileset constrs_1 -norecurse [file join $project_root $constraint_file]
set_property top $design_top [get_filesets sources_1]
set_property top $simulation_top [get_filesets sim_1]
set_property target_language Verilog [current_project]
update_compile_order -fileset sources_1
update_compile_order -fileset sim_1

launch_runs synth_1 -jobs 4
wait_on_run synth_1
if {[get_property STATUS [get_runs synth_1]] ne "synth_design Complete!"} {
    error "Synthesis failed: [get_property STATUS [get_runs synth_1]]"
}
launch_runs impl_1 -to_step write_bitstream -jobs 4
wait_on_run impl_1
if {[get_property STATUS [get_runs impl_1]] ne "write_bitstream Complete!"} {
    error "Implementation failed: [get_property STATUS [get_runs impl_1]]"
}

open_run impl_1
report_drc -file [file join $build_dir drc.rpt]
report_timing_summary -file [file join $build_dir timing_summary.rpt]
report_utilization -file [file join $build_dir utilization.rpt]
set bit_files [glob -nocomplain [file join $build_dir lab3_batch.runs impl_1 *.bit]]
if {[llength $bit_files] != 1} { error "Expected exactly one bitstream, got $bit_files" }
file copy -force [lindex $bit_files 0] [file join $build_dir ${design_top}.bit]
puts "LAB3_VIVADO_PASS top=$design_top bit=[file join $build_dir ${design_top}.bit]"
close_project
