# BSPOrganizer

A Tool for organizing the directory structure of extracted CAB archives containing Qualcomm platform drivers.

When given a source path containing directories listed in Config.xml, the script moves their contents to an organized output directory specified in the configuration file and generates a driver definitions XML file for use with the DriverUpdater tool.

The script only moves drivers if each source directory name exists in Config.xml. The configuration file is based on a specific Qualcomm platform, other QC platform drivers may have different names, and the script will not move these drivers.

If you find any drivers that don’t exist in Config.xml, please add them in a PR.

## Usage

If the `--modelnumber` argument is not specified, it defaults to the `--silicon` argument value.

- E.g: if the source directory contains QC SC7280 drivers and they will be adapted for an Android SoC with the model number SM7325:

```
python main.py --input ./Drivers --output ./Output --silicon 7280 --modelnumber 7325
```

Resulting output directory paths:

```
(outputdir)/components/QC7325/Drivers/SOC/ResetPower/qccdi7280.inf (and other files)
(outputdir)/components/QC7325/Drivers/Audio/ADCM/qcadcm7280.sys (and other files)
```

---

- E.g: if the source directory contains QC SC7180 drivers and they will be adapted for an Android SoC with the model number SM7125:

```
python main.py --input ./Drivers --output ./Output --silicon 7180 --modelnumber 7125
```

Resulting output directory paths:

```
(outputdir)/components/QC7125/Drivers/SOC/ResetPower/qccdi7180.inf (and other files)
(outputdir)/components/QC7125/Drivers/Audio/ADCM/qcadcm7180.sys (and other files)
```

---

- E.g: if the source directory contains QC SC8180 drivers and the `--modelnumber` value is not specified:

```
python main.py --input ./Drivers --output ./Output --silicon 8180
```

Resulting output directory paths:

```
(outputdir)/components/QC8180/Drivers/SOC/ResetPower/qccdi8180.inf (and other files)
(outputdir)/components/QC8180/Drivers/Audio/ADCM/qcadcm8180.sys (and other files)
```

Please see the [script example run output](example-run.txt) and the resulting generated [output directory hierarchy](output-tree.txt).
