library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY clk_gen is
	port(
			nRESET	: in std_logic;
			CLK		: in std_logic;

			clk1kHz	: out std_logic;
			clk10kHz	: out std_logic
		);
end clk_gen ;

ARCHITECTURE Behav OF clk_gen IS

signal clk_cnt : integer range 0 to 50000;
signal clk_cntA : integer range 0 to 50000;
signal clk_1k : std_logic;
signal clk_10k : std_logic;
BEGIN

	process(nreset,clk)
	begin
		if nreset = '0' then
			clk_cnt <= 0;
			clk_1k <= '1';
		elsif clk'event and clk = '1' then
			if clk_cnt >= 25000 then
				clk_cnt <= 0;
				clk_1k <= not clk_1k;
			else
				clk_cnt <= clk_cnt + 1;
			end if;
		end if;
	end process;

	process(nreset,clk)
	begin
		if nreset = '0' then
			clk_cntA <= 0;
			clk_10k <= '1';
		elsif clk'event and clk = '1' then
			if clk_cntA >= 2500 then
				clk_cntA <= 0;
				clk_10k <= not clk_10k;
			else
				clk_cntA <= clk_cntA + 1;
			end if;
		end if;
	end process;
	
	clk1kHz <= clk_1k;
	clk10kHz <= clk_10k;

END Behav;
