library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY dac_demo is
	port(
			nRESET	: in std_logic;
			clk		: in std_logic;
			clk1kHz	: in std_logic;
			sw_sel	: in std_logic;
	
			DAC_CSN 	: out std_logic;
			DAC_LDACN: out std_logic;
			DAC_WEN	: out std_logic;	
			DAC_A_B 	: out std_logic;
			DAC_D		: out std_logic_vector(7 downto 0)
		);
end dac_demo ;

ARCHITECTURE Behav OF dac_demo IS

signal dac_cnt : std_logic_vector(7 downto 0);
signal reg_sw_wr, reg_sw_sel : std_logic_vector(1 downto 0);
signal ch_sel : std_logic;

BEGIN

	PROCESS(nRESET,clk)
	BEGIN
		IF nRESET = '0' THEN
			reg_sw_wr <= "00";
			reg_sw_sel <= "00";
		ELSIF clk='1' AND clk'EVENT THEN
			reg_sw_wr <= reg_sw_wr(0) & clk1kHz;
			reg_sw_sel <= reg_sw_sel(0) & sw_sel;
		END IF;
	END PROCESS;


	PROCESS(nRESET,clk)
	BEGIN
		IF nRESET = '0' THEN
			dac_cnt <= x"00";
			DAC_WEN <= '1';
			ch_sel <= '0';
		ELSIF clk='1' AND clk'EVENT THEN
			if reg_sw_wr = "01" then
				dac_cnt <= dac_cnt + 1;
			end if;
			
			if reg_sw_wr = "10" then
				DAC_WEN <= '0';
			else
				DAC_WEN <= '1';
			end if;
			
			if reg_sw_sel = "01" then
				ch_sel <= not ch_sel;
			end if;
				
		END IF;
	END PROCESS;
	
	DAC_CSN 		<= '0';
	DAC_LDACN	<= '0';
	DAC_A_B 		<= ch_sel;
	DAC_D 		<= dac_cnt;
	
END Behav;
