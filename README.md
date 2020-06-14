# Fluorescence spectra plotter
![alt text](example/2020-06-14 21:06:58_protein_3.png 'Spectra')


This repository can be used to automatically create fluorescent specta plots from spectrometer data in csv format. 

Both csv files, one for the excitation spectra and one for the emission spectra, must be formated in the following way:

| wavelength in nm | protein_1 | protein_2 | protein_3 |  blank |
|:----------:|:--------:|:--------:|:--------:|:------:|
| 480     | ... |... |...|...|
| 482      | ... |... |...|...|
| 484      | ... |... |...|...|

Move the two files in the folder created from cloning the repository. Then open the terminal in the repository and enter:

```console
foo@bar:~$ python main.py -ex excitation_file.csv -em emission_file.csv
```

If your csv files do not use a **,** as a separator, you can indicate it (for example if a **;** is the separator:

```console
foo@bar:~$ python main.py -ex excitation_file.csv -em emission_file.csv -s ';'
```

This leads to the creation of a folder called **plots**, containing one plot for each sample. 

## Requirements:

see requirements.txt