Download 

https://sylvan.apple.com/Aerials/resources.tar

Inside the tar file, extract `entries.json` to current directory.

Parse json to txt and csv files: `parse_entries.json`

Download videos using aria:

aria2c --check-certificate=false -i urls_aria.txt -c -d ./apple_4k_screensaver_videos/


Subtitles / points of interest:

In the `resources.tar` file, extract `./TVIdleScreenStrings.bundle/en_GB.lproj/Localizable.nocache.strings`.

Convert this file to "strings.xml" and put in current directory.

https://localise.biz/free/converter/ios-to-android

Run `parse_sub_strings.py` to convert `strings.xml` to `sub_strings.json`.

Run `make_subs.py` to convert `sub_strings.json` to `.srt` subtitles files inthe  directory './subs/'.


-------------

also see: https://gist.github.com/dmn001/471efcecc19bfb9be7a8575a557162b7