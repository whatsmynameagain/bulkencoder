## CAUTION: The converted/re-encoded files are placed in the same directory where the originals were and **the originals are automatically deleted**. This means that some files *could* be lost if something goes wrong. Use at your own risk.

## What is this?

A simple python script used to find all avi/mpg/mov/mp4 files in a directory recursively and either convert them to mp4 or encode them more efficiently into a smaller mp4 in order to save space using HandBrakeCLI (flatpak). 

## Original use case

The encoding settings are hardcoded based on the specific needs I had (many poorly-encoded 1080p videos with no concern for minor quality loss). In my case, the mp4 "Fast 1080p30" preset with some tweaks was more than enough to reduce disk space usage significantly.

## Caveats
Because of the hardcoded settings, using that same preset on videos of different resolutions *might* yield decent results, but it is recommended to tweak the script depending on the source files. (See HandBrakeCLI's [quick tutorial](https://handbrake.fr/docs/en/latest/cli/cli-options.html) and [command line reference](https://handbrake.fr/docs/en/latest/cli/command-line-reference.html).)

## Installation

### Linux

- Clone or download main.py.
- Install the [HandBrake flatpak](https://flathub.org/apps/fr.handbrake.ghb).
- Make sure HandBrake has access to the directories you want to scan (I use [Flatseal](https://flathub.org/apps/com.github.tchx84.Flatseal)).

### Other OS

Not directly supported, but the script can be modified to call whatever HandBrakeCLI installation is available.

## Usage

### Make sure main.py is in a non temp directory. It will create a .txt file ('completed_log.txt') in that directory where it will keep track of already processed files over multiple batches.

```
python main.py source_directory number_to_process
```

Where **source_directory** is the absolute or relative path to the desired directory, and **number_to_process** is the number of files to be processed before automatically stopping.
**It is recommended to use the *absolute* path for complex directory trees.**

While I recommend doing smaller batches of files, if you want to process all available files, set *number_to_process* to **-1**

## Why HandBrake and not ffmpeg?

Because of simplicity. And because I already had a custom preset I was happy with.
