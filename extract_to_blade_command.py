import sublime, sublime_plugin
import os
from time import sleep

from .extract2blade import ExtractToBlade

class ExtractToBladeCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.init()

    if not self.allow_relative_path:
        self.sublime_file_path = ExtractToBlade.blade_views_dir(self.sublime_file_path)['path_to_views']

    if self.save_last_path:
        self.default_blade_input = self.project_data.get('extract2blade_last_blade_path','')

    # If multiple selection, join it by a new line separator
    for region in self.view.sel():
      if not region.empty():
        self.text_selected = self.text_selected + self.view.substr(region) + '\n'

    # Remove last new line formatter
    self.text_selected = ExtractToBlade.rreplace(self.text_selected,'\n','',1)

    # Open the new blade file input panel
    self.window.show_input_panel(
        ('File name (in %s): (suffix: .blade.php)' % (self.sublime_file_path)),
        self.default_blade_input, # Default value in input
        self.append_to_file, # Method to execute after input
        None,  # No 'change' handler
        self.cancel_handler
    )

  # If the feature is enabled, Cancel handler
  # will reset the last blade path
  def cancel_handler(self):
    if self.save_last_path:
        self.store_user_dirpath('')

  def append_to_file(self, input_filename):
    output_directory = ExtractToBlade.get_output_directory(self.sublime_file_path, input_filename)
    absolute_file_path = ExtractToBlade.get_absolute_filepath(self.sublime_file_path, input_filename)
    blade_filepath = ExtractToBlade.get_blade_filepath(self.sublime_file_path, input_filename)
    blade_dirpath = ExtractToBlade.get_blade_dirpath(self.sublime_file_path, input_filename)

    # Create the directory for the extracted new file if not exist
    self.create_dir(output_directory)

    # Add or append the text to the file
    self.write_to_file(absolute_file_path, self.text_selected)

    # Remove the original text
    self.view.run_command('left_delete')

    # Insert include sentence
    self.insert_include_sentence(blade_filepath)

    # Display the file, after appending to it
    file_view = self.window.open_file(absolute_file_path)

    # Keep the view open
    self.window.focus_view(self.view)

    # If enabled, save how the user entered the path to the file
    if self.save_last_path:
        self.store_user_dirpath(blade_dirpath)

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

  def create_dir(self, directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

  def write_to_file(self, absolute_file_path, text):
    f = open(absolute_file_path, 'a', encoding="utf-8")
    f.write(text)
    f.close()

  def store_user_dirpath(self, user_dirpath):
    proj_data = self.project_data
    proj_data['extract2blade_last_blade_path'] = user_dirpath
    self.window.set_project_data(proj_data)

  def insert_include_sentence(command_instance, blade_path):
    include_sentence = (command_instance.include_sentence % (blade_path))

    # Create the blade "include" sentence
    command_instance.view.run_command('insert', {"characters": include_sentence })

    # Hide Autocomplete
    command_instance.view.run_command('insert', {"characters": '\n'})
    command_instance.view.run_command("hide_auto_complete")
