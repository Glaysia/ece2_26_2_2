library ieee;
use ieee.std_logic_1164.all;
USE IEEE.STD_LOGIC_UNSIGNED.ALL;

ENTITY fled_demo is
	port(
			nRESET	: in std_logic;
			clk		: in std_logic;	-- 50MHz, 20ns
			sw			: in std_logic;
			
			led_red 		: out std_logic_vector(3 downto 0);
			led_green 	: out std_logic_vector(3 downto 0);
			led_blue 	: out std_logic_vector(3 downto 0)
		);
end fled_demo ;

ARCHITECTURE Behav OF fled_demo IS

component fled_pwm_ctrl 
	port(
			nRESET	: in std_logic;
			clk1kHz	: in std_logic;			
			ref		: in std_logic_vector(7 downto 0);	-- pwm duty
			led_out	: out std_logic							-- pwm out
		);
end component ;

signal clk_cnt : integer range 0 to 2500;
signal clk_cntA : integer range 0 to 250000;
signal duty_cnt : std_logic_vector(8 downto 0);
signal clk100kHz,clk1kHz,clk100Hz,clk200Hz,f_clk : std_logic;

type state_type is (s0,s1,s2,s3,s4,s5,s6,s7,s8,s9);
signal state   : state_type;
attribute syn_encoding : string;
attribute syn_encoding of state_type : type is "safe";
	
signal R_ref,G_ref,B_ref,dly_ref : std_logic_vector(7 downto 0);
	
BEGIN

	PROCESS(nRESET,clk)
	BEGIN
		IF nRESET = '0' THEN
			clk_cnt <= 0;
			clk100kHz <= '0';
		ELSIF clk='1' AND clk'EVENT THEN
			if clk_cnt >= 250 then
				clk_cnt <= 0;
				clk100kHz <= not clk100kHz;
			else
				clk_cnt <= clk_cnt + 1;
			end if;
		END IF;
	END PROCESS;

	f_clk <= clk100Hz;-- and sw;
	
	PROCESS(nRESET,clk)
	BEGIN
		IF nRESET = '0' THEN
			clk_cntA <= 0;
			clk100Hz <= '0';
		ELSIF clk='1' AND clk'EVENT THEN
			if clk_cntA >= 120000 then
				clk_cntA <= 0;
				clk100Hz <= not clk100Hz;
			else
				clk_cntA <= clk_cntA + 1;
			end if;
		END IF;
	END PROCESS;	

