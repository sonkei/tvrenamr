#!/usr/bin/python

import logging
import os
from pyinotify import WatchManager, Notifier, ProcessEvent, IN_CREATE, IN_MOVED_TO, IN_ISDIR
from core.core import TvRenamr
from core.errors import *
from optparse import OptionParser

log = logging.getLogger('Daemon')

class WatchFolder(ProcessEvent):
    def __init__(self): 
        pass
    
    def process_IN_MOVED_TO(self, event):
        log.debug('MOVED TO: '+event.pathname)
        if not event.name.startswith('.'):
            if event.dir:
                for each_tuple in os.walk(event.pathname):
                    for fname in each_tuple[2]: self.__rename(each_tuple[0], fname)
            else: self.__rename(*os.path.split(event.pathname))
    
    def process_IN_CREATE(self, event):
        log.debug('CREATED: '+event.pathname)
        if not event.name.startswith('.') and not event.dir: self.__rename(*os.path.split(event.pathname))
    
    def __rename(self, directory, filename):
        try:
            tv = TvRenamr(directory, options.log)
            credentials = tv.extract_episode_details_from_file(filename)
            if options.exceptions is not None:
                try: credentials['show'] = tv.convert_show_names_using_exceptions_file(options.exceptions, credentials['show'])
                except: ShowNotInExceptionsList
            title = tv.retrieve_episode_name(credentials['show'],credentials['season'],credentials['episode'])
            credentials['show'] = title['show']
            if options.the:
                try: credentials['show'] = tv.move_leading_the_to_trailing_the(credentials['show'])
                except: NoLeadingTheException
            credentials['title'] = title['title']
            path = tv.build_path(show=credentials['show'], season=credentials['season'], episode=credentials['episode'], title=credentials['title'], extension=credentials['extension'], renamed_dir=options.renamed, organise=options.organise, format=options.output_format)
            tv.rename(filename, path)
        except Exception, e:
            log.error(e)
            pass
    
if __name__=="__main__":
    parser = OptionParser()
    parser.add_option('-l', '--log_level', dest='log', default='info', help='Set the log level. Valid options are debug, info, warning, error and critical.')
    parser.add_option('--library', dest='library', help='Set the library to use for retrieving episode titles. This defaults to tvrage, but thetvdb is also available.')
    parser.add_option('-o', '--output', dest='output_format', help='Set the output format for the episodes being renamed.')
    parser.add_option('--organise', action='store_true', dest='organise', help='Automatically move renamed files to the directory specified with -r and organise them based on their show name and season number.')
    parser.add_option('-r', '--renamed', dest='renamed', help='The directory to move renamed files to, if not specified the working directory is used.')
    parser.add_option('-t', '--the', action='store_true', dest='the', help='Set the position of \'The\' in a show\'s name to the end of the file.')
    parser.add_option('-x', '--exceptions', dest='exceptions', help='Set the location of the exceptions file.')
    (options, args) = parser.parse_args()
    if args is None: parser.error('You must specify a file or directory')
    
    working_dir = args[0]
    
    wm = WatchManager()
    p = WatchFolder()
    notifier = Notifier(wm, p)

    mask = IN_MOVED_TO | IN_CREATE  # watched events -> add IN_DONT_FOLLOW to not follow symlinks, and IN_CREATE to watch created files
    wdd = wm.add_watch(working_dir, mask, rec=True, auto_add=True) #watch this directory, with mask(s), recursively
    notifier.loop()#daemonize=True, pid_file=os.path.join(os.path.dirname(__file__), tvrenamrd.pid), force_kill=True, stdout=os.path.join(os.path.dirname(__file__), stdout.txt))
else: print 'This script is only designed to be run standalone'