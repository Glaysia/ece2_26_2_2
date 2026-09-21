`timescale 1ns/1ps
module lab3_led_pwm #(
    parameter integer CLK_HZ = 50_000_000,
    parameter integer PWM_HZ = 1_000,
    parameter integer LEVELS = 10,
    parameter integer DEBOUNCE_CYCLES = 1_000_000
) (
    input  wire clk,
    input  wire rst,
    input  wire button,
    output wire [7:0] led
);
    wire press;
    wire pwm;
    reg [3:0] level;

    button_onepulse #(.STABLE_CYCLES(DEBOUNCE_CYCLES)) u_button (
        .clk(clk), .rst(rst), .button(button), .pulse(press)
    );

    always @(posedge clk or posedge rst) begin
        if (rst)
            level <= 4'd0;
        else if (press)
            level <= (level == LEVELS) ? 4'd0 : level + 1'b1;
    end

    pwm_channel #(.PERIOD_CYCLES(CLK_HZ / PWM_HZ), .LEVELS(LEVELS)) u_pwm (
        .clk(clk), .rst(rst), .level(level), .pwm(pwm)
    );

    assign led = {8{pwm}};
endmodule
