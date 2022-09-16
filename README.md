# SHA2017 Badge App Development

1. Flash latest [ESP32-platform-firmware](https://github.com/badgeteam/ESP32-platform-firmware) firmware
   > [Web flasher](https://update.bodge.team)
2. Install mpfshell-lite
   > `pip install mpfshell-lite`
3. Connect to the badge
   > `mpfs -c "open [/dev/ttyUSB0]"`
4. Run app
   > `runfile __init__.py`

# Reference

- [SHA2017 | BADGE.TEAM](https://badge.team/docs/badges/sha2017/)
- [API reference | BADGE.TEAM](https://badge.team/docs/esp32-platform-firmware/esp32-app-development/api-reference/)
- [Projects:Badge/MicroPython - SHA2017 Wiki](https://wiki.sha2017.org/w/Projects:Badge/MicroPython "Projects:Badge/MicroPython - SHA2017 Wiki")
- [mpfshell-lite/English.md at master · junhuanchen/mpfshell-lite](https://github.com/junhuanchen/mpfshell-lite/blob/master/English.md)
