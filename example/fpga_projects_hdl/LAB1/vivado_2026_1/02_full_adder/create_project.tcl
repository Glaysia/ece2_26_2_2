set project_dir [file dirname [file normalize [info script]]]
create_project full_adder [file join $project_dir vivado] -part xc7s75fgga484-1 -force
set_property target_language Verilog [current_project]
add_files [file normalize [file join $project_dir {../../common/rtl/full_adder.v}]]
add_files [file normalize [file join $project_dir {../../common/rtl/half_adder.v}]]
add_files -fileset sim_1 [file normalize [file join $project_dir {../../common/tb/tb_full_adder.sv}]]
add_files -fileset constrs_1 [file normalize [file join $project_dir {../../common/constraints/full_adder.xdc}]]
set_property top full_adder [get_filesets sources_1]
set_property top tb_full_adder [get_filesets sim_1]
set_property xsim.simulate.runtime all [get_filesets sim_1]
update_compile_order -fileset sources_1
update_compile_order -fileset sim_1
close_project
