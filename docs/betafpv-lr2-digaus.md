# BETAFPV LiteRadio2 (digaus mod) on EdgeTX

This fork applies digaus' OpenTX LiteRadio2 modifications to EdgeTX `main` and
adds a dedicated `LR2` build target for the BetaFPV LiteRadio2 hardware mod.

## Attribution

- EdgeTX: https://github.com/EdgeTX/edgetx
- Original OpenTX fork and commits: https://github.com/digaus/opentx (branch `BetaFPV`)
- RC Groups post describing the hardware mods and rationale:
  https://www.rcgroups.com/forums/showthread.php?3660773-BetaFPV-LiteRadio2-advanced-modifications#post45024673

## Hardware mod summary (from RC Groups post)

1) 2S Li-Ion battery mod (18500 cells) for longer runtime.
2) 1.3" OLED (SH1106, 128x64) plus navigation buttons to replace the rotary
   encoder; OLED needs a 2px offset and inverted segment/com to avoid the
   mirrored image and left-side bar.
3) External module telemetry mod using TELEMETRY_DIR control for S.PORT.
4) No SD card present on LiteRadio2, so firmware should not block on SD detect.

## Firmware changes applied in this fork

- Added a LiteRadio2 build target: `-DPCB=X7 -DPCBREV=LR2` with `RADIO_LR2`.
- OLED handling for SH1106: 2px column offset in `lcdRefresh`.
- Navigation uses KEY_PLUS / KEY_MINUS for page stepping on LR2.
- Telemetry direction set to match the external module mod wiring.
- SD card presence forced true to avoid boot-time SD detection failures.

## Build (Windows, portable toolchain)

1) Ensure `cmake`, `ninja`, and `arm-none-eabi-gcc` are on your PATH.
2) From the repo root, run:

```powershell
python tools\build-betafpv.py -b LR2 -t EN Z:\edgetx-lr2-digaus-mod
```

The firmware is written under `output/` with a timestamped name like:
`output\firmware_lr2_en_YYMMDD.bin`.

## Flashing notes

Per the RC Groups post, flash as bootloader to ensure the boot menu is correct.
Hold the internal boot button while powering on to enter bootloader mode, then
flash with EdgeTX Companion (or other preferred flashing tool).
