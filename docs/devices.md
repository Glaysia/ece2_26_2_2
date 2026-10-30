# 장치·기능별 소스 찾기

[메인 목차](../README.md) · [Verilog](../verilog/README.md) · [C](../c/README.md)

교안 원본과 새 제공 코드를 나란히 찾는 목록이다. 같은 장치를 다뤄도 원본·수정본의 포트와 핀 설정은 각각의 소스를 따른다.

| 장치·기능 | 교안 원본 | 새 제공 소스 |
|---|---|---|
| 논리·산술 | [logic_gate](../verilog/textbook/logic_gate/README.md) · [not_gate](../verilog/textbook/not_gate/README.md) · [full_adder](../verilog/textbook/full_adder/README.md) · [full_sub](../verilog/textbook/full_sub/README.md) · [adder_4bit](../verilog/textbook/adder_4bit/README.md) · [sub_4bit](../verilog/textbook/sub_4bit/README.md) · [mult_4bit](../verilog/textbook/mult_4bit/README.md) · [compare_4](../verilog/textbook/compare_4/README.md) · [encoder8x3](../verilog/textbook/encoder8x3/README.md) · [decoder3x8](../verilog/textbook/decoder3x8/README.md) · [mux_4x1](../verilog/textbook/mux_4x1/README.md) · [demux_1x8](../verilog/textbook/demux_1x8/README.md) · [bcd_conv](../verilog/textbook/bcd_conv/README.md) | [lab1](../verilog/lab1/README.md) · [01_multiplier](../verilog/additional/01_multiplier/README.md) · [02_bcd_to_binary](../verilog/additional/02_bcd_to_binary/README.md) |
| 카운터·저장·FSM | [count_4](../verilog/textbook/count_4/README.md) · [counter_dnup](../verilog/textbook/counter_dnup/README.md) · [freq_div](../verilog/textbook/freq_div/README.md) · [register_4](../verilog/textbook/register_4/README.md) · [shift_register](../verilog/textbook/shift_register/README.md) · [piso4](../verilog/textbook/piso4/README.md) · [moore](../verilog/textbook/moore/README.md) · [mealy](../verilog/textbook/mealy/README.md) · [state_app](../verilog/textbook/state_app/README.md) | [lab2](../verilog/lab2/README.md) · [integrated](../verilog/integrated/README.md) |
| LED·RGB·PWM | [led_pwm](../verilog/textbook/led_pwm/README.md) · [rgb_led](../verilog/textbook/rgb_led/README.md) · [rgb_pwm](../verilog/textbook/rgb_pwm/README.md) | [01_led_pwm](../verilog/lab3/01_led_pwm/README.md) · [02_rgb_pwm](../verilog/lab3/02_rgb_pwm/README.md) · [05_pwm](../c/stm32/examples/05_pwm/README.md) |
| 7세그먼트·시계 | [seg_decoder](../verilog/textbook/seg_decoder/README.md) · [seg_decoder_arry](../verilog/textbook/seg_decoder_arry/README.md) · [watch](../verilog/textbook/watch/README.md) | [08_segment_scan](../verilog/lab2/08_segment_scan/README.md) · [05_mmss_clock](../verilog/lab3/05_mmss_clock/README.md) |
| 문자 LCD | [textlcd](../verilog/textbook/textlcd/README.md) | [06_character_lcd](../verilog/lab3/06_character_lcd/README.md) |
| 피에조·피아노 | [piezo](../verilog/textbook/piezo/README.md) · [piano](../verilog/textbook/piano/README.md) | [03_piezo](../verilog/lab3/03_piezo/README.md) · [03_piano](../verilog/additional/03_piano/README.md) |
| 스텝모터·서보 | [stepmotor](../verilog/textbook/stepmotor/README.md) · [servo_ctrl](../verilog/textbook/servo_ctrl/README.md) | [04_stepper](../verilog/lab3/04_stepper/README.md) · [05_servo](../verilog/additional/05_servo/README.md) |
| 신호등 | [traffic](../verilog/textbook/traffic/README.md) | [04_traffic](../verilog/additional/04_traffic/README.md) |
| UART·USB 시리얼 | [serial](../verilog/textbook/serial/README.md) · [usb232](../verilog/textbook/usb232/README.md) | [07_uart_echo](../verilog/lab3/07_uart_echo/README.md) · [uart_keypad](../verilog/extras/uart_keypad/README.md) · [06_pc_uart](../c/stm32/examples/06_pc_uart/README.md) · [07_uart_to_fpga](../c/stm32/examples/07_uart_to_fpga/README.md) |
| ADC·DAC·SRAM | [adc](../verilog/textbook/adc/README.md) · [dac](../verilog/textbook/dac/README.md) · [sram](../verilog/textbook/sram/README.md) | [07_adc](../verilog/additional/07_adc/README.md) · [08_dac](../verilog/additional/08_dac/README.md) · [06_sram](../verilog/additional/06_sram/README.md) |
| STM32 LED·버튼·인터럽트 | — | [01_led_polling](../c/stm32/examples/01_led_polling/README.md) · [02_button_polling](../c/stm32/examples/02_button_polling/README.md) · [03_button_interrupt](../c/stm32/examples/03_button_interrupt/README.md) · [04_timer_interrupt](../c/stm32/examples/04_timer_interrupt/README.md) |
| STM32 SPI | — | [08_spi_master](../c/stm32/examples/08_spi_master/README.md) · [09_spi_slave](../c/stm32/examples/09_spi_slave/README.md) |

버튼·DIP·VFD 등을 포함한 제조사 [VHDL 통합 데모](../vhdl/full_demo/README.md)도 보존했다. FPGA SPI 과제는 기존 매뉴얼의 요구사항이며 제공된 정답 Verilog는 없다.
