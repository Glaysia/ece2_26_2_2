library ieee;
use ieee.std_logic_1164.all;
use ieee.std_logic_unsigned.all;

entity Top_xilinx is
port(
	USER_Clock	: in std_logic;
	CLK_OUT1		: in std_logic;			-- 50MHz
	
	DIP_SW		: in std_logic_vector(7 downto 0);
	Motor_CNT	: in std_logic;
	STEP_A,STEP_B,STEP_AN,STEP_BN	: out std_logic;
	LED_D			: out std_logic_vector(7 downto 0);
	AR_SEG_S	: out std_logic_vector(7 downto 0);
	AR_SEG_A,AR_SEG_B,AR_SEG_C,AR_SEG_D,AR_SEG_E,AR_SEG_F,AR_SEG_G,AR_SEG_DP	: out std_logic;
	SEG_A,SEG_B,SEG_C,SEG_D,SEG_E,SEG_F,SEG_G,SEG_DP	: out std_logic;
	tlcd_e		: out std_logic;
	tlcd_rs		: out std_logic;
	tlcd_rw		: out std_logic;
	tlcd_d		: out std_logic_vector(7 downto 0);
	PIEZO			: out std_logic;
	KEY 			: in std_logic_vector(11 downto 0);
	LED_Red		: out std_logic_vector(3 downto 0);
	LED_Green	: out std_logic_vector(3 downto 0);
	LED_Blue		: out std_logic_vector(3 downto 0);
	SERVO_CTRL	: out std_logic;
	EXT			: inout std_logic_vector(83 downto 0);

	DAC_CSN 		: out std_logic;
	DAC_LDACN	: out std_logic;
	DAC_WEN		: out std_logic;	
	DAC_A_B 		: out std_logic;
	DAC_D			: out std_logic_vector(7 downto 0);
	
	SPI_AD 	: out std_logic;
	SPI_DIN 	: out std_logic;
	SPI_DOUT : in std_logic;
	SPI_SCK 	: out std_logic;
	
	SRAM_A	: out std_logic_vector(17 downto 0);
	SRAM_D	: inout std_logic_vector(15 downto 0);
	SRAM_CSN : out std_logic;
	SRAM_OEN : out std_logic;
	SRAM_WEN : out std_logic
);
end Top_xilinx;

architecture hb of Top_xilinx is

component clk_gen
	port(
			nRESET	: in std_logic;
			CLK		: in std_logic;
			clk1kHz	: out std_logic;
			clk10kHz	: out std_logic
		);
end component;
		
component full_demo
	port(
		clk		: in std_logic;			-- 50MHz		
		button_sw	: in std_logic_vector(11 downto 0);
		dip_sw		: in std_logic_vector(7 downto 0);
		sensor		: in std_logic;		
		motor_data	: out std_logic_vector(3 downto 0);
		led			: out std_logic_vector(7 downto 0);
		sega_scan	: out std_logic_vector(7 downto 0);
		sega_data	: out std_logic_vector(7 downto 0);
		seg_data	: out std_logic_vector(7 downto 0);

        reset_out   : out std_logic;
		vfd_e		: out std_logic;
		vfd_rs		: out std_logic;
		vfd_rw		: out std_logic;
		vfd_data	: out std_logic_vector(7 downto 0)		);
end component;

signal nreset : std_logic;

component piezo_demo
	port(
			nRESET	: in std_logic;
			CLK		: in std_logic;
			sw3 		: in std_logic;
			
			piezo 	: out std_logic
		);
end component;

component seg_7_demo
	port(
			nRESET	: in std_logic;
			CLK		: in std_logic;
			sw 		: in std_logic;
			
			seg_data	: out std_logic_vector(7 downto 0)
		);
end component;

