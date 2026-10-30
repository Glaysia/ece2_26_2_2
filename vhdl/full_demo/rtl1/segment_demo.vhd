library ieee;
use ieee.std_logic_1164.all;

entity segment_demo is
port(
	clk		: in std_logic;
	
	mil10, mil1	: out integer range 0 to 9;
	s10, s1	: out integer range 0 to 9;
	m10, m1	: out integer range 0 to 9); 
end segment_demo;

architecture hb of segment_demo is

component sep
port(
	a		: in integer range 0 to 99;
	ten, one: out integer range 0 to 9);
end component;

signal clk_100hz : std_logic;
signal clk_1hz	: std_logic;
signal min, sec	: integer range 0 to 99;
signal mil		: integer range 0 to 99;
signal m_clk	: std_logic;

begin

s_mil : sep
port map(mil, mil10, mil1);

s_s : sep
port map(sec, s10, s1);

s_m : sep
port map(min, m10, m1);


process(clk)
variable mil_cnt	: integer range 0 to 4999;
variable mil_clk	: std_logic;
begin
if clk'event and clk = '1' then
	if mil_cnt = 4999 then
		mil_cnt := 0;
		mil_clk := not mil_clk;
	else
		mil_cnt := mil_cnt + 1;
		mil_clk := mil_clk;
	end if;
	clk_100hz <= mil_clk;
end if;
end process;


process(clk_100hz)
begin
if clk_100hz'event and clk_100hz = '1' then
	if mil >= 99 then
		mil <= 0;
		clk_1hz <= '1';
	else
		mil <= mil + 1;
		clk_1hz <= '0';
	end if;
end if;
end process;

process(clk_1hz)
begin
if clk_1hz'event and clk_1hz = '1' then
	if sec >= 59 then
		m_clk <= '1';
		sec <= 0;
	else
		sec <= sec + 1;
		m_clk <= '0';
	end if;
end if;
end process;

process(m_clk)
begin
if m_clk'event and m_clk = '1' then
	if min >= 59 then
		min <= 0;
	else
		min <= min + 1;
	end if;
end if;
end process;


end hb;