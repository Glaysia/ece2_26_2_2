set design_top lab3_led_pwm
set simulation_top tb_led_pwm
set constraint_file constraints/lab3_led_pwm.xdc
source [file join [file dirname [info script]] vivado_batch.tcl]
