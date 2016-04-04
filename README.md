# library-transcoder
Library transcoder is a simple python script that will "sync" a lossless version of your music library to a lossy version. It will copy files you tell it to copy (mp3, ogg, covers, any pre-determined .ext files etc) and transcode the files you want to transcode (flac, wav, etc) to the format you want to have your lossy library in (mp3, ogg, aac).<br />
It's not done so don't get it just yet :p

## Dependencies
> python 2.7, oggenc, flac, metaflac

## Usage
**translibrary.py [options] source_dir target_dir**

Options:
> -h, --help  show this help message and exit<br />
> -f FORMAT, --format=FORMAT  transcode to mp3 or ogg (default is mp3)<br />
> -m, --multiprocess  use multiprocessing to transcode the files (default is false)<br />
> -r, --resample  resample file to 44.1kHz when transcoding<br />
> -v, --verbose print status messages to stdout<br />
See at the top of the scripts for variables that can be changed.

## Features and todo-list
### Todo:
- [ ] Multithreading for transcoding.
- [ ] Transcode flac to target format/bitrate.

### Transcoding features:
- [ ] Transcode to AAC
- [x] Resampling when transcoding to MP3

### Done
- [x] Copy directory structure from source to target.
- [x] Whitelist of file extensions to keep and copy.
- [x] Copy existing mp3, ogg, mpc from source to target.
- [x] Copy cover.jpg or other specific filenames.
- [x] Reprocess files when more recent than target.
- [x] number of skipped copies, transcodes, etc.
- [x] Skip existing mp3/other files from copy.
- [x] Option for target formats (mp3, ogg)

#### Transcoding features
- [x] Option to downsample to 44.1kHz when transcoding.
- [x] Transcode to OGG
- [x] Resampling when transcoding to OGG
- [x] Transcode to MP3 (default)

