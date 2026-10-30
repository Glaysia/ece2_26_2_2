library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY piezo_demo is
	port(
			nRESET	: in std_logic;
			CLK		: in std_logic;
			sw3 		: in std_logic;
			
			piezo 	: out std_logic
		);
end piezo_demo ;

ARCHITECTURE Behav OF piezo_demo IS

signal reg_sw : std_logic_vector(1 downto 0);
signal clk_sel	: std_logic_vector(7 downto 0);
signal freq_cnt : integer range 0 to 95785;
signal ref : integer range 0 to 95785;
signal piezo_clk : std_logic;

BEGIN

	PROCESS(nRESET,CLK)
	BEGIN
		IF nRESET = '0' THEN
			reg_sw <= "00";
		ELSIF CLK='1' AND CLK'EVENT THEN
			reg_sw <= reg_sw(0) & sw3;
		END IF;
	END PROCESS;

	PROCESS(nRESET,CLK)
	BEGIN
		IF nRESET = '0' THEN
			clk_sel <= x"00";
		ELSIF CLK='1' AND CLK'EVENT THEN
			if reg_sw = "01" then
				if clk_sel > x"15" then
					clk_sel <= x"00";
				else
					clk_sel <= clk_sel + '1';
				end if;
			end if;
		END IF;
	END PROCESS;
	
--95785 	47893 	23946 
--85324 	42662 	21331 
--75988 	37994 	18997 
--71633 	35817 	17908 
--63939 	31969 	15985 
--56818 	28409 	14205 
--50710 	25355 	12677 



	
	ref <=	95785 	when clk_sel(7 downto 0) = x"01" else --261hz Do 3
				85324 	when clk_sel(7 downto 0) = x"02" else --293hz Re 3
				75988 	when clk_sel(7 downto 0) = x"03" else --329hz Mi 3
				71633 	when clk_sel(7 downto 0) = x"04" else --349hz Fa 3
				63939 	when clk_sel(7 downto 0) = x"05" else --391hz Sol3
				56818 	when clk_sel(7 downto 0) = x"06" else --440hz La 3 
				50710 	when clk_sel(7 downto 0) = x"07" else --493hz Si 3
				
				47893 	when clk_sel(7 downto 0) = x"08" else --523hz Do 4
				42662 	when clk_sel(7 downto 0) = x"09" else --587hz Re 4
				37994 	when clk_sel(7 downto 0) = x"0A" else --659hz Mi 4
				35817 	when clk_sel(7 downto 0) = x"0B" else --698hz Fa 4
				31969 	when clk_sel(7 downto 0) = x"0C" else --783hz Sol4
				28409 	when clk_sel(7 downto 0) = x"0D" else --880hz La 4 
				25355 	when clk_sel(7 downto 0) = x"0E" else --987hz Si 4
				
				23946 	when clk_sel(7 downto 0) = x"0F" else --523hz Do 5
				21331 	when clk_sel(7 downto 0) = x"10" else --587hz Re 5
				18997 	when clk_sel(7 downto 0) = x"11" else --659hz Mi 5
				17908 	when clk_sel(7 downto 0) = x"12" else --698hz Fa 5
				15985 	when clk_sel(7 downto 0) = x"13" else --783hz Sol5
				14205 	when clk_sel(7 downto 0) = x"14" else --880hz La 5 
				12677 	when clk_sel(7 downto 0) = x"15" else --987hz Si 5						
			0;
						
						

	process(nRESET,clk)
	begin
		if nRESET = '0' then
			freq_cnt <= 0;
			piezo_clk <= '0';
		elsif clk'event and clk = '1' then
			if freq_cnt >= ref then
				freq_cnt <= 0;
				piezo_clk <= not piezo_clk;
			else
				freq_cnt <= freq_cnt + 1;
				piezo_clk <= piezo_clk;
			end if;
		end if;
	end process;

piezo <= piezo_clk;

END Behav;