--- Demo state
	process (nRESET, f_clk)
	begin
		if nRESET = '0' then
			state <= s0;
			R_ref <= x"00";
			G_ref <= x"00";
			B_ref <= x"00";
			dly_ref <= x"00";
		elsif (rising_edge(f_clk)) then
			case state is
				when s0 =>
					state <= s1;
				when s1 =>	--red
					if R_ref = x"FF" and G_ref = x"00" and B_ref = x"00" then
						state <= s2;
					end if;
					
					if R_ref = x"FF" then
						R_ref <= x"FF";
					else
						R_ref <= R_ref + 1;
					end if;

					if G_ref = x"00" then
						G_ref <= x"00";
					else
						G_ref <= G_ref - 1;
					end if;

					if B_ref = x"00" then
						B_ref <= x"00";
					else
						B_ref <= B_ref - 1;
					end if;
					
				when s2 =>	--orange
					if R_ref <= x"FF" and G_ref = x"7F" and B_ref = x"00" and dly_ref = x"FF" then
						state <= s3;
					end if;

					if R_ref = x"FF" then
						R_ref <= x"FF";
					else
						R_ref <= R_ref + 1;
					end if;

					if G_ref = x"7F" then
						G_ref <= x"7F";
					else
						G_ref <= G_ref + 1;
					end if;

					if B_ref = x"00" then
						B_ref <= x"00";
					else
						B_ref <= B_ref - 1;
					end if;
					
					if dly_ref = x"FF" then
						dly_ref <= x"FF";
					else
						dly_ref <= dly_ref + 1;
					end if;
					
				when s3 =>	--yellow
					if R_ref <= x"FF" and G_ref = x"FF" and B_ref = x"00" and dly_ref = x"00" then
						state <= s4;
					end if;

					if R_ref = x"FF" then
						R_ref <= x"FF";
					else
						R_ref <= R_ref + 1;
					end if;

					if G_ref = x"FF" then
						G_ref <= x"FF";
					else
						G_ref <= G_ref + 1;
					end if;

					if B_ref = x"00" then
						B_ref <= x"00";
					else
						B_ref <= B_ref - 1;
					end if;

					if dly_ref = x"00" then
						dly_ref <= x"00";
					else
						dly_ref <= dly_ref - 1;
					end if;
					
				when s4 =>	--green
					if R_ref <= x"00" and G_ref = x"FF" and B_ref = x"00" then
						state <= s5;
					end if;

					if R_ref = x"00" then
						R_ref <= x"00";
					else
						R_ref <= R_ref - 1;
					end if;

					if G_ref = x"FF" then
						G_ref <= x"FF";
					else
						G_ref <= G_ref + 1;
					end if;

					if B_ref = x"00" then
						B_ref <= x"00";
					else
						B_ref <= B_ref - 1;
					end if;
					
				when s5 =>	--blue
					if R_ref <= x"00" and G_ref = x"00" and B_ref = x"FF" then
						state <= s6;
					end if;

					if R_ref = x"00" then
						R_ref <= x"00";
					else
						R_ref <= R_ref - 1;
					end if;

					if G_ref = x"00" then
						G_ref <= x"00";
					else
						G_ref <= G_ref - 1;
					end if;

					if B_ref = x"FF" then
						B_ref <= x"FF";
					else
						B_ref <= B_ref + 1;
					end if;
					
				when s6 =>	-- navy blue
					if R_ref <= x"00" and G_ref = x"00" and B_ref = x"7F" and dly_ref = x"FF" then
						state <= s7;
					end if;

					if R_ref = x"00" then
						R_ref <= x"00";
					else
						R_ref <= R_ref - 1;
					end if;

					if G_ref = x"00" then
						G_ref <= x"00";
					else
						G_ref <= G_ref - 1;
					end if;

					if B_ref = x"7F" then
						B_ref <= x"7F";
					else
						B_ref <= B_ref - 1;
					end if;

					if dly_ref = x"FF" then
						dly_ref <= x"FF";
					else
						dly_ref <= dly_ref + 1;
					end if;
					
				when s7 => -- violet
					if R_ref <= x"7F" and G_ref = x"00" and B_ref = x"FF" and dly_ref = x"00" then
						state <= s8;
					end if;

					if R_ref = x"7F" then
						R_ref <= x"7F";
					else
						R_ref <= R_ref + 1;
					end if;

					if G_ref = x"00" then
						G_ref <= x"00";
					else
						G_ref <= G_ref - 1;
					end if;

					if B_ref = x"FF" then
						B_ref <= x"FF";
					else
						B_ref <= B_ref + 1;
					end if;

					if dly_ref = x"00" then
						dly_ref <= x"00";
					else
						dly_ref <= dly_ref - 1;
					end if;
					
				when s8 =>
					if R_ref <= x"FF" and G_ref = x"FF" and B_ref = x"FF" then
						state <= s9;
					end if;

					if R_ref = x"FF" then
						R_ref <= x"FF";
					else
						R_ref <= R_ref + 1;
					end if;

					if G_ref = x"FF" then
						G_ref <= x"FF";
					else
						G_ref <= G_ref + 1;
					end if;

					if B_ref = x"FF" then
						B_ref <= x"FF";
					else
						B_ref <= B_ref + 1;
					end if;

				when s9 =>
					if R_ref <= x"00" and G_ref = x"00" and B_ref = x"00" then
						state <= s0;
					end if;

					if R_ref = x"00" then
						R_ref <= x"00";
					else
						R_ref <= R_ref - 1;
					end if;

					if G_ref = x"00" then
						G_ref <= x"00";
					else
						G_ref <= G_ref - 1;
					end if;

					if B_ref = x"00" then
						B_ref <= x"00";
					else
						B_ref <= B_ref - 1;
					end if;
					
				when others => null;
			end case;
		end if;
	end process;
---------------	
	
	
	
-- Full color LED 1
pwm_ctrl1 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> R_ref,
			led_out	=> led_red(0)
		);
pwm_ctrl5 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> G_ref,
			led_out	=> led_green(0)
			);
pwm_ctrl9 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> B_ref,
			led_out	=> led_blue(0)
			);
			
-- Full color LED 2			
pwm_ctrl2 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> R_ref,
			led_out	=> led_red(1)
		);
pwm_ctrl6 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> G_ref,
			led_out	=> led_green(1)
		);			
pwm_ctrl10 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> B_ref,
			led_out	=> led_blue(1)
		);

-- Full color LED 4	
pwm_ctrl8 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> R_ref,
			led_out	=> led_red(3)
		);
pwm_ctrl12 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> G_ref,
			led_out	=> led_green(3)
		);
pwm_ctrl4 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> B_ref,
			led_out	=> led_blue(3)
		);
		
-- Full color LED 3			
pwm_ctrl3 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> R_ref,
			led_out	=> led_red(2)
		);
pwm_ctrl7 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> G_ref,
			led_out	=> led_green(2)
		);
pwm_ctrl11 : fled_pwm_ctrl
port map(
			nRESET	=> nRESET,
			clk1kHz	=> clk100kHz,			
			ref		=> B_ref,
			led_out	=> led_blue(2)			
		);			


		
END Behav;
