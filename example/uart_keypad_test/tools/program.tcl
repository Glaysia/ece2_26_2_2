set root [file normalize [file join [file dirname [info script]] ..]]
cd $root
set bit [file normalize build/vivado/uart_keypad_test.runs/impl_1/uart_keypad_test.bit]
if {![file exists $bit]} {error "Missing bitstream"}
open_hw_manager
connect_hw_server -allow_non_jtag
set targets [get_hw_targets *13724327082d01]
if {[llength $targets]!=1} {error "Expected exactly the probed Xilinx cable"}
open_hw_target [lindex $targets 0]
set devices [get_hw_devices xc7s75_0]
if {[llength $devices]!=1} {error "Expected one xc7s75_0"}
set device [lindex $devices 0]
current_hw_device $device
refresh_hw_device $device
set_property PROGRAM.FILE $bit $device
program_hw_devices $device
refresh_hw_device $device
puts "UART_TEST_PROGRAMMED=$device BIT=$bit"
report_property $device
close_hw_target
disconnect_hw_server
close_hw_manager
