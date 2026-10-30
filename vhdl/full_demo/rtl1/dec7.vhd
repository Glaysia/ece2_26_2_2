library ieee;
use ieee.std_logic_1164.all;

entity dec7 is
port(
	bcd	: in integer range 0 to 16;
	seg	: out std_logic_vector(7 downto 0));
end dec7;

architecture a of dec7 is

signal y	: std_logic_vector(7 downto 0);

begin	

process(bcd)
begin
	case bcd is
		when 0 =>
			y <= "11111100";
		when 1 =>
			y <= "01100000";
		when 2 =>
			y <= "11011010";
		when 3 =>
			y <= "11110010";
		when 4 =>
			y <= "01100110";
		when 5 =>
			y <= "10110110";
		when 6 =>
			y <= "10111110";
		when 7 =>
			y <= "11100000";
		when 8 =>
			y <= "11111110";
		when 9 =>
			y <= "11100110";
		when 10 =>
			y <= "11101110";
		when 11 =>
			y <= "00111110";
		when 12 =>
			y <= "10011100";
		when 13 =>
			y <= "01111010";
		when 14 =>
			y <= "10011110";
		when 15 =>
			y <= "10001110";
		when 16 =>
			y <= "00000000";
		when others =>
			y <= "00000000";
	end case;
end process;
seg <= y;
end a;