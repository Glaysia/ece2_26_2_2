library ieee;
use ieee.std_logic_1164.all;

entity motor is
port(
	clk		: in std_logic;
	sensor	: in std_logic;
	
	motor_data : out std_logic_vector(3 downto 0));
end motor;

architecture hb of motor is

signal mode		: integer range 0 to 1;
signal m_cnt 	: integer range 0 to 3;
signal s_cnt	: integer range 0 to 19;
signal clk_div	: std_logic;
signal reg_sensor : std_logic_vector(1 downto 0);

begin


process(clk)
variable cnt : integer range 0 to 49;
variable clk_d : std_logic;
begin
if clk'event and clk = '1' then
	if cnt = 49 then
		cnt := 0;
		clk_d := not clk_d;
	else
		cnt := cnt + 1;
		clk_d := clk_d;
	end if;
	clk_div <= clk_d;
end if;
end process;


process(clk_div)
begin
if clk_div'event and clk_div = '1' then
	if mode = 0 then
		case m_cnt is
			when 0 => motor_data <= "0011";
			when 1 => motor_data <= "1001";
			when 2 => motor_data <= "1100";
			when 3 => motor_data <= "0110";
			when others => motor_data <= "0011";
		end case;
	elsif mode = 1 then
		case m_cnt is
			when 0 => motor_data <= "0011";
			when 1 => motor_data <= "0110";
			when 2 => motor_data <= "1100";
			when 3 => motor_data <= "1001";
			when others => motor_data <= "0011";
		end case;
	end if;
	m_cnt <= m_cnt + 1;
end if;
end process;

process (clk)
begin
if clk'event and clk = '1' then
	reg_sensor <= reg_sensor(0) & sensor;
end if;
end process;

process(clk)
begin
if clk'event and clk = '1' then
	if reg_sensor = "01" then
		if s_cnt = 9 then
			mode <= mode + 1;
			s_cnt <= 0;
		else
			s_cnt <= s_cnt + 1;
		end if;
	end if; 
end if;
end process;
end hb;