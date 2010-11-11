#! /usr/bin/python
#
"""Generate a PDF file from image files with cairo.

Based on png2pdf.py by ludwigf (http://blog.ludwigf.org/2010/1/27/png2pdf).
"""


import optparse
import os.path
import sys
import gtk
import cairo



def _images_to_pdf(inputs, output, width, height):
    """Convert inputs (image files) to output (PDF).
    """
    surface = cairo.PDFSurface(output, width, height)

    ctx = cairo.Context(surface)
    ct2 = gtk.gdk.CairoContext(ctx)

    for img in inputs:
        try:
            pixbuf = gtk.gdk.pixbuf_new_from_file(img)
        except:  # GError, $img may not be a image file supported.
            print >> sys.stderr, "Could not detect image type of '%s'. Skip it..." % img
            continue

        ct2.set_source_pixbuf(pixbuf,0,0)
        ct2.paint()

        # next page
        ctx.show_page()
    
    surface.finish()

        
def main():
    p = optparse.OptionParser("%prog [OPTION ...] IMAGE_0 [IMAGE_1 ...]")
    p.add_option('-o', '--output', default='output.pdf', help='Output PDF filename [%default]')
    p.add_option('', '--force', default=False, help='Force overwrite the output [no]')
    p.add_option('', '--width', type='int', default=1024, help='Output width [%default]')
    p.add_option('', '--height', type='int', default=768, help='Output height [%default]')
    (options, args) = p.parse_args()

    if len(args) < 1:
        p.print_help()
        sys.exit(0)

    inputs = args

    if os.path.exists(options.output) and not options.force:
        print >> sys.stderr, "Output '%s' already exists. Stop the job." % options.output
        sys.exit(1)

    _images_to_pdf(inputs, options.output, options.width, options.height)


if __name__ == '__main__':
    main()

# vim: set sw=4 ts=4 expandtab:
