import sublime, sublime_plugin
import os
from time import sleep

class ExtractToFileCommand(sublime_plugin.TextCommand):
  def run(self, edit):
    self.edit = edit
    self.sublime_vars = self.view.window().extract_variables()

    # extract the text
    self.text_selected = ''
    for region in self.view.sel():
      if not region.empty():
        self.text_selected = self.view.substr(region)

    # ask the user where to put the text
    self.file_choices = ['New file ...'] + os.listdir(self.sublime_vars['file_path'])

    self.view.window().show_quick_panel(
      self.file_choices,

      self.item_chosen,        # Callback
      sublime.MONOSPACE_FONT,  # Options
      0,                       # Starting index
      self.item_highlighted    # Callback
    )

    # print(os.listdir(dir_of_script))

  def item_chosen(self, i):
    # Special case: new file
    if (i == 0):
      self.view.window().show_input_panel(
        ('File name (in %s):' % (self.sublime_vars['file_path'])),
        '',
        self.append_to_file,
        None,  # No 'change' handler
        None   # No 'cancel' handler
      )

    # append to existing file
    else:
      self.append_to_file(self.file_choices[i])

  def append_to_file(self, filename):
    pathname = self.sublime_vars['file_path'] + '/' + filename

    # Remove the original text
    self.view.run_command('left_delete')

    # Add the text to the file
    f = open(pathname, 'a')
    f.write("\n" + self.text_selected)
    f.close()

    # Display the file, after appending to it
    file_view = self.view.window().open_file(pathname)

  def item_highlighted(self, i):
    1
