import os
import sys

class ExtractToBlade(object):
  def get_output_directory(path, filename):
    filename = filename.replace('.blade.php','')
    return ExtractToBlade.output_paths(path, filename)['output_directory']

  def get_absolute_filepath(path, filename):
    filename = filename.replace('.blade.php','')
    output_paths = ExtractToBlade.output_paths(path, filename)
    blade_paths = ExtractToBlade.blade_paths(output_paths['abspath'], filename, output_paths['basename'])
    return os.path.join( output_paths['output_directory'] , blade_paths['filename'] )

  def get_blade_filepath(path, filename):
    filename = filename.replace('.blade.php','')
    output_paths = ExtractToBlade.output_paths(path, filename)
    return ExtractToBlade.blade_paths(output_paths['abspath'], filename, output_paths['basename'])['path']

  def get_blade_dirpath(path, filename):
    filename = filename.replace('.blade.php','')
    output_paths = ExtractToBlade.output_paths(path, filename)
    return ExtractToBlade.blade_paths(output_paths['abspath'], filename, output_paths['basename'])['user_dirpath']

  def output_paths(sublime_file_path, filename):
    abspath = os.path.normpath(os.path.join(sublime_file_path,  filename.strip('//').strip('\\')))

    basename = os.path.basename(abspath)
    
    if '.' in basename:
        abspath = os.path.join( os.path.normpath(abspath.replace(basename,'') ) , basename.replace('.','/'))
        basename = os.path.basename(abspath)


    output_directory = os.path.normpath(os.path.dirname(abspath))

    return {"abspath": abspath, "basename": basename, "output_directory": output_directory}

  def blade_paths(abspath, filename, basename):
    blade_path = ExtractToBlade.resolve_blade_path(abspath)
    # save how the last time the user entered the path to the blade view
    # by ripping off the resolved basename from the input
    blade_user_dirpath = ExtractToBlade.rreplace(filename, basename, '',1)

    blade_filename = basename + '.blade.php'

    return {"path": blade_path, "user_dirpath": blade_user_dirpath, "filename": blade_filename}
  # replace last occurrence of string https://stackoverflow.com/a/2556156/4330182
  def rreplace(s, old, new, count):
    return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]

  def blade_views_dir(absolute_path):
    absolute_path = absolute_path.lower().replace('\\','/').split('resources/views',1)
    path_to_views = absolute_path[0] + 'resources/views/'

    try:
        path_after_views = absolute_path[1][1:] # remove first character
    except IndexError:
        path_after_views = ""

    return { "path_to_views" : path_to_views, "path_after_views" : path_after_views }

  def resolve_blade_path(abspath):
    blade_filename = ExtractToBlade.blade_views_dir(abspath)['path_after_views']
    blade_filename = blade_filename.replace('/', '.')
    return blade_filename
