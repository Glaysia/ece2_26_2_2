library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY HB_DAC is
	port(
			nRESET	: in std_logic;
			clk		: in std_logic;
			ADD_SEL	: in std_logic;
	
			DAC_CSN 	: out std_logic;
			DAC_LDACN: out std_logic;
			DAC_WEN	: out std_logic;	
			DAC_A_B 	: out std_logic;
			DAC_D		: out std_logic_vector(7 downto 0);
			LED_OUT : out std_logic_vector(7 downto 0)
		);
end HB_DAC ;

ARCHITECTURE Behav OF HB_DAC IS

signal dac_cnt : std_logic_vector(7 downto 0);
signal reg_sw_wr : std_logic_vector(1 downto 0);
signal ch_sel : std_logic;
signal cnt : integer range 0 to 99;
signal clk_cnt : std_logic;

BEGIN

	PROCESS(nRESET,clk)
	BEGIN
		IF nRESET = '1' THEN
			cnt <= 0;
			clk_cnt <= '0';
		elsif clk'event and clk = '1' then
			if cnt >= 99 then
				cnt <= 0;
				clk_cnt <= not clk_cnt;
			else
				cnt <= cnt + 1;
			end if;
		end if;
	end process;
			

	PROCESS(nRESET,clk)
	BEGIN
		IF nRESET = '1' THEN
			reg_sw_wr <= "00";
		ELSIF clk='1' AND clk'EVENT THEN
			reg_sw_wr <= reg_sw_wr(0) & clk_cnt;
		END IF;
	END PROCESS;


	PROCESS(nRESET,clk)
	BEGIN
		IF nRESET = '1' THEN
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
				
		END IF;
	END PROCESS;
	
	DAC_CSN 		<= '0';
	DAC_LDACN	<= '0';
	DAC_A_B 		<= ADD_SEL;
	DAC_D 		<= dac_cnt;
	LED_OUT 		<= dac_cnt;
	
END Behav;
