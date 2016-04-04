# -*- coding: utf-8 -*-
from sys import *
import os.path
import time
from optparse import OptionParser

# OPTIONS
# names of covers to keep. format: cover_names = ['cover.jpg', 'folder.jpg', ...]. To keep all images, see next variable.
cover_names = ['cover.jpg']

# file extensions that will be copied without any transcoding or transformation: same format as above.
copy_extensions = ['mp3', 'ogg', 'm4a', 'mpc', 'txt']

# Extensions that need to be transcoded.
transcode_extensions = ['flac', 'wav', 'ape', 'alac']

# Transcoding options for each encoder
default_lame_options = "-V2 --add-id3v2"
ogg_options = "-q8"

# mp3 multiple values separator
mp3_sep = " & "

parser = OptionParser(usage="usage: %prog [options] source_dir target_dir")

parser.add_option("-f", "--format", dest="format", default="mp3", type="choice", choices=["ogg","mp3"],
                  help="transcode to mp3 or ogg (default is mp3)")
parser.add_option("-m", "--multiprocess", action="store_true", dest="multiprocess", default=False,
                  help="use multiprocessing to transcode the files (default is false)")
parser.add_option("-r", "--resample", action="store_true", dest="resample", default=False,
                  help="resample file to 44.1kHz when transcoding")
parser.add_option("-v", "--verbose",
                  action="store_true", dest="verbose", default=False,
                  help="print status messages to stdout")

(options, args) = parser.parse_args()

if len(args) != 2:
    parser.error("incorrect number of arguments")

source_topdir = args[0]
destination_topdir = args[1]

dirs_created = 0
dirs_skipped = 0
covers_copied = 0
covers_skipped = 0
files_copied = 0
files_updated = 0
files_skipped = 0
files_transcoded = 0
transcode_error = 0

transcode_source_files = []

def shellquote(s):
    return "'" + s.replace("'", "'\\''") + "'"

def copy_file(source_file, destination_file):
    if not(os.system("cp %s %s" % (shellquote(source_file), shellquote(target_file)))):
        return True
    else:
        return False

def build_lame_cmd(tags_dict):
    global default_lame_options
    lame_options = default_lame_options
    if "title" in tags_dict:
        lame_options += " --tt "+shellquote(tags_dict['title'])
    if "artist" in tags_dict:
        lame_options += " --ta "+shellquote(tags_dict['artist'])
    if "tracknumber" in tags_dict:
        lame_options += " --tn "+shellquote(tags_dict['tracknumber'])
    if "genre" in tags_dict:
        lame_options += " --tg "+shellquote(tags_dict['genre'])
    if "date" in tags_dict:
        lame_options += " --ty "+shellquote(tags_dict['date'])
    if "album" in tags_dict:
        lame_options += " --tl "+shellquote(tags_dict['album'])
    if "albumartist" in tags_dict:
        lame_options += " --tv TPE2="+shellquote(tags_dict['albumartist'])
    if "composer" in tags_dict:
        lame_options += " --tv TCOM="+shellquote(tags_dict['composer'])
    return lame_options

def transcode_ogg(source_file, target_file):
    global ogg_options, files_transcoded, transcode_error
    if options.resample:
        ogg_options += " --resample 44100"
    command = "oggenc %s -Q -o %s %s" % (ogg_options, shellquote(target_file), shellquote(source_file))
    if not(os.system(command)):
        files_transcoded += 1
    else:
        print "Error during transcoding to ogg. source: %s -- dest: %s" % (source_file, target_file)
        transcode_error += 1

def transcode_mp3(source_file, target_file):
    global files_transcoded, transcode_error
    vorbis_tags = os.popen("metaflac --export-tags-to=- %s" % shellquote(source_file))
    tags_dict = {}
    for vorbis in vorbis_tags:
        tag, value = vorbis.split("=", 1)
        tag = tag.lower()
        if tag in tags_dict:
            tags_dict[tag] = tags_dict[tag]+mp3_sep+value.replace("\n", "")
        else:
            tags_dict[tag] = value.replace("\n", "")
    if options.resample:
        resample = "--resample 44.1"
    command = "flac -cd %s | lame %s %s - %s" % (shellquote(source_file), resample, build_lame_cmd(tags_dict), shellquote(target_file))
    print command
    if not(os.system(command)):
        files_transcoded += 1
    else:
        print "Error during transcoding to mp3. source: %s -- dest: %s" % (source_file, target_file)
        transcode_error += 1

def process_file(source_file):
    global files_transcoded, files_skipped
    target_file = file.replace(source_topdir, destination_topdir)
    target_file = os.path.splitext(target_file)[0]+"."+options.format.lower()
    if not(os.path.isfile(target_file)) or (os.path.isfile(target_file) and os.path.getmtime(source_file) > os.path.getmtime(target_file)):
        if options.format == "mp3":
            transcode_mp3(source_file, target_file)
        elif options.format == "ogg":
            transcode_ogg(source_file, target_file)
    else:
        files_skipped += 1

for root, dirs, files in os.walk(source_topdir):
    for source_dir in dirs:
        source_dir = os.path.join(root, source_dir)
        target_dir = source_dir.replace(source_topdir, destination_topdir)
        # directory creation if not existing
        if not(os.path.isdir(target_dir)):
            os.system("mkdir %s" % shellquote(target_dir))
            dirs_created += 1
        else:
            dirs_skipped += 1
    for file in files:
        source_file = os.path.join(root, file)
        target_file = source_file.replace(source_topdir, destination_topdir)

        filename, file_extension = os.path.splitext(source_file)
        file_extension = file_extension.lower()
        file_extension = file_extension.replace(".", "")
        
        # cover copy if not existing
        if file in cover_names:
            if not(os.path.isfile(target_file)):
                if copy_file(source_file, target_file):
                    covers_copied += 1
            else:
                covers_skipped += 1
        
        # file copy if not existing or too old
        elif file_extension in copy_extensions:
            if not(os.path.isfile(target_file)):
                if copy_file(source_file, target_file):
                    files_copied += 1
            elif os.path.isfile(target_file) and os.path.getmtime(target_file) < os.path.getmtime(source_file):
                if copy_file(source_file, target_file):
                    files_updated += 1
            else:
                files_skipped += 1
        
        # transcoding
        elif file_extension in transcode_extensions:
            transcode_source_files.append(source_file)

for file in transcode_source_files:
    process_file(file)

# Output
if options.verbose:
    print "%d directories created. %d directories already existing." % (dirs_created, dirs_skipped)
    print "%d covers copied. %d covers already existing." % (covers_copied, covers_skipped)
    print "Copied %d files. Transcoded %d files. Updated %d files. Skipped %d files." % (files_copied, files_transcoded, files_updated, files_skipped)
    print "%d transcode errors." % transcode_error
