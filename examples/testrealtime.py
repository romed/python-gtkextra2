#!/usr/bin/env python

import gtk, gtkextra
from random import randint

class Application(gtk.Window):

    def __init__(self):
        gtk.Window.__init__(self)
        self.set_title("GtkPlot Real Time Demo")
        self.set_size_request(550, 600)
        self.connect("destroy", self.quit)

        colormap = self.get_colormap()
        red = colormap.alloc_color("red")
        light_blue = colormap.alloc_color("light blue")
        light_yellow = colormap.alloc_color("light yellow")
        white = colormap.alloc_color("white")

        scrollwin = gtk.ScrolledWindow()
        scrollwin.set_policy(gtk.POLICY_AUTOMATIC, gtk.POLICY_AUTOMATIC)
        self.add(scrollwin)

        self.canvas = canvas = gtkextra.PlotCanvas(gtkextra.PLOT_LETTER_W, gtkextra.PLOT_LETTER_H)
        canvas.set_background(light_blue)
        canvas.connect("button_press_event", self.button_press_handler)
        scrollwin.add_with_viewport(canvas)

        plot = gtkextra.Plot()
        plot.resize(width=0.65, height=0.45)
        plot.set_background(light_yellow)
        plot.legends_set_attributes(None, 0, None, white)
        plot.set_range(0.0, 20.0, 0.0, 1.0)
        plot.axis_set_ticks(gtkextra.PLOT_AXIS_X, 2.0, 1)
        plot.axis_set_ticks(gtkextra.PLOT_AXIS_Y, 0.1, 1)
        plot.axis_set_labels_style(gtkextra.PLOT_AXIS_TOP, gtkextra.PLOT_LABEL_FLOAT, 0)
        plot.axis_set_labels_style(gtkextra.PLOT_AXIS_BOTTOM, gtkextra.PLOT_LABEL_FLOAT, 0)
        plot.axis_set_visible(gtkextra.PLOT_AXIS_TOP, gtk.TRUE)
        plot.axis_set_visible(gtkextra.PLOT_AXIS_RIGHT, gtk.TRUE)
        plot.grids_set_visible(gtk.TRUE, gtk.TRUE, gtk.TRUE, gtk.TRUE)
        plot.axis_hide_title(gtkextra.PLOT_AXIS_TOP)
        plot.axis_hide_title(gtkextra.PLOT_AXIS_RIGHT)
        plot.axis_set_title(gtkextra.PLOT_AXIS_LEFT, "Intensity")
        plot.axis_set_title(gtkextra.PLOT_AXIS_BOTTOM, "Time (s)")
        plot.set_legends_border(gtkextra.PLOT_BORDER_SHADOW, 3)
        plot.legends_move(0.60, 0.10)
        canvas.add_plot(plot, 0.15, 0.15)

        #canvas.put_text(0.45, 0.05, "Times-BoldItalic", 20, 0, None, None,
        #canvas.put_text(0.45, 0.05, "Courier-Bold", 20, 0, None, None, #OK
        canvas.put_text(0.45, 0.05, "Helvetica", 20, 0, None, None, #OK
                        gtk.TRUE, gtk.JUSTIFY_CENTER, "Real Time Demo")

        data = gtkextra.PlotData()
        plot.add_data(data)
        data.set_legend("Random pulse")
        data.set_symbol(gtkextra.PLOT_SYMBOL_DIAMOND, gtkextra.PLOT_SYMBOL_OPAQUE, 10, 2, red, red)
        data.set_line_attributes(gtkextra.PLOT_LINE_SOLID, 0, 0, 1, red)
        
        plot.clip_data(gtk.TRUE)

        self.show_all()

        gtk.timeout_add(1000, self.update, canvas, plot, data)

    def update(self, canvas, plot, data, *args):
        y = randint(0, 9) / 10.0

        px = data.x
        py = data.y
        if px is None : px = []
        if py is None : py = []
        
        n = data.get_numpoints()
        if n == 0:
            x = 1.0
        else:
            x = px[n - 1] + 1.0

        px.append(x)
        py.append(y)

        data.set_points(x=px, y=py)

        (xmin, xmax) = plot.get_xrange()
        if x > xmax:
            plot.set_xrange(xmin + 5.0, xmax + 5.0)

        canvas.paint()
        canvas.refresh()

        return gtk.TRUE
        
    def button_press_handler(self, canvas, event, *extra):
        (x, y) = canvas.get_pointer()
        position = canvas.get_position(x, y)
        print "Canvas position:", position[0], position[1] 

    def quit(self, *args):
        gtk.main_quit()

if __name__ == '__main__':
    app = Application()
    gtk.main()
