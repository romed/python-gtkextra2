# Quick hack to help populate objects definitions in defs files.

# Copy C field definitions to this string.
# Then run me.
lines = """

"""


"""
  (fields
   '("gboolean" "is_visible")
   '("GtkPlotVector" "origin")
   '("GtkPlotVector" "direction")
   '("GtkPlotText" "title")
"""

import string

print """  (fields"""
for line in lines.split('\n'):
    line = line.strip()
    line = line.replace(';', '')
    if not line:
        continue

    t,v = line.split(' ')
    t = t.strip()
    v = v.strip()
    if v[0] == '*':
        v = v[1:]
        t += '*'
    
    print """    '("%s" "%s")""" % (t,v)
print """  )"""

    

    
    
    
