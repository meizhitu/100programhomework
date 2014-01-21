__author__ = 'rui'
#coding=utf-8
import pygtk

pygtk.require("2.0")
import gtk

openWindowCount = 0


class PostItWindow:
    def __init__(self):
        self.gladeFile = "res/postit.glade"
        self.builder = gtk.Builder()
        self.builder.add_from_file(self.gladeFile)
        self.mainWindow = self.builder.get_object('postItWindow')
        self.tvInput = self.builder.get_object('tvInput')
        self.btnEdit = self.builder.get_object('buttonEdit')
        self.btnColor = self.builder.get_object('colorbutton')
        self.builder.connect_signals(self)
        if self.mainWindow:
            self.mainWindow.connect('destroy', self.destroy)
            self.mainWindow.set_title("即时贴")
            self.mainWindow.show_all()

    def destroy(self, widget, data=None):
        global openWindowCount
        openWindowCount -= 1
        if openWindowCount == 0:
            gtk.main_quit()

    def on_buttonDo_clicked(self, *args):
        w = PostItWindow()
        global openWindowCount
        openWindowCount += 1

    def on_colorbutton_color_set(self, *args):
        color = self.btnColor.get_color()
        self.btnEdit.modify_bg(gtk.STATE_NORMAL, color)
        print ('You have selected the color:%d %d %d' % (color.red, color.green, color.blue))

    def on_tvInput_key_press_event(self, widget, event):
        ctrl = event.state & gtk.gdk.CONTROL_MASK
        alt = event.state & gtk.gdk.MOD1_MASK
        shift = event.state & gtk.gdk.SHIFT_MASK
        if event.keyval == 65293 and ctrl:
            self.tvInput.set_size_request(1, 1)
            text_buffer = self.tvInput.get_buffer()
            result = text_buffer.get_text(text_buffer.get_start_iter(), text_buffer.get_end_iter())
            self.btnEdit.set_label(result)
            return True
        return False

    def on_buttonEdit_clicked(self, *args):
        self.tvInput.set_size_request(220, 220)


if __name__ == "__main__":
    w = PostItWindow()
    openWindowCount += 1
    gtk.main()