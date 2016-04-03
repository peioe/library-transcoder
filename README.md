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
