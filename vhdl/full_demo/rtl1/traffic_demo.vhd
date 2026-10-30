library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;
use ieee.std_logic_arith.all;

entity traffic_demo is
port(
	clk		: in std_logic;                     -- 10khz clock
	flicker : in std_logic;
	flick_sw : in std_logic;
--	red		: out std_logic_vector(3 downto 0); -- south, west, east, north
--	yellow	: out std_logic_vector(3 downto 0);
--	green		: buffer std_logic_vector(3 downto 0);
--	left_o	: out std_logic_vector(3 downto 0);
--	walk_r	: out std_logic_vector(3 downto 0);
--	walk_g	: out std_logic_vector(3 downto 0);
	EXT_63_40 : out std_logic_vector(23 downto 0)
	);
end traffic_demo;

architecture arc of traffic_demo is

signal cnt	: integer range 0 to 4999;
signal scnt	: integer range 0 to 12;
signal direction	: integer range 0 to 3;
signal sclk	: std_logic;
signal mclk	: std_logic;
signal s_flicker  : std_logic;
signal red,yellow,green,left_o,walk_r,walk_g : std_logic_vector(3 downto 0);

begin

left_o <= green;

EXT_63_40(0)	<=	LEFT_O(0);
EXT_63_40(1)	<=	WALK_G(0);
EXT_63_40(2)	<=	GREEN(0);
EXT_63_40(3)	<=	WALK_R(0);
EXT_63_40(4)	<=	WALK_G(2);
EXT_63_40(5)	<=	RED(0);
EXT_63_40(6)	<=	WALK_R(2);
EXT_63_40(7)	<=	YELLOW(0);
EXT_63_40(8)	<=	RED(3);
EXT_63_40(9)	<=	RED(2);
EXT_63_40(10)	<=	YELLOW(3);
EXT_63_40(11)	<=	YELLOW(2);
EXT_63_40(12)	<=	LEFT_O(3);
EXT_63_40(13)	<=	LEFT_O(2);
EXT_63_40(14)	<=	GREEN(3);
EXT_63_40(15)	<=	GREEN(2);
EXT_63_40(16)	<=	WALK_G(1);
EXT_63_40(17)	<=	RED(1);
EXT_63_40(18)	<=	WALK_R(1);
EXT_63_40(19)	<=	YELLOW(1);
EXT_63_40(20)	<=	WALK_G(3);
EXT_63_40(21)	<=	LEFT_O(1);
EXT_63_40(22)	<=	WALK_R(3);
EXT_63_40(23)	<=	GREEN(1);

process (flicker, flick_sw)
begin
	if flick_sw = '1' and flick_sw'event then
		s_flicker <= not s_flicker;
	end if;

end process;

process (clk)
begin
	if clk = '1' and clk'event then
		if cnt = 4999 then
			cnt <= 0;
			sclk <= not sclk;
		else
			cnt <= cnt + 1;
		end if;
	end if;
end process;

process (s_flicker,flicker, sclk)
begin
	if s_flicker = '1' or flicker = '1' then
		scnt <= 0;
		mclk <= '0';
	elsif sclk = '1' and sclk'event then
		if scnt = 12 then
			scnt <= 0;
			mclk <= '1';
		else
			scnt <= scnt + 1;
			mclk <= '0';
		end if;
	end if;
end process;

process (s_flicker,flicker, mclk)
begin
	if s_flicker = '1' or flicker = '1' then
		direction <= 0;
	elsif mclk = '1' and mclk'event then
		if direction = 3 then
			direction <= 0;
		else
			direction <= direction + 1;
		end if;
	end if;
end process;

