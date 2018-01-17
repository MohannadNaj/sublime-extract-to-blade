import sublime, sublime_plugin
import os
from time import sleep

class ExtractToBladeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.init()

    if not self.allow_relative_path:
        self.sublime_file_path = self.blade_views_dir(self.sublime_file_path)['path_to_views']

    if self.save_last_path:
        self.default_blade_input = self.project_data.get('extract2blade_last_blade_path','')

    # If multiple selection, join it by a new line separator
    for region in self.view.sel():
      if not region.empty():
        self.text_selected = self.text_selected + self.view.substr(region) + '\n'

    # Remove last new line formatter
    self.text_selected = self.rreplace(self.text_selected,'\n','',1)

    # Open the new blade file input panel
    self.window.show_input_panel(
        ('File name (in %s): (suffix: .blade.php)' % (self.sublime_file_path)),
        self.default_blade_input, # Default value in input
        self.append_to_file, # Method to execute after input
        None,  # No 'change' handler
        None   # No 'cancel' handler
    )


  def append_to_file(self, input_filename):
    input_filename = input_filename.replace('.blade.php','')

    output_paths = self.output_paths(input_filename)
    blade_paths = self.blade_paths(output_paths['abspath'], input_filename, output_paths['basename'])

    absolute_file_path = output_paths['output_directory'] + '/' + blade_paths['filename']

    # Create the directory for the extracted new file if not exist
    self.create_dir(output_paths['output_directory'])

    # Add or append the text to the file
    self.write_to_file(absolute_file_path, self.text_selected)

    # Remove the original text
    self.view.run_command('left_delete')

    # Insert include sentence
    self.insert_include_sentence(blade_paths['path'])

    # Display the file, after appending to it
    file_view = self.window.open_file(absolute_file_path)

    # If enabled, save how the user entered the path to the file
    if self.save_last_path:
        self.store_user_dirpath(blade_paths['user_dirpath'])

  def resolve_blade_path(self, abspath):
    blade_filename = self.blade_views_dir(abspath)['path_after_views']
    blade_filename = blade_filename.replace('/', '.')
    return blade_filename

  # replace last occurrence of string https://stackoverflow.com/a/2556156/4330182
  def rreplace(self, s, old, new, count):
    return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]

  def blade_views_dir(self, absolute_path):
    absolute_path = absolute_path.lower().replace('\\','/').split('resources/views',1)
    path_to_views = absolute_path[0] + 'resources/views/'


    try:
        path_after_views = absolute_path[1][1:] # remove first character
    except IndexError:
        path_after_views = ""

    return { "path_to_views" : path_to_views, "path_after_views" : path_after_views }

  def init(self):
    self.init_defaults()
    self.load_settings()

  def init_defaults(self):
    self.window = self.view.window()
    self.sublime_vars = self.window.extract_variables()
    self.project_data = self.window.project_data()
    self.sublime_file_path = self.sublime_vars['file_path']
    self.default_blade_input = ''
    # extract the text
    self.text_selected = ''

  def load_settings(self):
    sublime_preferences = sublime.load_settings('Preferences.sublime-settings')
    self.save_last_path = sublime_preferences.get('extract_to_blade_save_last_path', True)
    self.allow_relative_path = sublime_preferences.get('extract_to_blade_relative_path', False)
    self.include_sentence = sublime_preferences.get('extract_to_blade_include_sentence', "@include('%s')")

  def output_paths(self, filename):
    abspath = os.path.abspath(self.sublime_file_path + '/' + filename)
    basename = os.path.basename(abspath)
    
    if '.' in basename:
        abspath = os.path.abspath(abspath.replace(basename,'') + '/' + basename.replace('.','/'))
        basename = os.path.basename(abspath)

    output_directory = os.path.dirname(abspath)
    return {"abspath": abspath, "basename": basename, "output_directory": output_directory}

  def blade_paths(self, abspath, input_filename, basename):
    blade_path = self.resolve_blade_path(abspath)
    # save how the last time the user entered the path to the blade view
    # by ripping off the resolved basename from the input
    blade_user_dirpath = self.rreplace(input_filename, basename, '',1)

    blade_filename = basename + '.blade.php'

    return {"path": blade_path, "user_dirpath": blade_user_dirpath, "filename": blade_filename}

  def insert_include_sentence(self, blade_path):
    include_sentence = (self.include_sentence % (blade_path))

    # Create the blade "include" sentence
    self.view.run_command('insert', {"characters": include_sentence })

    # Hide Autocomplete
    self.view.run_command('insert', {"characters": '\n'})
    self.view.run_command("hide_auto_complete")

  def create_dir(self, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

  def write_to_file(self, absolute_file_path, text):
    f = open(absolute_file_path, 'a')
    f.write(text)
    f.close()

  def store_user_dirpath(self, user_dirpath):
    proj_data = self.project_data
    proj_data['extract2blade_last_blade_path'] = user_dirpath
    self.window.set_project_data(proj_data)