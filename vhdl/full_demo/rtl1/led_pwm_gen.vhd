library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

-- 8 LEDs Controller with 8BIT PWM Generator
-- 8BIT (CLK * 256(2^8))Level Shades
-- LED input "10000000" 128 level
-- LED input "01000000"  64 level
-- LED input "00100000"  32 level
-- LED input "00010000"  16 level
-- LED input "00001000"   8 level
-- LED input "00000100"   4 level
-- LED input "00000010"   2 level
-- LED input "00000001"   1 level


entity led_pwm_gen is

port( 
		clk		: in std_logic;						-- PWM Clock (1/256 shade)
		data_a	: in std_logic_vector(7 downto 0);	-- LED 7 input
		data_b	: in std_logic_vector(7 downto 0);	-- LED 6 input
		data_c	: in std_logic_vector(7 downto 0);	-- LED 5 input
		data_d	: in std_logic_vector(7 downto 0);	-- LED 4 input
		data_e	: in std_logic_vector(7 downto 0);	-- LED 3 input
		data_f	: in std_logic_vector(7 downto 0);	-- LED 2 input
		data_g	: in std_logic_vector(7 downto 0);	-- LED 1 input
		data_h	: in std_logic_vector(7 downto 0);	-- LED 0 input
		pwm		: out std_logic_vector(7 downto 0); -- PWM output
		led		: out std_logic_vector(7 downto 0);	-- LED 7~0 output
		fclk	: out std_logic); 					-- Frame Clock
end led_pwm_gen;

architecture hb of led_pwm_gen is

signal cnt	  : integer range 0 to 255;
signal shades : std_logic_vector(7 downto 0);


begin

process(clk)									
begin
if clk'event and clk ='1' then
	if cnt = 255 then
		cnt <= 0;
		fclk <= '1';
	else
		cnt <= cnt + 1;
		fclk <= '0';
	end if;
end if;
end process;
	
process(cnt)
begin
	if (cnt >=0 and cnt < 1 ) then
		shades <= "00000001";
	elsif (cnt >=1 and cnt <3)then
		shades <= "00000010";
	elsif (cnt >=3 and cnt <7)then
		shades <= "00000100";
	elsif (cnt >=7 and cnt <15)then
		shades <= "00001000";
	elsif (cnt >=15 and cnt <31)then
		shades <= "00010000";
	elsif (cnt >=31 and cnt <63)then
		shades <= "00100000";
	elsif (cnt >=63 and cnt <127)then
		shades<= "01000000";
	elsif (cnt >=127 and cnt <=255)then
		shades<= "10000000";
	else
		shades <= "00000000";
	end if;
end process;

PWM <= shades;	
	

LED(7) <= (DATA_A(7)and SHADES(7))or(DATA_A(6)and SHADES(6))or(DATA_A(5)and SHADES(5))or(DATA_A(4)and SHADES(4))or     
			(DATA_A(3)and SHADES(3))or (DATA_A(2)and SHADES(2))or (DATA_A(1)and SHADES(1))or (DATA_A(0)and SHADES(0));  
LED(6) <= (DATA_B(7)and SHADES(7))or(DATA_B(6)and SHADES(6))or(DATA_B(5)and SHADES(5))or(DATA_B(4)and SHADES(4))or     
			(DATA_B(3)and SHADES(3))or (DATA_B(2)and SHADES(2))or (DATA_B(1)and SHADES(1))or (DATA_B(0)and SHADES(0));  
LED(5) <= (DATA_C(7)and SHADES(7))or(DATA_C(6)and SHADES(6))or(DATA_C(5)and SHADES(5))or(DATA_C(4)and SHADES(4))or     
			(DATA_C(3)and SHADES(3))or (DATA_C(2)and SHADES(2))or (DATA_C(1)and SHADES(1))or (DATA_C(0)and SHADES(0));  
LED(4) <= (DATA_D(7)and SHADES(7))or(DATA_D(6)and SHADES(6))or(DATA_D(5)and SHADES(5))or(DATA_D(4)and SHADES(4))or     
			(DATA_D(3)and SHADES(3))or (DATA_D(2)and SHADES(2))or (DATA_D(1)and SHADES(1))or (DATA_D(0)and SHADES(0));  
LED(3) <= (DATA_E(7)and SHADES(7))or(DATA_E(6)and SHADES(6))or(DATA_E(5)and SHADES(5))or(DATA_E(4)and SHADES(4))or     
			(DATA_E(3)and SHADES(3))or (DATA_E(2)and SHADES(2))or (DATA_E(1)and SHADES(1))or (DATA_E(0)and SHADES(0));
LED(2) <= (DATA_F(7)and SHADES(7))or(DATA_F(6)and SHADES(6))or(DATA_F(5)and SHADES(5))or(DATA_F(4)and SHADES(4))or     
			(DATA_F(3)and SHADES(3))or (DATA_F(2)and SHADES(2))or (DATA_F(1)and SHADES(1))or (DATA_F(0)and SHADES(0)); 
LED(1) <= (DATA_G(7)and SHADES(7))or(DATA_G(6)and SHADES(6))or(DATA_G(5)and SHADES(5))or(DATA_G(4)and SHADES(4))or     
			(DATA_G(3)and SHADES(3))or (DATA_G(2)and SHADES(2))or (DATA_G(1)and SHADES(1))or (DATA_G(0)and SHADES(0));  
LED(0) <= (DATA_H(7)and SHADES(7))or(DATA_H(6)and SHADES(6))or(DATA_H(5)and SHADES(5))or(DATA_H(4)and SHADES(4))or     
			(DATA_H(3)and SHADES(3))or (DATA_H(2)and SHADES(2))or (DATA_H(1)and SHADES(1))or (DATA_H(0)and SHADES(0)); 

end hb;