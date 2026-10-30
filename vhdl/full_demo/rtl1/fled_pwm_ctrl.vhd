library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY fled_pwm_ctrl is
	port(
			nRESET	: in std_logic;
			clk1kHz	: in std_logic;
			ref		: in std_logic_vector(7 downto 0);	-- pwm duty
			led_out	: out std_logic							-- pwm out
		);
end fled_pwm_ctrl ;

ARCHITECTURE Behav OF fled_pwm_ctrl IS

signal pwm_width : std_logic_vector(7 downto 0);

BEGIN

	PROCESS(nRESET,clk1kHz)
	BEGIN
		IF nRESET = '0' THEN
			pwm_width <= x"00";
			led_out <= '1';
		ELSIF clk1kHz='1' AND clk1kHz'EVENT THEN
			pwm_width <= pwm_width + '1';
			
			if pwm_width >= ref then
				led_out <= '1';
			else
				led_out <= '0';
			end if;			
		END IF;
	END PROCESS;
	
END Behav;
