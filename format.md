# Anycubic NFC Format

## Version 1

> Byte order is big endian

Dump of the NTAG213 chip of a Pantone Spring Leaf PLA

```
[Page 00] 53:4e:63:f6 (Management data)
[Page 01] d4:72:00:01 (Management data)
[Page 02] a7:48:00:00 (Management data)
[Page 03] e1:10:12:00 (Management data)
[Page 04] 7b:00:64:00 -> Format version information (64 -> version 1)
[Page 05] 48:50:4c:31 -> SKU: HPL19-102 (max length might be longer -> check firmware)
[Page 06] 39:2d:31:30 -> ^^
[Page 07] 32:00:00:00 -> ^^
[Page 08] 00:00:00:00
[Page 09] 00:00:00:00
[Page 0a] 00:00:00:00
[Page 0b] 00:00:00:00
[Page 0c] 00:00:00:00
[Page 0d] 00:00:00:00
[Page 0e] 00:00:00:00
[Page 0f] 50:4c:41:00 -> Type: PLA
[Page 10] 00:00:00:00
[Page 11] 00:00:00:00
[Page 12] 00:00:00:00
[Page 13] 00:00:00:00
[Page 14] ff:4f:a8:89 -> Color: #89a84f (opacity: 0xff)
[Page 15] 00:00:00:00
[Page 16] 00:00:00:00
[Page 17] 00:00:00:00
[Page 18] c8:00:d2:00 -> Nozzle temp range: 200-210°C
[Page 19] 00:00:00:00
[Page 1a] 00:00:00:00
[Page 1b] 00:00:00:00
[Page 1c] 00:00:00:00
[Page 1d] 32:00:3c:00 -> Bed temp range: 50-60°C
[Page 1e] af:00:4a:01 -> Diameter and length: 175x10^-2mm, 330m
[Page 1f] e8:03:00:00 -> Weight: 1000g
[Page 20] 00:00:00:00
[Page 21] 00:00:00:00
[Page 22] 00:00:00:00
[Page 23] 00:00:00:00
[Page 24] 00:00:00:00
[Page 25] 00:00:00:00
[Page 26] 00:00:00:00
[Page 27] 00:00:00:00
[Page 28] 00:00:00:bd (Management data)
[Page 29] 04:00:00:04 (Management data)
[Page 2a] 00:00:00:00 (Management data)
[Page 2b] 00:00:00:00 (Management data)
[Page 2c] 00:00:00:00 (Management data)
```

## Version 2

> Byte order is big endian

Dump of the NTAG213 chip of a Bright White PLA+

```
[Page 00] 1d:98:cd:c0 (Management data)
[Page 01] 39:98:00:00 (Management data)
[Page 02] a1:a3:00:00 (Management data)
[Page 03] e1:10:12:00 (Management data)
[Page 04] 7b:00:65:00 -> Format version information (65 -> version 2)
[Page 05] 41:48:50:4c -> SKU: AHPLPBW-102 (max length might be longer -> check firmware)
[Page 06] 50:42:57:2d -> ^^
[Page 07] 31:30:32:00 -> ^^
[Page 08] 00:00:00:00
[Page 09] 00:00:00:00
[Page 0a] 41:43:00:00 -> Manufacturer: AC (Anycubic) (added for every spool in version 2)
[Page 0b] 00:00:00:00
[Page 0c] 00:00:00:00
[Page 0d] 00:00:00:00
[Page 0e] 00:00:00:00
[Page 0f] 50:4c:41:2b -> Type: PLA+
[Page 10] 00:00:00:00
[Page 11] 00:00:00:00
[Page 12] 00:00:00:00
[Page 13] 00:00:00:00
[Page 14] ff:ed:f0:f0 -> Color: #f0f0ed (opacity: 0xff)
[Page 15] 00:00:00:00
[Page 16] 00:00:00:00
[Page 17] 32:00:64:00 -> Printing speed: 50-100mm/s (new in version 2, currently only present for PLA+, optional)
[Page 18] cd:00:d7:00 -> Nozzle temp range: 205-215°C
[Page 19] 00:00:00:00
[Page 1a] 00:00:00:00
[Page 1b] 00:00:00:00
[Page 1c] 00:00:00:00
[Page 1d] 32:00:3c:00 -> Bed temp range: 50-60°C
[Page 1e] af:00:4a:01 -> Diameter and length: 175x10^-2mm, 330m
[Page 1f] e8:03:00:00 -> Weight: 1000g
[Page 20] 00:00:00:00
[Page 21] 00:00:00:00
[Page 22] 00:00:00:00
[Page 23] 00:00:00:00
[Page 24] 00:00:00:00
[Page 25] 00:00:00:00
[Page 26] 00:00:00:00
[Page 27] 00:00:00:00
[Page 28] 00:00:00:bd (Management data)
[Page 29] 04:00:00:04 (Management data)
[Page 2a] 47:00:00:00 (Management data)
[Page 2b] 00:00:00:00 (Management data)
[Page 2c] 00:00:00:00 (Management data)
```