component servo_demo 
	port(
			nRESET	: in std_logic;
			clk1KHz	: in std_logic;			
			clk		: in std_logic;	-- 50MHz, 20ns
			sw_aj		: in std_logic;
			sw_r 		: in std_logic;	-- (-) right
			sw_c		: in std_logic;	-- center
			sw_l 		: in std_logic;	-- (+) left			
			servo 	: out std_logic
		);
end component;

component fled_demo
	port(
			nRESET	: in std_logic;
			clk		: in std_logic;	-- 50MHz, 20ns
			sw			: in std_logic;
			
			led_red 		: out std_logic_vector(3 downto 0);
			led_green 	: out std_logic_vector(3 downto 0);			
			led_blue 	: out std_logic_vector(3 downto 0)

		);	
end component;


component traffic_demo
	PORT(
			clk		: in std_logic;                     -- 10khz clock
			flicker : in std_logic;
			flick_sw : in std_logic;
--			red		: out std_logic_vector(3 downto 0); -- south, west, east, north
--			yellow	: out std_logic_vector(3 downto 0);
--			green	: buffer std_logic_vector(3 downto 0);
--			left_o	: out std_logic_vector(3 downto 0);
--			walk_r	: out std_logic_vector(3 downto 0);
--			walk_g	: out std_logic_vector(3 downto 0);
			EXT_63_40 : out std_logic_vector(23 downto 0)
	);
end component;

component dac_demo
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
end component;

component adc_demo
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
end component;

signal motor_data : std_logic_vector(3 downto 0);
signal ar_seg_data : std_logic_vector(7 downto 0);
signal seg_data : std_logic_vector(7 downto 0);

signal clk1kHz,clk10kHz : std_logic;
signal led: std_logic_vector(7 downto 0);
signal PIEZO_sig : std_logic;
	
signal test_cnt : std_logic_vector(19 downto 0);

signal COMMON,SEGMENT : std_logic_vector(7 downto 0);
signal RED, GREEN, YELLOW, LEFT_O, WALK_G, WALK_R: std_logic_vector(3 downto 0);
signal traffic_clk : std_logic;

signal ACD_0CH	:  std_logic_vector(7 downto 0);
signal ACD_1CH	:  std_logic_vector(7 downto 0);
signal ACD_2CH	:  std_logic_vector(7 downto 0);
signal ACD_3CH	:  std_logic_vector(7 downto 0);
signal ACD_4CH	:  std_logic_vector(7 downto 0);
signal ACD_5CH	:  std_logic_vector(7 downto 0);
signal ACD_6CH	:  std_logic_vector(7 downto 0);
signal ACD_7CH	:  std_logic_vector(7 downto 0);
signal dac_ref : std_logic_vector(7 downto 0);
		
begin

	SRAM_A	<= "000000000000000000";--: out std_logic_vector(17 downto 0);
	SRAM_D	<= x"0000";--: inout std_logic_vector(15 downto 0);
	SRAM_CSN <= '1';--: out std_logic;
	SRAM_OEN <= '1';--: out std_logic;
	SRAM_WEN <= '1';--: out std_logic

	LED_D <= led(7 downto 0);
--	LED_D <= ACD_1CH;
	
	dac_ref <= x"00" when (ACD_0CH - x"6b") <= x"00" else ACD_0CH - x"6b";
	DAC_D <= x"4A" - ('0' & dac_ref(7 downto 1));
	
	PIEZO <= PIEZO_sig;
	STEP_A <= motor_data(0);
	STEP_B <= motor_data(1);
	STEP_AN <= motor_data(2);
	STEP_BN <= motor_data(3);
	
	AR_SEG_A <= ar_seg_data(7);
	AR_SEG_B <= ar_seg_data(6);
	AR_SEG_C <= ar_seg_data(5);
	AR_SEG_D <= ar_seg_data(4);
	AR_SEG_E <= ar_seg_data(3);
	AR_SEG_F <= ar_seg_data(2);
	AR_SEG_G <= ar_seg_data(1);
	AR_SEG_DP <= ar_seg_data(0);
	
	SEG_A <= seg_data(7);
	SEG_B <= seg_data(6);
	SEG_C <= seg_data(5);
	SEG_D <= seg_data(4);
	SEG_E <= seg_data(3);
	SEG_F <= seg_data(2);
	SEG_G <= seg_data(1);
	SEG_DP <= seg_data(0);

