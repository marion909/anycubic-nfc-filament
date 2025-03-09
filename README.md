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

## Supporting the Research

Within the tool, you can create dumps of original Anycubic spool tags to support my research. The dump of one of the two
spool sides is enough.

You can send me your dumps via email
to [anycubic-nfc-research@molodos.com](mailto:anycubic-nfc-research@molodos.com?subject=Anycubic%20NFC%20Tag%20Research&body=Material%20(e.g.%20%22PLA%2B%22)%3A%0AColor%20(e.g.%20%22Pearl%20Black%22)%3A%0AAdditional%20information%3A%0A%0A(please%20don't%20forget%20to%20attach%20the%20dump%20file)).
Please include details on which exact spool you scanned (material, color, etc.).

Thanks for your support!

## FAQ

**Why is the material type not displaying/recognized correctly on my printer?**

Try updating your ACE Pro (you can do that on the top right of the "Workbench" in Anycubic Slicer Next)

**Why does the filament show as "?" in my slicer "Workbench" tab?**

There currently seems to be a problem with displaying some filaments in the slicer "Workbench" tab correctly. Probably
because they are not available with official RFID chips in the store yet. But: When syncing the ACE Pro in the "Prepare"
tab in your slicer, the right filament is selected.

Currently, only the following filaments are displayed correctly in the "Workbench" tab: PLA, PLA+, PLA High Speed (if
you own official spools of other types with RFID chips, create a spool dump in the application and send it to me, to
support my research and add it to the app. Read more in [this section](#supporting-the-research))

**Why is the wrong filament type selected when syncing with the ACE Pro in the "Prepare" tab?**

Make sure that the filament in the ACE Pro is available in the filament dropdown in your slicer. If not, select "
Add/Remove filament" on the bottom of the list, add the filament to the list and try syncing again.

Currently, there is another known problem where PLA+ is recognized as PLA. As I have not found a workaround yet, I
believe that it is a bug in the slicer that will also occur with official PLA+ filament from Anycubic.

## Credits

Special thanks
to [u/SnooCheesecakes1269](https://www.reddit.com/user/SnooCheesecakes1269/), [u/kivulhepy](https://www.reddit.com/user/kivulhepy/), [u/Nearby_Farmer_4983](https://www.reddit.com/user/Nearby_Farmer_4983/)
for providing me with NFC tag dumps, so I was able to reverse-engineer the format of the tags.
