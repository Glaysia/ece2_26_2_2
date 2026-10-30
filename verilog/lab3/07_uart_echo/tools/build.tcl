set design_top lab3_uart_echo
set simulation_top tb_uart_echo
set constraint_file constraints/lab3_uart_echo.xdc
source [file join [file dirname [info script]] vivado_batch.tcl]
