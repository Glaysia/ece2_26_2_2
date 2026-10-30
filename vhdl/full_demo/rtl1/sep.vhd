library ieee;
use ieee.std_logic_1164.all;

entity sep is
port(
	a		: in integer range 0 to 99;
	ten, one: out integer range 0 to 9);
end sep;

architecture a of sep is
begin

process(a)
begin
	if a <= 9 then
		ten <= 0;
		one <= a;
	elsif a <= 19 then
		ten <= 1;
		one <= a - 10;
	elsif a <= 29 then
		ten <= 2;
		one <= a - 20;
	elsif a <= 39 then
		ten <= 3;
		one <= a - 30;
	elsif a <= 49 then
		ten <= 4;
		one <= a - 40;
	elsif a <= 59 then
		ten <= 5;
		one <= a - 50;
	elsif a <= 69 then
		ten <= 6;
		one <= a - 60;
	elsif a <= 79 then
		ten <= 7;
		one <= a - 70;
	elsif a <= 89 then
		ten <= 8;
		one <= a - 80;
	elsif a <= 99 then
		ten <= 9;
		one <= a - 90;
	else
		ten <= 0;
		one <= 0;
	end if;
end process;
end a;