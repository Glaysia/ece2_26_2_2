library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY adc_demo is
	port(
			nRESET	: in std_logic;
			clk		: in std_logic;
			
			ADC_SCLK	: out std_logic;
			ADC_nCS	: out std_logic;
			ACD_DIN	: out std_logic;
			ADC_DOUT	: in std_logic;
			
			ACD_0CH	: out std_logic_vector(7 downto 0);
			ACD_1CH	: out std_logic_vector(7 downto 0);
			ACD_2CH	: out std_logic_vector(7 downto 0);
			ACD_3CH	: out std_logic_vector(7 downto 0);
			ACD_4CH	: out std_logic_vector(7 downto 0);
			ACD_5CH	: out std_logic_vector(7 downto 0);
			ACD_6CH	: out std_logic_vector(7 downto 0);
			ACD_7CH	: out std_logic_vector(7 downto 0);
			clk_out	: out std_logic
			
		);
end adc_demo ;

ARCHITECTURE Behav OF adc_demo IS

signal clk_cnt : std_logic_vector(1 downto 0);
signal cs_cnt : std_logic_vector(4 downto 0);
signal sclk,rclk : std_logic;
signal cs_start,cs_start_s,cs,ctrl_sreg,ctrl_sreg_dummy : std_logic;
signal out_buf : std_logic_vector(15 downto 0);
signal real_t_cnt : std_logic_vector(5 downto 0);
signal cs_start_cnt : std_logic_vector(3 downto 0);
signal add : std_logic_vector(2 downto 0);


BEGIN

clk_out <= clk;

	process(nRESET,cs_start_s)
	begin
		if nRESET = '0' then
			cs_start_cnt <= "0000";
		elsif cs_start_s'event and cs_start_s = '0' then
				if cs_start_cnt >= "0111" then
					cs_start_cnt <= "0001";
				else
					cs_start_cnt <= cs_start_cnt + 1;
				end if;
		end if;
	end process;
	
	process(CLK)
	begin
		if clk'event and clk = '1' then
			if cs_start_cnt	>= "0001" and cs_start_cnt <= "0111" then
				cs_start	<= cs_start_s;
			else
				cs_start	<= '1';
			end if;
		end if;
	end process;		

	process(nRESET,rclk)
	begin
		if nRESET = '0' then
			real_t_cnt <= "000000";
		elsif rclk'event and rclk = '1' then
			if real_t_cnt >= "101000" then
				real_t_cnt <= "000000";
			else
				real_t_cnt <= real_t_cnt + 1;
			end if;
		end if;
	end process;
	
	process(rclk,nRESET)
	begin
		if nRESET = '0' then
			cs_start_s <= '1';
		elsif rclk'event and rclk = '1' then
			if real_t_cnt >= "000001" and real_t_cnt <= "000010" then
				cs_start_s <= '0';
			else
				cs_start_s <= '1';
			end if;
		end if;
	end process;
				

-------------------------------------------------------------------------
-- ADC CS Generator
-------------------------------------------------------------------------
	process(nRESET,CLK)
	begin
		if nRESET = '0' then
			clk_cnt <= "00";
		elsif clk'event and clk = '1' then
			clk_cnt <= clk_cnt + 1;
		end if;
	end process;

	rclk <= clk_cnt(1);
		
	process(nRESET,rclk)
	begin
		if nRESET = '0' then
			cs_cnt <= "10010";		
		elsif rclk'event and rclk = '1' then
			if cs_start = '0' then
				cs_cnt <= "00000";
			else
				if cs_cnt >= "10001" then
					cs_cnt <= "10010";
				else
					cs_cnt <= cs_cnt + 1;
				end if;
			end if;
		end if;
	end process;

	process(CLK)
	begin
		if clk'event and clk = '1' then
			if cs_cnt	>= "00001" and cs_cnt <= "10000" then
				sclk	<= rclk;
			else
				sclk	<= '1';
			end if;
		end if;
	end process;

	process(CLK)
	begin
		if clk'event and clk = '1' then
			if cs_cnt	>= "00001" and cs_cnt <= "10001" then
				cs 		<= '0';
			else
				cs 		<= '1';
			end if;
		end if;
	end process;
