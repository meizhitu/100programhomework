__author__ = 'rui'
#coding=utf-8

import sys
import os
import pango

import gtk


class TextEditorEx:
    # When our window is destroyed, we want to break out of the GTK main loop.
    # We do this by calling gtk_main_quit(). We could have also just specified
    # gtk_main_quit as the handler in Glade!
    def on_window_destroy(self, widget, data=None):
        gtk.main_quit()

    # When the window is requested to be closed, we need to check if they have
    # unsaved work. We use this callback to prompt the user to save their work
    # before they exit the application. From the "delete-event" signal, we can
    # choose to effectively cancel the close based on the value we return.
    def on_window_delete_event(self, widget, event, data=None):
        if self.check_for_save(): self.on_save_menu_item_activate(None, None)
        return False # Propogate event

    # Called when the user clicks the 'New' menu. We need to prompt for save if
    # the file has been modified, and then delete the buffer and clear the
    # modified flag.
    def on_new_menu_item_activate(self, menuitem, data=None):
        if self.check_for_save(): self.on_save_menu_item_activate(None, None)
        # clear editor for a new file
        buff = self.text_view.get_buffer()
        buff.set_text("")
        buff.set_modified(False)
        self.filename = None
        self.reset_default_status()

    # Called when the user clicks the 'Open' menu. We need to prompt for save if
    # thefile has been modified, allow the user to choose a file to open, and
    # then call load_file() on that file.
    def on_open_menu_item_activate(self, menuitem, data=None):
        if self.check_for_save(): self.on_save_menu_item_activate(None, None)
        filename = self.get_open_filename()
        if filename: self.load_file(filename)

    # Called when the user clicks the 'Save' menu. We need to allow the user to choose
    # a file to save if it's an untitled document, and then call write_file() on that
    # file.
    def on_save_menu_item_activate(self, menuitem, data=None):
        if self.filename == None:
            filename = self.get_save_filename()
            if filename: self.write_file(filename)
        else:
            self.write_file(None)

    # Called when the user clicks the 'Save As' menu. We need to allow the user
    # to choose a file to save and then call write_file() on that file.
    def on_save_as_menu_item_activate(self, menuitem, data=None):
        filename = self.get_save_filename()
        if filename: self.write_file(filename)

    # Called when the user clicks the 'Quit' menu. We need to prompt for save if
    # the file has been modified and then break out of the GTK+ main loop
    def on_quit_menu_item_activate(self, menuitem, data=None):
        if self.check_for_save(): self.on_save_menu_item_activate(None, None)
        gtk.main_quit()

    # Called when the user clicks the 'Cut' menu.
    def on_cut_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.cut_clipboard(gtk.clipboard_get(), True);

    # Called when the user clicks the 'Copy' menu.
    def on_copy_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.copy_clipboard(gtk.clipboard_get());

    # Called when the user clicks the 'Paste' menu.
    def on_paste_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.paste_clipboard(gtk.clipboard_get(), None, True);

    # Called when the user clicks the 'Delete' menu.
    def on_delete_menu_item_activate(self, menuitem, data=None):
        buff = self.text_view.get_buffer();
        buff.delete_selection(False, True);

    # Called when the user clicks the 'About' menu. We use gtk_show_about_dialog()
    # which is a convenience function to show a GtkAboutDialog. This dialog will
    # NOT be modal but will be on top of the main application window.
    def on_about_menu_item_activate(self, menuitem, data=None):
        if self.about_dialog:
            self.about_dialog.present()
            return

        authors = [
            "Micah Carrick <email@micahcarrick.com>"
        ]

        about_dialog = gtk.AboutDialog()
        about_dialog.set_transient_for(self.window)
        about_dialog.set_destroy_with_parent(True)
        about_dialog.set_name("GTK+ Text Editor")
        about_dialog.set_version("0.1")
        about_dialog.set_copyright("Copyright \xc2\xa9 2007 Micah Carrick")
        about_dialog.set_website("http://www.micahcarrick.com")
        about_dialog.set_comments("GTK+ and Glade3 GUI Programming Tutorial")
        about_dialog.set_authors(authors)
        about_dialog.set_logo_icon_name(gtk.STOCK_EDIT)

        # callbacks for destroying the dialog
        def close(dialog, response, editor):
            editor.about_dialog = None
            dialog.destroy()

        def delete_event(dialog, event, editor):
            editor.about_dialog = None
            return True

        about_dialog.connect("response", close, self)
        about_dialog.connect("delete-event", delete_event, self)

        self.about_dialog = about_dialog
        about_dialog.show()

    # We call error_message() any time we want to display an error message to
    # the user. It will both show an error dialog and log the error to the
    # terminal window.
    def error_message(self, message):
        # log to terminal window
        print message
        # create an error message dialog and display modally to the user
        dialog = gtk.MessageDialog(None,
                                   gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                   gtk.MESSAGE_ERROR, gtk.BUTTONS_OK, message)
        dialog.run()
        dialog.destroy()

    # This function will check to see if the text buffer has been
    # modified and prompt the user to save if it has been modified.
    def check_for_save(self):
        ret = False
        buff = self.text_view.get_buffer()

        if buff.get_modified():
            # we need to prompt for save
            message = "Do you want to save the changes you have made?"
            dialog = gtk.MessageDialog(self.window,
                                       gtk.DIALOG_MODAL | gtk.DIALOG_DESTROY_WITH_PARENT,
                                       gtk.MESSAGE_QUESTION, gtk.BUTTONS_YES_NO,
                                       message)
            dialog.set_title("Save?")

            if dialog.run() == gtk.RESPONSE_NO:
                ret = False
            else:
                ret = True

            dialog.destroy()

        return ret

    # We call get_open_filename() when we want to get a filename to open from the
    # user. It will present the user with a file chooser dialog and return the
    # filename or None.
    def get_open_filename(self):
        filename = None
        chooser = gtk.FileChooserDialog("Open File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_OPEN,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_OPEN, gtk.RESPONSE_OK))
        response = chooser.run()
        if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        chooser.destroy()

        return filename

    # We call get_save_filename() when we want to get a filename to save from the
    # user. It will present the user with a file chooser dialog and return the
    # filename or None.
    def get_save_filename(self):
        filename = None
        chooser = gtk.FileChooserDialog("Save File...", self.window,
                                        gtk.FILE_CHOOSER_ACTION_SAVE,
                                        (gtk.STOCK_CANCEL, gtk.RESPONSE_CANCEL,
                                         gtk.STOCK_SAVE, gtk.RESPONSE_OK))
        response = chooser.run()
        if response == gtk.RESPONSE_OK: filename = chooser.get_filename()
        chooser.destroy()

        return filename

    # We call load_file() when we have a filename and want to load it into the
    # buffer for the GtkTextView. The previous contents are overwritten.
    def load_file(self, filename):
        # add Loading message to status bar and ensure GUI is current
        self.statusbar.push(self.statusbar_cid, "Loading %s" % filename)
        while gtk.events_pending(): gtk.main_iteration()

        try:
            # get the file contents
            fin = open(filename, "r")
            text = fin.read()
            fin.close()

            # disable the text view while loading the buffer with the text
            self.text_view.set_sensitive(False)
            buff = self.text_view.get_buffer()
            buff.set_text(text)
            buff.set_modified(False)
            self.text_view.set_sensitive(True)

            # now we can set the current filename since loading was a success
            self.filename = filename

        except:
            # error loading file, show message to user
            self.error_message("Could not open file: %s" % filename)

        # clear loading status and restore default
        self.statusbar.pop(self.statusbar_cid)
        self.reset_default_status()

    def write_file(self, filename):
        # add Saving message to status bar and ensure GUI is current
        if filename:
            self.statusbar.push(self.statusbar_cid, "Saving %s" % filename)
        else:
            self.statusbar.push(self.statusbar_cid, "Saving %s" % self.filename)

        while gtk.events_pending(): gtk.main_iteration()

        try:
            # disable text view while getting contents of buffer
            buff = self.text_view.get_buffer()
            self.text_view.set_sensitive(False)
            text = buff.get_text(buff.get_start_iter(), buff.get_end_iter())
            self.text_view.set_sensitive(True)
            buff.set_modified(False)
            # set the contents of the file to the text from the buffer
            if filename:
                fout = open(filename, "w")
            else:
                fout = open(self.filename, "w")
            fout.write(text)
            fout.close()

            if filename: self.filename = filename

        except:
            # error writing file, show message to user
            self.error_message("Could not save file: %s" % filename)

        # clear saving status and restore default
        self.statusbar.pop(self.statusbar_cid)
        self.reset_default_status()

    def reset_default_status(self):
        if self.filename:
            status = "File: %s" % os.path.basename(self.filename)
        else:
            status = "File: (UNTITLED)"

        self.statusbar.pop(self.statusbar_cid)
        self.statusbar.push(self.statusbar_cid, status)

    # We use the initialization of the TutorialTextEditor class to establish
    # references to the widgets we'll need to work with in the callbacks for
    # various signals. This is done using the XML file we created with Glade
    def __init__(self):
        # Default values
        self.filename = None
        self.about_dialog = None

        # use GtkBuilder to build our interface from the XML file
        try:
            builder = gtk.Builder()
            builder.add_from_file("res/texteditor.glade")
        except:
            self.error_message("Failed to load UI XML file: texteditor.glade")
            sys.exit(1)

        # get the widgets which will be referenced in callbacks
        self.window = builder.get_object("window")
        self.statusbar = builder.get_object("statusbar")
        self.text_view = builder.get_object("text_view")

        # connect signals
        builder.connect_signals(self)

        # set the text view font
        self.text_view.modify_font(pango.FontDescription("monospace 10"))

        # set the default icon to the GTK "edit" icon
        gtk.window_set_default_icon_name(gtk.STOCK_EDIT)

        # setup and initialize our statusbar
        self.statusbar_cid = self.statusbar.get_context_id("Tutorial GTK+ Text Editor")
        self.reset_default_status()

    # Run main application window
    def main(self):
        self.window.show()
        gtk.main()


if __name__ == "__main__":
    editor = TextEditorEx()
    editor.main()