#!/usr/bin/env python

import gtk
import gtkextra

class xApplication(gtkextra.CharSelection):

    def __init__(self):
        gtkextra.CharSelection.__init__(self)
        self.connect("destroy", gtk.main_quit)
        self.cancel_button.connect("clicked", gtk.main_quit)
        self.ok_button.connect("clicked", self.ok_clicked)
        self.show()

    def ok_clicked(self, *args):
        psfont = self.font_combo.psfont
        psname = psfont.psname
        code = self.get_selection()
        print "%s, %d" % (psname, code)
        
    def mainloop(self):
        gtk.main()

class Application(gtkextra.CharSelection):

    def __init__(self):
        gtkextra.CharSelection.__init__(self)
        self.connect("destroy", self.quit)
        self.cancel_button.connect("clicked", self.quit)
        self.ok_button.connect("clicked", self.ok_clicked)
        self.show()

    def ok_clicked(self, *args):
        #FIXME
        psfont = self.font_combo.psfont
        psname = psfont.psname
        code = self.get_selection()
        print "%s, %d" % (psname, code)
        
    def quit(self, *args):
        gtk.main_quit()


if __name__ == '__main__':		
    app = Application()
    gtk.main()
