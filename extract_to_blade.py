import sublime, sublime_plugin
import os
from time import sleep

class ExtractToBladeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.edit = edit
    self.sublime_vars = self.view.window().extract_variables()
    self.save_last_path = sublime.load_settings('Preferences.sublime-settings').get('extract_to_blade_save_last_path', True)

    default_input = ''

    if self.save_last_path:
        default_input = self.view.window().project_data().get('extract2blade_last_blade_path','')

    # extract the text
    self.text_selected = ''
    for region in self.view.sel():
      if not region.empty():
        self.text_selected = self.view.substr(region)


      self.view.window().show_input_panel(
        ('File name (in %s): (suffix: .blade.php)' % (self.sublime_vars['file_path'])),
        default_input,
        self.append_to_file,
        None,  # No 'change' handler
        None   # No 'cancel' handler
      )


  def append_to_file(self, filename):
    filename = filename.replace('.blade.php','')
    absolute_pathname = os.path.abspath(self.sublime_vars['file_path'] + '/' + filename)
    blade_path = self.resolve_blade_path(absolute_pathname)
    blade_filename = blade_path
    output_directory = os.path.dirname(absolute_pathname)

    if '.' in blade_path:
        blade_filename = blade_filename.replace('.','/')
        output_directory = os.path.dirname(output_directory + '/' + blade_filename)
        blade_filename = os.path.basename( blade_filename )
        blade_path = self.resolve_blade_path( output_directory + '/' + blade_filename )

    # save how the last time the user entered the path to the blade view
    blade_dirpath = self.rreplace(filename, blade_filename, '',1)

    blade_filename = blade_filename + '.blade.php'

    # Remove the original text
    self.view.run_command('left_delete')

    # Create the blade "include" sentence
    self.view.run_command('insert', {"characters": '@include("' + blade_path + '")'})

    # Hide Autocomplete
    self.view.run_command('insert', {"characters": '\n'})
    self.view.run_command("hide_auto_complete")

    # Create the directory for the extracted new file if not exist
    if not os.path.exists(output_directory):
        os.makedirs(output_directory)

    absolute_file_path = output_directory + '/' + blade_filename
    # Add the text to the file
    f = open(absolute_file_path, 'a')
    f.write(self.text_selected)
    f.close()

    if self.save_last_path:
        proj_data = self.view.window().project_data()
        proj_data['extract2blade_last_blade_path'] = blade_dirpath
        self.view.window().set_project_data(proj_data)

    # Display the file, after appending to it
    file_view = self.view.window().open_file(absolute_file_path)

  def resolve_blade_path(self, absolute_pathname):
    blade_filename = absolute_pathname.lower().replace('\\','/').split('resources/views/',1)[1]
    blade_filename = blade_filename.replace('/', '.')

    return blade_filename

  # replace last occurrence of string https://stackoverflow.com/a/2556156/4330182
  def rreplace(self, s, old, new, count):
    return (s[::-1].replace(old[::-1], new[::-1], count))[::-1]