------------------------------------------------------------------------
-- Control Register configuration
------------------------------------------------------------------------

	add <= 	"000" when cs_start_cnt = "0001" else
			"001" when cs_start_cnt = "0010" else
			"010" when cs_start_cnt = "0011" else
			"011" when cs_start_cnt = "0100" else
			"100" when cs_start_cnt = "0101" else
			"101" when cs_start_cnt = "0110" else
			"111";

	ctrl_sreg_dummy <= '1';
	
	ctrl_sreg <= 	'1' when cs_cnt = "00001" else		-- 11) write en '1' write, '0' read
						'0' when cs_cnt = "00010" else	 	-- 10) SEQ
						'1' when cs_cnt = "00011" else	 	-- 09) Don't care
						add(2) when cs_cnt = "00100" else	-- 08) ADD 2
						add(1) when cs_cnt = "00101" else	-- 07) ADD 1
						add(0) when cs_cnt = "00110" else	-- 06) ADD 0
						'1' when cs_cnt = "00111" else	 	-- 05) PM 1
						'1' when cs_cnt = "01000" else		-- 04) PM 0
						'0' when cs_cnt = "01001" else		-- 03) SHADOW
						'1' when cs_cnt = "01010" else		-- 02) Don't care
						'1' when cs_cnt = "01011" else	 	-- 01) RANGE
						'1' when cs_cnt = "01100" else	 	-- 00) CODING
						'1';

	process(CLK)
	begin
		if CLK'event and CLK = '1' then
			if cs_start_cnt = "000" then
				ACD_DIN <= ctrl_sreg_dummy;
			else
				ACD_DIN <= ctrl_sreg;
			end if;
		end if;
	end process;
			
------------------------------------------------------------------------
-- Data input
------------------------------------------------------------------------
	process(sclk)
	begin
		if sclk'event and sclk = '0' then
			out_buf <= out_buf(14 downto 0) & ADC_DOUT;--'0';
--			out_buf(0) <= ADC_DOUT;
		end if;
	end process;

	process(nRESET,clk)
	begin
		if nRESET = '0' then
			ACD_0CH <= (others => '0');
			ACD_1CH <= (others => '0');
			ACD_2CH <= (others => '0');
			ACD_3CH <= (others => '0');
			ACD_4CH <= (others => '0');
			ACD_5CH <= (others => '0');
			ACD_6CH <= (others => '0');
			ACD_7CH <= (others => '0');			
		elsif clk'event and clk = '1' then
			if cs_start_cnt = "0000" then
				ACD_0CH <= (others => '0');
				ACD_1CH <= (others => '0');
				ACD_2CH <= (others => '0');
				ACD_3CH <= (others => '0');
				ACD_4CH <= (others => '0');
				ACD_5CH <= (others => '0');
				ACD_6CH <= (others => '0');
				ACD_7CH <= (others => '0');	
			else
				if cs_cnt = "10001" then
					case out_buf(15 downto 12) is
						when "0000" => ACD_0CH <=out_buf(11 downto 4);
						when "0001" => ACD_1CH <=out_buf(11 downto 4);
						when "0010" => ACD_2CH <=out_buf(11 downto 4);
						when "0011" => ACD_3CH <=out_buf(11 downto 4);
						when "0100" => ACD_4CH <=out_buf(11 downto 4);
						when "0101" => ACD_5CH <=out_buf(11 downto 4);
						when "0110" => ACD_6CH <=out_buf(11 downto 4);
						when "0111" => ACD_7CH <=out_buf(11 downto 4);
						when others => null;
					end case;
				end if;
			end if;
		end if;
	end process;

		
	ADC_SCLK	<=	sclk;
	ADC_nCS	<=	cs;
	
END Behav;
