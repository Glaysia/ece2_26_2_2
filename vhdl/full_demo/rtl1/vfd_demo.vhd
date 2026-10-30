library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity vfd_demo is
generic(
	cnt_max : integer := 4; 
	lcd_char : integer := 16;
	stable_delay : integer := 19;
	display_delay : integer := 399 
);
port(
	clk : in std_logic;			-- 1MHz Clock	
	rst	: in std_logic;

	vfd_e : out std_logic;
	vfd_rs : out std_logic;
	vfd_rw : out std_logic;
	vfd_data : out std_logic_vector(7 downto 0)
);
end vfd_demo;

architecture a of vfd_demo is

type lcd_state is ( 
	delay_20m, 
	function_set,
	entry_mode, 
	disp_on, 
	disp_line1, 
	disp_line2, 
	delay_2s, 
	brightness_set 
);

signal lcd_routine : lcd_state;
signal cnt_clk : integer range 0 to cnt_max;
signal cnt_clk_half : integer range 0 to cnt_max;

signal cnt_delay_20m : integer range 0 to stable_delay;
signal cnt_delay_2s : integer range 0 to display_delay;
signal cnt_line : integer range 0 to lcd_char;
signal cnt_brightness : std_logic_vector(1 downto 0);

type ar_lcd_data is array (0 to lcd_char) of std_logic_vector(7 downto 0);
signal reg_lcd_data1 : ar_lcd_data;
signal reg_lcd_data2 : ar_lcd_data;

signal cnt	: integer range 0 to 499;
signal clk_d	: std_logic;

begin

vfd_rw <= '0';

reg_lcd_data1(0)  <= "10000000";  -- line1 address
reg_lcd_data1(1)  <= "01010111";	-- W
reg_lcd_data1(2)  <= "01100101";	-- e
reg_lcd_data1(3)  <= "01101100";	-- l
reg_lcd_data1(4)  <= "01100011";	-- c
reg_lcd_data1(5)  <= "01101111";	-- o
reg_lcd_data1(6)  <= "01101101";	-- m
reg_lcd_data1(7)  <= "01100101";	-- e
reg_lcd_data1(8)  <= "00100000";	-- 
reg_lcd_data1(9)  <= "01001000";	-- H
reg_lcd_data1(10) <= "01100001";	-- a 
reg_lcd_data1(11) <= "01101110";	-- n
reg_lcd_data1(12) <= "01100010";	-- b
reg_lcd_data1(13) <= "01100001";	-- a
reg_lcd_data1(14) <= "01100011";	-- c
reg_lcd_data1(15) <= "01101011";	-- k
reg_lcd_data1(16) <= "00100001";	-- !

reg_lcd_data2(0)  <= "11000000";  -- line2 address
reg_lcd_data2(1)  <= "01001000";	-- H
reg_lcd_data2(2)  <= "01000010";	-- B
reg_lcd_data2(3)  <= "01000101";	-- E
reg_lcd_data2(4)  <= "00101101";	-- -
reg_lcd_data2(5)  <= "01000011";	-- C
reg_lcd_data2(6)  <= "01101111";	-- o
reg_lcd_data2(7)  <= "01101101";	-- m
reg_lcd_data2(8)  <= "01100010";	-- b
reg_lcd_data2(9)  <= "01101111";	-- o
reg_lcd_data2(10) <= "00100000";	-- 
reg_lcd_data2(11) <= "01001001";	-- I
reg_lcd_data2(12) <= "01001001";	-- I
reg_lcd_data2(13) <= "00101101";	-- -
reg_lcd_data2(14) <= "01000100";	-- D
reg_lcd_data2(15) <= "01001100";	-- L
reg_lcd_data2(16) <= "01000100";	-- D

process(clk)
begin
if clk'event and clk = '1' then
	if cnt = 499 then
		clk_d <= not clk_d;
		cnt <= 0;
	else
		cnt <= cnt + 1;
	end if;
end if;
end process;

process (rst, clk_d)
begin
	if rst = '0' then
		cnt_clk <= 0;
	elsif clk_d'event and clk_d = '1' then
		if cnt_clk = cnt_max then
			cnt_clk <= 0;
		else
			cnt_clk <= cnt_clk + 1;
		end if;
	end if;
end process;

process (rst, clk_d)
begin
	if rst = '0' then
		cnt_delay_20m <= 0;
	elsif clk_d'event and clk_d = '1' then
		if lcd_routine = delay_20m then
			if cnt_clk = cnt_max then
				if cnt_delay_20m = stable_delay then
					cnt_delay_20m <= 0;
				else
					cnt_delay_20m <= cnt_delay_20m + 1;
				end if;
			end if;
		else
			cnt_delay_20m <= 0;
		end if;
	end if;
