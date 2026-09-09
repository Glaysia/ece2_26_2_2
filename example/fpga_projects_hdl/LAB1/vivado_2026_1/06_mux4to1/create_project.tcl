set project_dir [file dirname [file normalize [info script]]]
create_project mux_4x1 [file join $project_dir vivado] -part xc7s75fgga484-1 -force
set_property target_language Verilog [current_project]
add_files [file normalize [file join $project_dir {../../common/rtl/mux_4x1.v}]]
add_files -fileset sim_1 [file normalize [file join $project_dir {../../common/tb/tb_mux_4x1.sv}]]
add_files -fileset constrs_1 [file normalize [file join $project_dir {../../common/constraints/mux_4x1.xdc}]]
set_property top mux_4x1 [get_filesets sources_1]
set_property top tb_mux_4x1 [get_filesets sim_1]
set_property xsim.simulate.runtime all [get_filesets sim_1]
update_compile_order -fileset sources_1
update_compile_order -fileset sim_1
close_project
