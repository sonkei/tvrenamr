#!/usr/bin/python

import os
from optparse import OptionParser

from core.core import TvRenamr
from core.errors import *
import core

parser = OptionParser()
parser.add_option('-a', '--auto', action='store_true', dest='organise', help='Automatically move renamed files to the directory specified in renamed and organise them appropriated according to their show name and season number')
parser.add_option('-e', '--episode', dest='episode', help='Set the episode number. Currently this will cause errors when working with more than one file')
parser.add_option('--ignore-recursive', action='store_true', dest='ignore_recursive', default=False, help='Only use files from the root of a given directory do not enter any sub-directories')
parser.add_option('-l', '--log_level', dest='log', default='debug', help='Set the log level')
parser.add_option('-n', '--name', dest='name', help='Set the show name for renaming')
parser.add_option('-o', '--output', dest='output_format', help='Set the output format for the episodes being renamed')
parser.add_option('-r', "--renamed", dest='renamed', help='The directory to move renamed files to, if not specified the working directory is used')
parser.add_option('--regex', dest='regex', help='The regular expression to set the format of files being renamed. Use %n to specify the show name, %s for the season number and %e for the episode number. All spaces are converted to periods before the regex is run')
parser.add_option('-s', '--season', dest='season', help='Set the season number.')
parser.add_option('-t', '--the', action='store_true', dest='the', help='Set the position of \'The\' in a show\'s name to the end of the file')
parser.add_option('-x', '--exceptions', dest='exceptions', help='Specify an exceptions file')
(options, args) = parser.parse_args()

def __determine_type(path, ignore_recursive=False, ignore_filelist=None):
    """
    Determines which files need to be processed for renaming.

    :param path: The input file or directory.
    :param ignore_recursive: To ignore a recursive search for files if
    `path` is a directory. Default is False.
    :param ignore_filelist: Optional set of files to ignore from renaming.
    Often used by filtering methods such as Deluge.

    :returns: A list of files to be renamed.
    :rtype: A list of dictionaries, who's keys are `directory` and `filename`
    """
    if os.path.isdir(path):
        filelist = []
        for root, dirs, files in os.walk(path):
            for fname in files:
                # If we have a file we should be ignoring and skipping it.
                if ignore_filelist is not None and (os.path.join(root, fname) in ignore_filelist):
                    continue

                filelist.append({'directory': root, 'filename': fname})
            # Don't want a recusive walk?
            if ignore_recursive:
                break

        return filelist
    elif os.path.isfile(path):
        working = os.path.split(path)
        return [{'directory': working[0], 'filename': working[1]}]

def rename(path):
    details = __determine_type(path)
    for show in details:
        filename = show['filename']
        working_dir = show['directory']
        tv = TvRenamr(working_dir, 'debug')
        try:
            credentials = tv.extract_episode_details_from_file(filename, user_regex=options.regex)
            if options.exceptions: credentials['series'] = tv.convert_show_names_using_exceptions_file(options.exceptions, credentials['series'])
            if options.name: credentials['series']=options.name
            if options.season: credentials['season']=options.season
            if options.episode: credentials['episode']=options.episode
            title = tv.retrieve_episode_name(credentials['series'],credentials['season'],credentials['episode'])
            if options.the: credentials['series'] = tv.set_position_of_leading_the_to_end_of_series_name(title['series'])
            else: credentials['series'] = title['series']
            credentials['title'] = title['title']
            path = tv.build_path(series=credentials['series'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], renamed_dir=options.renamed, organise=options.organise, format=options.output_format)
            tv.rename(filename,path)
        except Exception, e: print e

if __name__=="__main__":
    if args[0] is None: parser.error('You must specify a file or directory')
    rename(args[0])
else: print 'This script is only designed to be run standalone'