clock : clk_gen
port map(
	nRESET	=> nreset,
	CLK		=> CLK_OUT1,
	clk1kHz	=> clk1kHz,
	clk10kHz => clk10kHz
	);
	
demo1 : full_demo
port map(
	clk => CLK_OUT1,
	button_sw 	=> key,
	dip_sw 		=> DIP_SW,
	sensor 		=> Motor_CNT,
	motor_data	=> motor_data,
	led 			=> led,
	sega_scan 	=> AR_SEG_S,
	sega_data	=> ar_seg_data,
--	seg_data 	=> seg_data,
    reset_out => nreset,
	vfd_e			=> tlcd_e,
	vfd_rs		=> tlcd_rs,
	vfd_rw		=> tlcd_rw,
	vfd_data		=> tlcd_d
	);

demo2 : piezo_demo
port map(
	nRESET	=> nreset,
	CLK		=> CLK_OUT1,
	sw3 		=> KEY(2),			
	piezo 	=> PIEZO_sig
	);

demo3 : seg_7_demo
port map(
	nRESET	=> nreset,
	CLK		=> clk1kHz,
	sw 		=> KEY(0),
	seg_data	=> seg_data
	);

demo4 : servo_demo
port map(
	nRESET	=> nreset,
	clk1KHz	=> clk1kHz,
	clk		=> CLK_OUT1,
	sw_aj		=> key(1),
	sw_r 		=> key(5),	-- (-) right
	sw_c 		=> key(4),	-- (+) left	
	sw_l 		=> key(3),	-- (+) left			
	servo 	=> SERVO_CTRL
		);

demo5 : fled_demo
port map(
			nRESET	=> nreset,
			clk		=> CLK_OUT1,
			sw			=> KEY(11),
			
			led_red 		=> LED_Red,
			led_green 	=> LED_Green,
			led_blue 	=> LED_Blue
		);

--traffic_clk <= clk10kHz and KEY(6);
		
demo6 : traffic_demo 
port map(
		clk 		=> clk10kHz,
		flicker 	=> KEY(7),
		flick_sw => KEY(8),
--		red		=> RED,
--		yellow	=> YELLOW,
--		green		=> GREEN,
--		left_o	=> LEFT_O,
--		walk_r	=> WALK_R,
--		walk_g	=> WALK_G,
		EXT_63_40 => EXT(63 downto 40)
	);

demo7 : dac_demo
port map(
			nRESET	 => nreset,
			clk		 => clk10kHz,
			clk1kHz	 => clk1kHz,
			sw_sel	 => KEY(10),
	
			DAC_CSN 	 => DAC_CSN,
			DAC_LDACN => DAC_LDACN,
			DAC_WEN	 => DAC_WEN,
			DAC_A_B 	 => DAC_A_B
--			DAC_D		 => DAC_D
		);

demo8 : adc_demo
port map(
			nRESET	=> nreset,
			clk		=> CLK_OUT1,
			ADC_SCLK	=> SPI_SCK,
			ADC_nCS	=> SPI_AD,
			ACD_DIN	=> SPI_DIN,
			ADC_DOUT	=> SPI_DOUT,
			
			ACD_0CH	=> ACD_0CH,
			ACD_1CH	=> ACD_1CH,
			ACD_2CH	=> ACD_2CH,
			ACD_3CH	=> ACD_3CH,
			ACD_4CH	=> ACD_4CH,
			ACD_5CH	=> ACD_5CH,
			ACD_6CH	=> ACD_6CH,
			ACD_7CH	=> ACD_7CH
		);


end hb;