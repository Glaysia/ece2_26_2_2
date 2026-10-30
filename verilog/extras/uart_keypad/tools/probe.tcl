open_hw_manager
connect_hw_server -allow_non_jtag
set targets [get_hw_targets]
puts "UART_TEST_TARGETS=$targets"
foreach target $targets {
 open_hw_target $target
 foreach device [get_hw_devices] { puts "UART_TEST_DEVICE=$device PART=[get_property PART $device]" }
 close_hw_target
}
disconnect_hw_server
close_hw_manager
