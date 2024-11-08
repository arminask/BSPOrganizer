# BSPOrganizer

A Tool for organizing the directory structure of extracted CAB archives containing Qualcomm platform drivers.

When given a source path containing directories listed in Config.xml, the script moves their contents to the output path specified in the configuration file and generates a driver definitions XML file for use with the DriverUpdater tool.

The script only moves drivers if each source directory name exists in Config.xml. The configuration file is based on a specific Qualcomm platform, other QC platform drivers may have different names, and the script will not move these drivers.

If you find any drivers that don’t exist in Config.xml, please add them in a PR.

## Usage

If the `--codename` and/or `--modelnumber` arguments are not specified, they default to the `--silicon` argument value.

- E.g: if the source directory contains QC SC7280 drivers, Android SoC model number SM7325, and the output BSP is for a device with the codename Yupik:

```
python main.py --input Drivers --output ./Output --silicon 7280 --codename Yupik --modelnumber 7325
```

Resulting output directory paths:

```
(outputdir)/components/QC7325/Drivers/SOC/ResetPower
(outputdir)/components/Devices/Yupik/Platform/Drivers/Audio/Device
```

---

- E.g: if the source directory contains QC SC7180 drivers, Android SoC model number SM7125, and the output BSP is for a device with the codename Atoll:

```
python main.py --input Drivers --output ./Output --silicon 7180 --codename Atoll --modelnumber 7125
```

Resulting output directory paths:

```
(outputdir)/components/QC7125/Drivers/SOC/ResetPower
(outputdir)/components/Devices/Atoll/Platform/Drivers/Audio/Device
```

Please see the [script example run output](example-run.txt) and the resulting generated [output directory hierarchy](output-tree.txt).
