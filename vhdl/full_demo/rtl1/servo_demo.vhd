library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY servo_demo is
	port(
			nRESET	: in std_logic:='1';
			clk1KHz	: in std_logic;			
			clk		: in std_logic;	-- 50MHz, 20ns
			sw_aj		: in std_logic;
			sw_r 		: in std_logic;	-- (-) right
			sw_c		: in std_logic;	-- center
			sw_l 		: in std_logic;	-- (+) left			
			servo 	: out std_logic
		);
end servo_demo ;

ARCHITECTURE Behav OF servo_demo IS

signal clk_cnt : std_logic_vector(2 downto 0);
signal reg_sw_r,reg_sw_l : std_logic_vector(1 downto 0);

signal width_cnt : integer range 0 to 1000000;
signal ref_cnt,ref_value,ref_int : integer range 0 to 119999; 
signal freq_cnt : integer range 0 to 119999;

signal sw_r_clk, sw_l_clk : std_logic;

type state_type is (s0,s1,s2,s3);
signal state   : state_type;

BEGIN

	sw_r_clk <= (clk_cnt(1) and sw_r) when sw_aj = '0' else sw_r;
	sw_l_clk <= (clk_cnt(1) and sw_l) when sw_aj = '0' else sw_l;

	PROCESS(nRESET,clk1KHz)
	BEGIN
		IF nRESET = '0' THEN
			clk_cnt <= "000";
		ELSIF clk1KHz='1' AND clk1KHz'EVENT THEN
			clk_cnt <= clk_cnt + 1;
		END IF;
	END PROCESS;

	PROCESS(nRESET,CLK)
	BEGIN
		IF nRESET = '0' THEN
			reg_sw_r <= "00";
			reg_sw_l <= "00";
		ELSIF CLK='1' AND CLK'EVENT THEN
			reg_sw_r <= reg_sw_r(0) & sw_r_clk;
			reg_sw_l <= reg_sw_l(0) & sw_l_clk;
		END IF;
	END PROCESS;

	PROCESS(nRESET,CLK)
	BEGIN
		IF nRESET = '0' THEN
			width_cnt <= 0;
			servo <= '0';
		ELSIF CLK='1' AND CLK'EVENT THEN
			if width_cnt >= 1000000 then		-- 20ms
				width_cnt <= 0;
			else
				width_cnt <= width_cnt + 1;
			end if;
			
			if width_cnt <= ref_value then
				servo <= '1';
			else
				servo <= '0';
			end if;
			
		END IF;
	END PROCESS;

	PROCESS(nRESET,CLK)
	BEGIN
		IF nRESET = '0' THEN
			ref_cnt <= 74999;						-- center 0 degree
		ELSIF CLK='1' AND CLK'EVENT THEN
			if state = s2 then
				ref_cnt <= 74999;
			else
				if sw_c = '1' then
					ref_cnt <= 74999;	
				elsif reg_sw_l = "01" then
					if ref_cnt <= 29999 then		-- right 90 degree
						ref_cnt <= 29999;
					else
						ref_cnt <= ref_cnt - 499;	-- move right 1 degree
					end if;
				elsif reg_sw_r = "01" then
					if ref_cnt >= 119999 then		-- left 90 degree
						ref_cnt <= 119999;
					else
						ref_cnt <= ref_cnt + 499;	-- move left 1 degree
					end if;
				end if;
			end if;
		END IF;
	END PROCESS;	

	--- Demo state
	process (nRESET, clk_cnt(1))
	begin
		if nRESET = '0' then
			state <= s0;
			ref_int <= 0;
		elsif (rising_edge(clk_cnt(1))) then
			case state is
				when s0 =>
					if ref_int = 29999 then
						state <= s1;
					end if;
					
					if ref_int <= 29999 then
						ref_int <= 29999;
					else
						ref_int <= ref_int - 499;
					end if;
					
					ref_value <= ref_int;
					
				when s1 =>
					if ref_int = 119999 then
						state <= s2;
					end if;
					
					if ref_int >= 119999 then
						ref_int <= 119999;
					else
						ref_int <= ref_int + 499;
					end if;
					
					ref_value <= ref_int;

				when s2 =>
					if ref_int = 74999 then
						state <= s3;
					end if;
					
					if ref_int <= 74999 then
						ref_int <= 74999;
					else
						ref_int <= ref_int - 444;
					end if;
					
					ref_value <= ref_int;

				when s3 => 
						ref_int <= ref_int;
						ref_value <= ref_cnt;
			
				when others => null;
			end case;
		end if;
	end process;
	
END Behav;