process (s_flicker, flicker, direction, scnt, sclk)
begin
	if s_flicker = '1' or flicker = '1' then
		red <= "0000";
		green <= "0000";
		yellow <= sclk & sclk & sclk & sclk;
		walk_r <= sclk & sclk & sclk & sclk;
		walk_g <= "0000";
	else
		case direction is
			when 0 =>
				if scnt <= 10 then
					red    <= "0111";	--swen
					green  <= "1000";
					yellow <= "0000";

				elsif scnt <= 12  then
					red    <= "0111";
					green  <= "0000";
					yellow <= "1000";
				else
					red <= "0000";
					green <= "0000";
					yellow <= sclk & sclk & sclk & sclk;
				end if;

				if scnt <= 3 then
					walk_r <= "1011";
					walk_g <= "0100";
				elsif scnt <= 10 then
					walk_r <= "1011";
					walk_g <= '0' & (not sclk) & "00";
				elsif scnt <= 12 then
					walk_r <= "1111";
					walk_g <= "0000";
				else
					walk_r <= "0000";
					walk_g <= sclk & sclk & sclk & sclk;
				end if;

			when 1 => -- when 3
				if scnt <= 10 then
					red    <= "1110";
					green  <= "0001";
					yellow <= "0000";
				elsif scnt <= 12  then
					red    <= "1110";
					green  <= "0000";
					yellow <= "0001";
--				if scnt <= 10 then
--					red    <= "1011";
--					green  <= "0100";
--					yellow <= "0000";
--				elsif scnt <= 12  then
--					red    <= "1011";
--					green  <= "0000";
--					yellow <= "0100";
				else
					red <= "0000";
					green <= "0000";
					yellow <= sclk & sclk & sclk & sclk;
				end if;

				if scnt <= 3 then
					walk_r <= "1101";
					walk_g <= "0010";
				elsif scnt <= 10 then
					walk_r <= "1101";
					walk_g <= "00" & (not sclk) & '0';
				elsif scnt <= 12 then
					walk_r <= "1111";
					walk_g <= "0000";
				else
					walk_r <= "0000";
					walk_g <= sclk & sclk & sclk & sclk;
				end if;

			when 2 => -- when 1

				if scnt <= 10 then
					red    <= "1011";
					green  <= "0100";
					yellow <= "0000";
				elsif scnt <= 12  then
					red    <= "1011";
					green  <= "0000";
					yellow <= "0100";
--				if scnt <= 10 then
--					red    <= "1101";
--					green  <= "0010";
--					yellow <= "0000";
--				elsif scnt <= 12  then
--					red    <= "1101";
--					green  <= "0000";
--					yellow <= "0010";
				else
					red <= "0000";
					green <= "0000";
					yellow <= sclk & sclk & sclk & sclk;
				end if;

				if scnt <= 3 then
					walk_r <= "1110";
					walk_g <= "0001";
				elsif scnt <= 10 then
					walk_r <= "1110";
					walk_g <= "000" & (not sclk);
				elsif scnt <= 12 then
					walk_r <= "1111";
					walk_g <= "0000";
				else
					walk_r <= "0000";
					walk_g <= sclk & sclk & sclk & sclk;
				end if;

			when 3 => -- when 2

				if scnt <= 10 then
					red    <= "1101";
					green  <= "0010";
					yellow <= "0000";
				elsif scnt <= 12  then
					red    <= "1101";
					green  <= "0000";
					yellow <= "0010";
--				if scnt <= 10 then
--					red    <= "1110";
--					green  <= "0001";
--					yellow <= "0000";
--				elsif scnt <= 12  then
--					red    <= "1110";
--					green  <= "0000";
--					yellow <= "0001";
				else
					red <= "0000";
					green <= "0000";
					yellow <= sclk & sclk & sclk & sclk;
				end if;

				if scnt <= 3 then
					walk_r <= "0111";
					walk_g <= "1000";
				elsif scnt <= 10 then
					walk_r <= "0111";
					walk_g <= (not sclk) & "000";
				elsif scnt <= 12 then
					walk_r <= "1111";
					walk_g <= "0000";
				else
					walk_r <= "0000";
					walk_g <= sclk & sclk & sclk & sclk;
				end if;
		end case;
	end if;
end process;

end arc;
