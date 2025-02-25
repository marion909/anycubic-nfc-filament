# Anycubic NFC Filament

A tool to create NFC tags compatible with the Anycubic ACE Pro for third party filament spools.

## Required Hardware

The following hardware is needed (buy them via my affiliate links to support this project without additional costs):

- ACR122U NFC reader. Buy one [here](https://amzn.to/4h24oZQ) (affiliate link)
- NTAG213 NFC stickers. Buy some [here](https://amzn.to/4bgO4TR) (affiliate link)

*Note: You will need two NFC stickers per spool of filament.*

## Using the Tool

1) Make sure that python is installed on your
   computer ([Python install guide](https://realpython.com/installing-python/))
2) Make sure that a [ACR122U](https://amzn.to/4h24oZQ) (affiliate link) is connected to your computer
3) Clone this repository and go to the root directory with a shell
4) Install the requirements: `pip install -r requirements.txt`
5) Start the tool: `python -m anycubic_nfc_app`
6) Open the web interface in your browser by entering http://localhost:8080 into the top bar

## Credits

Special thanks
to [u/SnooCheesecakes1269](https://www.reddit.com/user/SnooCheesecakes1269/), [u/kivulhepy](https://www.reddit.com/user/kivulhepy/), [u/Nearby_Farmer_4983](https://www.reddit.com/user/Nearby_Farmer_4983/)
for providing me with NFC tag dumps, so I was able to reverse-engineer the format of the tags.