end process;

process (rst, clk_d)
begin
	if rst = '0' then
		cnt_delay_2s <= 0;
	elsif clk_d'event and clk_d = '1' then
		if lcd_routine = delay_2s then
			if cnt_clk = cnt_max then
				if cnt_delay_2s = display_delay then
					cnt_delay_2s <= 0;
				else
					cnt_delay_2s <= cnt_delay_2s + 1;
				end if;
			end if;
		else
			cnt_delay_2s <= 0;
		end if;
	end if;
end process;

process (rst, clk_d)
begin
	if rst = '0' then
		cnt_line <= 0;
	elsif clk_d'event and clk_d = '1' then
		if lcd_routine = disp_line1 or lcd_routine = disp_line2 then
			if cnt_clk = cnt_max then
				if cnt_line = lcd_char then
					cnt_line <= 0;
				else
					cnt_line <= cnt_line + 1;
				end if;
			end if;
		else
			cnt_line <= 0;
		end if;
	end if;
end process;

process (rst, clk_d)
begin
	if rst = '0' then
		lcd_routine <= delay_20m;
	elsif clk_d'event and clk_d = '1' then
		if cnt_clk = cnt_max then
			case lcd_routine is
				when delay_20m =>
					if cnt_delay_20m = stable_delay then
						lcd_routine <= function_set;
					end if;
				when function_set =>
					lcd_routine <= entry_mode;
				when entry_mode =>
					lcd_routine <= disp_on;
				when disp_on =>
					lcd_routine <= disp_line1;
				when disp_line1 =>
					if cnt_line = lcd_char then
						lcd_routine <= disp_line2;
					end if;
				when disp_line2 =>
					if cnt_line = lcd_char then
						lcd_routine <= delay_2s;
					end if;
				when delay_2s =>
					if cnt_delay_2s = display_delay then
						lcd_routine <= brightness_set;
					end if;
				when brightness_set =>
					lcd_routine <= delay_2s;
			end case;
		end if;
	end if;
end process; 		

cnt_clk_half <= cnt_max - 1;
						
process (rst, clk_d)
begin
	if rst = '0' then
		vfd_e <= '0';
	elsif clk_d'event and clk_d = '1' then
		case lcd_routine is
			when delay_20m =>
				vfd_e <= '0';
			when function_set to disp_line2 =>
				if cnt_clk >= 1 and (cnt_clk <= cnt_clk_half) then
					vfd_e <= '1';
				else
					vfd_e <= '0';
				end if;
			when delay_2s =>
				vfd_e <= '0';
			when brightness_set =>
				if cnt_clk >= 1 and (cnt_clk <= cnt_clk_half) then
					vfd_e <= '1';
				else
					vfd_e <= '0';
				end if;
		end case;
	end if;
end process;				
					
process (rst, clk_d)
begin
	if rst = '0' then
		vfd_rs <= '0';
	elsif clk_d'event and clk_d = '1' then
		if lcd_routine = disp_line1 or lcd_routine = disp_line2 then
			if cnt_line = 0 then
				vfd_rs <= '0';
			else
				vfd_rs <= '1';
			end if;
		else
			vfd_rs <= '0';
		end if;
	end if;
end process;

process (rst, clk_d)
begin
	if rst = '0' then
		cnt_brightness <= "00";
	elsif clk_d'event and clk_d = '1' then
		if lcd_routine = brightness_set then
			if cnt_brightness = "11" then
				cnt_brightness <= "00";
			else
				cnt_brightness <= cnt_brightness + 1;
			end if;
		end if;
	end if;
end process;


process (rst, clk_d)
begin
	if rst= '0' then
		vfd_data <= "00000000";
	elsif clk_d'event and clk_d = '1' then
		case lcd_routine is
			when delay_20m =>
				vfd_data <= "00000000";
			when function_set =>
				vfd_data <= "00111000";
			when entry_mode =>
				vfd_data <= "00000110";
			when disp_on =>
				vfd_data <= "00001100";
			when disp_line1 =>
				vfd_data <= reg_lcd_data1(cnt_line);
			when disp_line2 =>
				vfd_data <= reg_lcd_data2(cnt_line);
			when delay_2s =>
				vfd_data <= "00000000";
			when brightness_set =>
				vfd_data <= "001110" & cnt_brightness;
		end case;
	end if;
end process; 	


end a;
