#!/usr/bin/env python
import gtk
import gtkextra
from math import exp, pow, sin

class Application(gtk.Window):

    scale = 1.0
    def __del__(self):
        print 'Application.__del__'
    
    def __init__(self):
        self.nlayers = 0
        self.buttons = []
        self.plots = []
        
        page_width = gtkextra.PLOT_LETTER_W * self.scale
        page_height = gtkextra.PLOT_LETTER_H * self.scale
    
        gtk.Window.__init__(self)
        self.set_title("GtkPlot Demo")
        self.set_size_request(550, 650)
        #self.set_size_request(page_width, page_height)

        scrollwin = gtk.ScrolledWindow()
        scrollwin.set_policy(gtk.POLICY_ALWAYS, gtk.POLICY_ALWAYS)
        self.add(scrollwin)

        colormap = self.get_colormap()
        light_yellow = colormap.alloc_color("light yellow")
        light_blue = colormap.alloc_color("light blue")

        self.canvas = canvas = gtkextra.PlotCanvas(page_width, page_height)
        canvas.plot_canvas_set_flags(gtkextra.PLOT_CANVAS_DND_FLAGS)
        scrollwin.add_with_viewport(canvas)
        canvas.set_size(page_width, page_height)

        plot = self.new_layer(canvas)
        plot.set_range(-1.0, 1.0, -1.0, 1.4)
        plot.legends_move(0.51, 0.05)
        plot.set_legends_border(gtkextra.PLOT_BORDER_NONE, gtkextra.PLOT_BORDER_NONE)
        plot.axis_hide_title(gtkextra.PLOT_AXIS_TOP)
        plot.axis_set_ticks(gtkextra.PLOT_AXIS_X, 1.0, 1)
        plot.axis_set_ticks(gtkextra.PLOT_AXIS_Y, 1.0, 1)
        plot.axis_set_visible(gtkextra.PLOT_AXIS_TOP, gtk.TRUE)
        plot.axis_set_visible(gtkextra.PLOT_AXIS_RIGHT, gtk.TRUE)
        plot.x0_set_visible(gtk.TRUE)
        plot.y0_set_visible(gtk.TRUE)
        plot.axis_set_labels_suffix(gtkextra.PLOT_AXIS_LEFT, "%");
        canvas.add_plot(plot, 0.15, 0.06)
        self.build_example1(plot)

        plot = self.new_layer(canvas)
        plot.set_background(light_yellow)
        plot.legends_set_attributes(None, 0, None, light_blue)
        plot.set_range(0.0, 1.0, 0.0, 0.85)
        plot.axis_set_visible(gtkextra.PLOT_AXIS_TOP, gtk.TRUE)
        plot.axis_set_visible(gtkextra.PLOT_AXIS_RIGHT, gtk.TRUE)
        plot.axis_hide_title(gtkextra.PLOT_AXIS_TOP)
        plot.axis_hide_title(gtkextra.PLOT_AXIS_RIGHT)
        plot.grids_set_visible(gtk.TRUE, gtk.TRUE, gtk.TRUE, gtk.TRUE)
        plot.set_legends_border(gtkextra.PLOT_BORDER_SHADOW, 3)
        plot.legends_move(0.58, 0.05)
        canvas.add_plot(plot, 0.15, 0.4)
        self.build_example2(plot)

        canvas.connect("move_item", self.move_item)
        canvas.connect("select_item", self.select_item)

        canvas.put_text(0.40, 0.02, "Helvetica", 16, 0, None, None,
                        gtk.TRUE, gtk.JUSTIFY_CENTER, "DnD titles, legends and plots")
        canvas.put_text(0.40, 0.72, "Helvetica", 16, 0, None, None,
                        gtk.TRUE, gtk.JUSTIFY_CENTER,
                        "You can use \\ssubscripts\\b\\b\\b\\b\\b\\b\\b"\
                        "\\b\\b\\b\\N\\Ssuperscripts")
        child = canvas.put_text(0.40, 0.755, "Helvetica", 16, 0, None, None,
                                gtk.TRUE, gtk.JUSTIFY_CENTER,
                                "Format text mixing \\Bbold \\N\\i, italics, "\
                                "\\ggreek \\4\\N and \\+different fonts")

        child.data.set_border(gtkextra.PLOT_BORDER_SHADOW, 2, 0, 2)

        self.show_all()

        canvas.export_ps_with_size("plotdemo.ps", epsflag=gtk.TRUE)
        print "Wrote plotdemo.ps"


    def move_item(self, canvas, item, new_x, new_y, *args):
        print "move_item"
        if item.type == gtkextra.PLOT_CANVAS_DATA:
            print "MOVING DATA"
            (i, old_x, old_y) = canvas.get_active_point()
            print "Active point: %d -> %f %f" % (i, new_x, new_y)
            data = canvas.get_active_data()
            x, y, dx, dy = data.x, data.y, data.dx, data.dy
            x[i] = new_x
            y[i] = new_y
            data.set_points(x=x, y=y, dx=dx, dy=dy)
        return gtk.TRUE

    def select_item(self, canvas, event, item, *args):
        if item.type == gtkextra.PLOT_CANVAS_TEXT:
            print "Item selected: TEXT"
        elif item.type == gtkextra.PLOT_CANVAS_TITLE:
            print "Item selected: TITLE"
        elif item.type == gtkextra.PLOT_CANVAS_LEGENDS:
            print "Item selected: LEGENDS"
        elif item.type == gtkextra.PLOT_CANVAS_PLOT:
            print "Item selected: PLOT"
        elif item.type == gtkextra.PLOT_CANVAS_AXIS:
            print "Item selected: AXIS"
        elif item.type == gtkextra.PLOT_CANVAS_PIXMAP:
            print "Item selected: PIXMAP"
        elif item.type == gtkextra.PLOT_CANVAS_DATA:
            print "Item selected: DATA"
            (i, x, y) = canvas.get_active_point()
            print "Active point: %d -> %f %f" % (i, x, y)
            canvas.get_active_data().add_marker(i)
            canvas.get_active_plot().queue_draw()
        elif item.type == gtkextra.PLOT_CANVAS_MARKER:
            print "Item selected: MARKER"
        elif item.type == gtkextra.PLOT_CANVAS_NONE:
            print "Item selected: NONE"
        plot = canvas.get_active_plot()
        for n in xrange(self.nlayers):
            if plot == self.plots[n]:
                canvas.set_active_plot(plot)
                self.buttons[n].set_active(gtk.TRUE)
            else:
                self.buttons[n].set_active(gtk.FALSE)
        return gtk.TRUE

    def activate_plot(self, button, canvas, *args):
        if button.get_active():
            for n in xrange(self.nlayers):
                if button == self.buttons[n]:
                    canvas.set_active_plot(self.plots[n])
                else:
                    self.buttons[n].set_active(gtk.FALSE) 
        return gtk.TRUE

    def activate_button(self, canvas, *args):
        plot = canvas.get_active_plot()
        for n in xrange(self.nlayers):
            if plot == self.plots[n]:
                self.buttons[n].set_active(gtk.TRUE)
            else:
                self.buttons[n].set_active(gtk.FALSE)
        return gtk.TRUE
        
    def new_layer(self, canvas):
        self.nlayers = self.nlayers + 1
        button = gtk.ToggleButton(str(self.nlayers))
        button.set_size_request(20, 20)
        canvas.put(button, (self.nlayers - 1) * 20, 0)
        button.connect("toggled", self.activate_plot, canvas)
        plot = gtkextra.Plot()
        plot.resize(0.5, 0.25)
        self.buttons.append(button)
        self.plots.append(plot)
        button.set_active(gtk.TRUE)
        return plot

    def build_example1(self, plot):
        px1 = [0., .2, .4, .6, .8, 1.]
        py1 = [.2, .4, .5, .35, .30, .40]
        dx1 = [.2, .2, .2, .2, .2, .2]
        dy1 = [.1, .1, .1, .1, .1, .1]

        px2 = [0., -.2, -.4, -.6, -.8, -1.]
        py2 = [.2, .4, .5, .35, .30, .40]
        dx2 = [.2, .2, .2, .2, .2, .2]
        dy2 = [.1, .1, .1, .1, .1, .1]

        colormap = self.get_colormap()
        red = colormap.alloc_color("red")
        black = colormap.alloc_color("black")
        blue = colormap.alloc_color("blue")

        data = gtkextra.PlotData()
        plot.add_data(data)
        data.set_points(x=px1, y=py1, dx=dx1, dy=dy1)
        data.set_symbol(gtkextra.PLOT_SYMBOL_DIAMOND, gtkextra.PLOT_SYMBOL_EMPTY, 10, 2, red, red)
        data.set_line_attributes(gtkextra.PLOT_LINE_SOLID, 0, 0, 1, red)
        data.set_connector(gtkextra.PLOT_CONNECT_SPLINE)
        data.show_yerrbars()
        data.set_legend("Spline + EY")
        data.show_labels(gtk.TRUE)
        data.set_labels(['0', '1', '2', '3', '4', '5'])
        data.set_labels(['0', '1', '2', '3', '4', '99'])
        
        data = gtkextra.PlotData()
        plot.add_data(data)
        data.set_points(x=px2, y=py2, dx=dx2, dy=dy2)
        data.set_symbol(gtkextra.PLOT_SYMBOL_SQUARE, gtkextra.PLOT_SYMBOL_OPAQUE, 8, 2, black, black)
        data.set_line_attributes(gtkextra.PLOT_LINE_SOLID, 0, 0, 4, red)
        data.set_connector(gtkextra.PLOT_CONNECT_STRAIGHT)
        data.set_x_attributes(gtkextra.PLOT_LINE_SOLID, 0, 0, 0, black)
        data.set_y_attributes(gtkextra.PLOT_LINE_SOLID, 0, 0, 0, black)
        data.set_legend("Line + Symbol")
        
        data = plot.add_function(self.function)
        data.set_line_attributes(gtkextra.PLOT_LINE_SOLID, 0, 0, 0, blue)
        data.set_legend("Function Plot")

    def build_example2(self, plot):
        px2 = [.1, .2, .3, .4, .5, .6, .7, .8]
        py2 = [.012, .067, .24, .5, .65, .5, .24, .067]
        dx2 = [.1, .1, .1, .1, .1, .1, .1, .1]

        colormap = self.get_colormap()
        dark_green = colormap.alloc_color("dark green")
        blue = colormap.alloc_color("blue")
        
        data = plot.add_function(self.gaussian)
        data.set_line_attributes(gtkextra.PLOT_LINE_DASHED, 0, 0, 2, dark_green)
        data.set_legend("Gaussian")

        data = gtkextra.PlotBar(gtk.ORIENTATION_VERTICAL)
        plot.add_data(data)
        data.set_points(x=px2, y=py2, dx=dx2)
        data.set_symbol(gtkextra.PLOT_SYMBOL_NONE, gtkextra.PLOT_SYMBOL_OPAQUE, 10, 2, blue, blue)
        data.set_line_attributes(gtkextra.PLOT_LINE_NONE, 0, 0, 1, blue)
        data.set_connector(gtkextra.PLOT_CONNECT_NONE)
        data.set_legend("V Bars")

    def function(self, x, *extra):
        try:
            return -0.5 + 0.3 * sin(3.0 * x) * sin(50.0 * x)
        except:
            return None

    def gaussian(self, x, *extra):
        try:
            return 0.65 * exp(-0.5 * pow(x - 0.5, 2) / 0.02)
        except:
            return None

if __name__ == '__main__':
    app = Application()
    app.connect("destroy", lambda win : gtk.main_quit())
    gtk.main()