Reconstructed dump of the NTAG213 chip of HS PLA (reconstructed
from [this](https://www.reddit.com/r/anycubic/comments/1g047ad/comment/mdz70s9/?utm_source=share&utm_medium=web3x&utm_name=web3xcss&utm_term=1&utm_content=share_button))

```
[Page 00] 1d:98:cd:c0 (Management data)
[Page 01] 39:98:00:00 (Management data)
[Page 02] a1:a3:00:00 (Management data)
[Page 03] e1:10:12:00 (Management data)
[Page 04] 7b:00:65:00 -> Format version information (65 -> version 2) TODO: Check if density is real
[Page 05] 41:48:50:4c -> SKU: AHPLPBW-102 (max length might be longer -> check firmware)
[Page 06] 50:42:57:2d -> ^^
[Page 07] 31:30:32:00 -> ^^
[Page 08] 00:00:00:00 -> ^^
[Page 09] 00:00:00:00 -> ^^
[Page 0a] 41:43:00:00 -> Manufacturer: AC (Anycubic) (added for every spool in version 2)
[Page 0b] 00:00:00:00 -> ^^
[Page 0c] 00:00:00:00 -> ^^
[Page 0d] 00:00:00:00 -> ^^
[Page 0e] 00:00:00:00 -> ^^
[Page 0f] 50:4c:41:3f -> Type: PLA?High?Speed
[Page 10] 48:69:67:68 -> ^^
[Page 11] 3f:53:70:65 -> ^^
[Page 12] 65:64:00:00 -> ^^
[Page 13] 00:00:00:00 -> ^^
[Page 14] ff:00:06:e1 -> Color: #e10600 (opacity: 0xff)
[Page 15] 00:00:00:00 -> (unknown - maybe color 2 later)
[Page 16] 00:00:00:00 -> (unknown - maybe color 3 later)
[Page 17] 32:00:96:00 -> Printing speed range 1: 50-150mm/s
[Page 18] be:00:d2:00 -> Nozzle temp range 1: 190-210°C
[Page 19] 96:00:2c:01 -> Printing speed range 2: 150-300mm/s
[Page 1a] d2:00:e6:00 -> Nozzle temp range 2: 210-230°C
[Page 1b] 2c:01:58:02 -> Printing speed range 3: 300-600mm/s
[Page 1c] e6:00:04:01 -> Nozzle temp range 3: 230-240°C
[Page 1d] 32:00:3c:00 -> Bed temp range: 50-60°C
[Page 1e] af:00:4a:01 -> Diameter and length: 175x10^-2mm, 330m
[Page 1f] e8:03:00:00 -> Weight: 1000g
[Page 20] 00:00:00:00
[Page 21] 00:00:00:00
[Page 22] 00:00:00:00
[Page 23] 00:00:00:00
[Page 24] 00:00:00:00
[Page 25] 00:00:00:00
[Page 26] 00:00:00:00
[Page 27] 00:00:00:00
[Page 28] 00:00:00:bd (Management data)
[Page 29] 04:00:00:04 (Management data)
[Page 2a] 47:00:00:00 (Management data)
[Page 2b] 00:00:00:00 (Management data)
[Page 2c] 00:00:00:00 (Management data)
```

## Dump Types and SKUs

> Filament types (names) should align with the material names in the slicer after "Anycubic ". This leads to the right
> filament being recognized when syncing with the ACE Pro in the "Prepare" tab.

> Filament SKUs are less important. They are used to display the right filament in the "Workbench" tab. Somehow, tha
> Anycubic Slicer Next uses the SKU to calculate the matching filament type to display there. The color is not important
> as long as the SKU matches the type.

List of actually found SKUs on official RFID tags:

- PLA Basic Pantone Peach Fuzz: HPL16-101
- PLA Basic Pantone Interstellar Violet: HPL17-101
- PLA Basic Pantone Tropical Turquoise: HPL18-101
- PLA Basic Pantone Spring Leaf: HPL19-101
- PLA+ Bright White: AHPLPBW-102
- PLA+ Dazzling Blue: AHPLPDB-102
- PLA+ Pearl Black: AHPLPBK-102
- PLA+ Texture Grey: AHPLPGY-102
- PLA+ Bright Red: AHPLPBR-102
- PLA Classic Green: AHPLCG-103
- PLA Strawberry Pink: AHPLSP-103
- PLA Vibrant Orange: AHPLVO-103
- PLA Vibrant Yellow: AHPLVY-103
- PLA Purple Opulence: AHPLPO-103
- PLA Dark Brown: AHPLKB-103
- PLA Beige: AHPLLB-103
- PLA Bright Red: AHPLRR-103

SKUs for filament types (reverse-engineered from Anycubic shop in HMTL source code):

- PLA Basic Black: AHPLBK-101
- PLA+ Black: AHPLPBK-102
- PLA Matte Black: HYGBK-101
- PLA Silk White: HSCWH-101
- HS PLA Black: AHHSBK-102
- PETG Black: HPEBK-103
- ASA Black: HASBK-101
- ABS Black: HABBK-102
- TPU Black: HTPBK-101
- PLA Glow Green: HFGBL-101
