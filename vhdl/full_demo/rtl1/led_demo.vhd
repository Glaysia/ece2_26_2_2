library ieee;
use ieee.std_logic_1164.all;

entity led_demo is
port(
	clk		: in std_logic;
	led_data: out std_logic_vector(7 downto 0));
end led_demo;

architecture hb of led_demo is

component led_clk_gen
port(
	clk		: in std_logic;
	fclk	: in std_logic;
	led_clk	: out std_logic;
	led1	: out std_logic_vector(7 downto 0);
	led2	: out std_logic_vector(7 downto 0);
	led3	: out std_logic_vector(7 downto 0);
	led4	: out std_logic_vector(7 downto 0);
	led5	: out std_logic_vector(7 downto 0);
	led6	: out std_logic_vector(7 downto 0);
	led7	: out std_logic_vector(7 downto 0);
	led8	: out std_logic_vector(7 downto 0));
end component;

component led_pwm_gen is
port(
	clk		: in std_logic;
	data_a	: in std_logic_vector(7 downto 0);
	data_b	: in std_logic_vector(7 downto 0);
	data_c	: in std_logic_vector(7 downto 0);
	data_d	: in std_logic_vector(7 downto 0);
	data_e	: in std_logic_vector(7 downto 0);
	data_f	: in std_logic_vector(7 downto 0);
	data_g	: in std_logic_vector(7 downto 0);
	data_h	: in std_logic_vector(7 downto 0);
	pwm		: out std_logic_vector(7 downto 0);
	led		: out std_logic_vector(7 downto 0);
	fclk	: out std_logic);
end component;

signal led1 : std_logic_vector(7 downto 0);
signal led2 : std_logic_vector(7 downto 0);
signal led3 : std_logic_vector(7 downto 0);
signal led4 : std_logic_vector(7 downto 0);
signal led5 : std_logic_vector(7 downto 0);
signal led6 : std_logic_vector(7 downto 0);
signal led7 : std_logic_vector(7 downto 0);
signal led8 : std_logic_vector(7 downto 0);
signal data_a : std_logic_vector(7 downto 0);
signal data_b : std_logic_vector(7 downto 0);
signal data_c : std_logic_vector(7 downto 0);
signal data_d : std_logic_vector(7 downto 0);
signal data_e : std_logic_vector(7 downto 0);
signal data_f : std_logic_vector(7 downto 0);
signal data_g : std_logic_vector(7 downto 0);
signal data_h : std_logic_vector(7 downto 0);

signal led_clk : std_logic;
signal pwm_clk : std_logic;
signal fclk_in : std_logic;
signal fclk_out: std_logic;

signal led_b	: std_logic_vector(7 downto 0);

begin

clk_gen : led_clk_gen
port map(	
	clk => clk, 
	fclk => fclk_in, 
	led_clk => led_clk, 
	led1 => led1, 
	led2 => led2, 
	led3 => led3, 
	led4 => led4,
 	led5 => led5, 
	led6 => led6, 
	led7 => led7, 
	led8 => led8);

pwm_gen : led_pwm_gen
port map(
	clk => pwm_clk, 
	data_a => data_h, 
	data_b => data_g, 
	data_c => data_f, 
	data_d => data_e, 
	data_e => data_d,
	data_f => data_c, 
	data_g => data_b, 
	data_h => data_a, 
	led => led_b, 
	fclk => fclk_out);

fclk_in <= fclk_out;
pwm_clk <= led_clk;
data_a <= led1;
data_b <= led2;
data_c <= led3;
data_d <= led4;
data_e <= led5;
data_f <= led6;
data_g <= led7;
data_h <= led8;

led_data(7 downto 0) <= led_b;

end hb;

