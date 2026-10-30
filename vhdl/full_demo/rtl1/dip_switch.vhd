library ieee;
use ieee.std_logic_1164.all;

entity dip_switch is
port(
	dip_sw		: in std_logic_vector(3 downto 0);
	dip_data	: out integer range 0 to 16);
end dip_switch;

architecture hb of dip_switch is

begin

process(dip_sw)
begin
case dip_sw is
	when "0000" => dip_data <= 0;
	when "0001" => dip_data <= 1;
	when "0010" => dip_data <= 2;
	when "0011" => dip_data <= 3;
	when "0100" => dip_data <= 4;
	when "0101" => dip_data <= 5;
	when "0110" => dip_data <= 6;
	when "0111" => dip_data <= 7;
	when "1000" => dip_data <= 8;
	when "1001" => dip_data <= 9;
	when "1010" => dip_data <= 10;
	when "1011" => dip_data <= 11;
	when "1100" => dip_data <= 12;
	when "1101" => dip_data <= 13;
	when "1110" => dip_data <= 14;
	when "1111" => dip_data <= 15;
	when others => dip_data <= 16;
end case;
end process;

end hb;