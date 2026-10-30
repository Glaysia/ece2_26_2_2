library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY seg_7_demo is
	port(
			nRESET	: in std_logic;
			CLK		: in std_logic;
			sw 		: in std_logic;
			
			seg_data	: out std_logic_vector(7 downto 0)
		);
end seg_7_demo ;

ARCHITECTURE Behav OF seg_7_demo IS

signal reg_sw : std_logic_vector(1 downto 0);
signal dec_cnt	: std_logic_vector(3 downto 0);


BEGIN

	PROCESS(nRESET,CLK)
	BEGIN
		IF nRESET = '0' THEN
			reg_sw <= "00";
		ELSIF CLK='1' AND CLK'EVENT THEN
			reg_sw <= reg_sw(0) & sw;
		END IF;
	END PROCESS;

	PROCESS(nRESET,CLK)
	BEGIN
		IF nRESET = '0' THEN
			dec_cnt <= x"0";
		ELSIF CLK='1' AND CLK'EVENT THEN
			if reg_sw = "01" then
				if dec_cnt >= x"9" then
					dec_cnt <= x"0";
				else
					dec_cnt <= dec_cnt + '1';
				end if;
			end if;

			case dec_cnt is
				when x"0" =>
					seg_data <= "11111100";
				when x"1" =>
					seg_data <= "01100000";
				when x"2" =>
					seg_data <= "11011010";
				when x"3" =>
					seg_data <= "11110010";
				when x"4" =>
					seg_data <= "01100110";
				when x"5" =>
					seg_data <= "10110110";
				when x"6" =>
					seg_data <= "10111110";
				when x"7" =>
					seg_data <= "11100000";
				when x"8" =>
					seg_data <= "11111110";
				when x"9" =>
					seg_data <= "11100110";
				when others => null;
			end case;

		END IF;
	END PROCESS;
	


END Behav;
