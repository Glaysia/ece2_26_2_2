library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity led_clk_gen is

port( 
		clk		: in std_logic;   						
		fclk	: in std_logic;							-- Frame Clock
		led_clk	: out std_logic;
		led1	: out std_logic_vector(7 downto 0);
		led2	: out std_logic_vector(7 downto 0);
		led3	: out std_logic_vector(7 downto 0);
		led4	: out std_logic_vector(7 downto 0);
		led5	: out std_logic_vector(7 downto 0);
		led6	: out std_logic_vector(7 downto 0);
		led7	: out std_logic_vector(7 downto 0);
		led8	: out std_logic_vector(7 downto 0));
end led_clk_gen;

architecture hb of led_clk_gen is

signal clk_cnt	: std_logic_vector(7 downto 0);
signal iclk 	: std_logic;
signal cnt 		: integer range 0 to 13;

begin
process(clk)
begin
if clk'event and clk = '1' then
	clk_cnt <= clk_cnt + '1';
end if;
end process;
	
process(clk_cnt(1))
variable cnt : integer range 0 to 15;
begin
if clk_cnt(1)'event and clk_cnt(1) = '1' then
	if cnt = 6 then
		cnt := 0;
		led_clk <= '1';
	else
		cnt := cnt + 1;
		led_clk <= '0';
	end if;
end if;
end process;
	
process(fclk)
variable cnt : integer range 0 to 50;
begin
if fclk'event and fclk = '1' then
	if cnt = 50 then
		cnt := 0;
		iclk <= '1';
	else
		cnt := cnt + 1;
		iclk <= '0';
	end if;
end if;
end process;
			
process(iclk)								
begin
if iclk'event and iclk = '1' then
	if cnt = 13 then
		cnt <= 0;
	else
		cnt <= cnt + 1;
	end if;
end if;
end process;

process(iclk)
begin
if iclk'event and iclk = '1' then
	if cnt = 0 then
		led1 <= "11111111";
		led2 <= "01111111";
		led3 <= "00111111";
		led4 <= "00011111";
		led5 <= "00001111";
		led6 <= "00000111";
		led7 <= "00000011";
		led8 <= "00000001";
	elsif cnt = 1 then
		led1 <= "01111111";
		led2 <= "11111111";
		led3 <= "00011111";
		led4 <= "00001111";
		led5 <= "00000111";
		led6 <= "00000011";
		led7 <= "00000001";
		led8 <= "00000000";
	elsif cnt = 2 then
		led1 <= "00111111";
		led2 <= "01111111";
		led3 <= "11111111";
		led4 <= "00000111";
		led5 <= "00000011";
		led6 <= "00000001";
		led7 <= "00000000";
		led8 <= "00000000";
	elsif cnt = 3 then
		led1 <= "00011111";
		led2 <= "00111111";
		led3 <= "01111111";
		led4 <= "11111111";
		led5 <= "00000001";
		led6 <= "00000000";
		led7 <= "00000000";
		led8 <= "00000000";
	elsif cnt = 4 then
		led1 <= "00001111";
		led2 <= "00011111";
		led3 <= "00111111";
		led4 <= "01111111";
		led5 <= "11111111";
		led6 <= "00000000";
		led7 <= "00000000";
		led8 <= "00000000";
	elsif cnt = 5 then
		led1 <= "00000111";
		led2 <= "00001111";
		led3 <= "00011111";
		led4 <= "00111111";
		led5 <= "01111111";
		led6 <= "11111111";
		led7 <= "00000000";
		led8 <= "00000000";
	elsif cnt = 6 then
		led1 <= "00000011";
		led2 <= "00000111";
		led3 <= "00001111";
		led4 <= "00011111";
		led5 <= "00111111";
		led6 <= "01111111";
		led7 <= "11111111";
		led8 <= "00000000";
	elsif cnt = 7 then
		led1 <= "00000001";
		led2 <= "00000011";
		led3 <= "00000111";
		led4 <= "00001111";
		led5 <= "00011111";
		led6 <= "00111111";
		led7 <= "01111111";
		led8 <= "11111111";
	elsif cnt = 8 then
		led1 <= "00000000";
		led2 <= "00000001";
		led3 <= "00000011";
		led4 <= "00000111";
		led5 <= "00001111";
		led6 <= "00011111";
		led7 <= "11111111";
		led8 <= "01111111";
	elsif cnt = 9 then
		led1 <= "00000000";
		led2 <= "00000000";
		led3 <= "00000001";
		led4 <= "00000011";
		led5 <= "00000111";
		led6 <= "11111111";
		led7 <= "01111111";
		led8 <= "00111111";
	elsif cnt = 10 then
		led1 <= "00000000";
		led2 <= "00000000";
		led3 <= "00000000";
		led4 <= "00000001";
		led5 <= "11111111";
		led6 <= "01111111";
		led7 <= "00111111";
		led8 <= "00011111";
	elsif cnt = 11 then
		led1 <= "00000000";
		led2 <= "00000000";
		led3 <= "00000000";
		led4 <= "11111111";
		led5 <= "01111111";
		led6 <= "00111111";
		led7 <= "00011111";
		led8 <= "00001111";
	elsif cnt = 12 then
		led1 <= "00000000";
		led2 <= "00000000";
		led3 <= "11111111";
		led4 <= "01111111";
		led5 <= "00111111";
		led6 <= "00011111";
		led7 <= "00001111";
		led8 <= "00000111";
	elsif cnt = 13 then
		led1 <= "00000000";
		led2 <= "11111111";
		led3 <= "01111111";
		led4 <= "00111111";
		led5 <= "00011111";
		led6 <= "00001111";
		led7 <= "00000111";
		led8 <= "00000011";
	end if;
end if;
end process;								

end hb;