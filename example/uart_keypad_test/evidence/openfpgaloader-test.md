# openFPGALoader hardware test — 2026-09-14

Result: FPGA detection and SRAM programming did not succeed with the attached Xilinx USB cable on Windows. No bitstream was programmed by openFPGALoader.

- Attached cable: USB VID 03FD / PID 0008, Xilinx WinUSB driver (oem64.inf).
- MSYS2 mingw64 openFPGALoader 1.0.0 installed. Its cable list lacks Xilinx Platform Cable support; default detection attempts FT2232 and fails.
- Upstream source: https://github.com/trabucayre/openFPGALoader at dafa7fcab2b96e927fd3108c3f33d1cc46117c8b, reports v1.1.1. Native build in `../build/openfpgaloader-native`, source in `../build/openfpgaloader-src`.
- Built with Xilinx FPGA and Xilinx Platform Cable support, using installed libusb 1.0.30. Probe firmware argument: `C:/AMDDesignTools/2026.1/Vivado/data/xicom/xusb_xp2.hex`.
- Initial attempt: access denied while Vivado hw_server was running. Stopped that server; cable access then worked.
- Unmodified upstream attempt: alternate interface 1 returns LIBUSB_ERROR_IO, bulk write returns LIBUSB_ERROR_NOT_FOUND, invalid IDCODE 0x00000022 (not the FPGA's identity).
- Read-only USB descriptors: configuration 2, interface 0, alternate setting 0, endpoints 02/86. Only alternate setting 0 advertised.
- Diagnostic local source change: `set_interface_alt_setting(0, 1)` changed to `(0, 0)` in xilinxPlatformCableUsb.cpp. Rebuilt attempt fails reading constant with LIBUSB_ERROR_TIMEOUT. This is an experimental build, not a validated fix.
- Windows device restart via pnputil was denied by the OS. No driver was replaced.
- Follow-up Vivado read-only probe also failed: no active target, jsn1 may be locked by another hw_server. After the probe, no hw_server/openFPGALoader process remained, while Windows still showed the Xilinx cable as OK. USB unplug/replug is needed before retesting to restore a fresh cable state.

Do not label this cable/environment as tested working with openFPGALoader. The Windows USB/firmware interaction needs further investigation; results do not establish that other OS/cable combinations fail.

## Retry after physical USB reconnect

- Fresh connection enumerated as 03FD:0013, Xilinx Platform Cable USB II Firmware Loader.
- openFPGALoader reported firmware transfer Done, but 100-second re-enumeration wait failed; Windows remained at PID 0013. See openfpgaloader-retry-detect.txt.
- Vivado read-only probe then initialized the cable and correctly detected xc7s75_0. Cable became PID 0008.
- Diagnostic build changed again: omitted set_interface_alt_setting entirely, retaining Windows' existing alternate setting. This is a local experimental patch.
- Following initialization, openFPGALoader could read cable version/status and issue USB transfers. At 6 MHz no FPGA was listed. Verbose 750 kHz retry explicitly returned `found 0 devices`, despite exit code 0. See openfpgaloader-retry-initialized.txt and openfpgaloader-retry-slow.txt.
- No valid FPGA IDCODE was obtained; no FPGA bitstream programming was attempted. No Windows driver replacement was performed.
