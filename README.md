# library-transcoder
Library transcoder is a simple python script that will "sync" a lossless version of your music library to a lossy version. It will copy files you tell it to copy (mp3, ogg, covers, any pre-determined .ext files etc) and transcode the files you want to transcode (flac, wav, etc) to the format you want to have your lossy library in (mp3, ogg, aac).

It's not done so don't get it just yet :p

## Usage
translibrary.py [options] source_dir target_dir

Options:
> -h, --help  show this help message and exit

> -v, --verbose print status messages to stdout

> -m, --multiprocess  use multiprocessing to transcode the files (default is false)

> -f FORMAT, --format=FORMAT  transcode to mp3 or ogg (default is ogg)

> -r, --resample  resample file to 44.1kHz when transcoding

## Features and todo-list

### Done
-* Copy directory structure from source to dest
-* Whitelist of file extensions to keep and copy.
-* Copy existing mp3, ogg, mpc from source to dest
-* Copy cover.jpg or other specific filenames
-* Reprocess files when more recent than destination.
-* number of skipped copies, transcodes, etc
-* Skip existing mp3/other files from copy.
-* Option for target formats (mp3, ogg)

*
** Transcoding features
-* Option to downsample to 44.1kHz when transcoding.
-* Transcode to ogg



** Todo:
-* Help message with version
-* Option for the number of processes. Default to number of CPUs.
-* Transcode flac to target format/bitrate.

** Transcoding features:
-* transcode to AAC
