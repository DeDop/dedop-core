import os.path

import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages


class FigureWriter:
    """
    Writer for Matplotlib figures.

    :param output_path: PDF file path or directory.
    :param output_format: output format. Must be either "pdf" or "dir".
    """

    def __init__(self, output_path: str, output_format: str):
        self._pdf_pages = None
        self._output_path = None
        self._output_format = None

        if not output_path:
            raise ValueError('output_path must be given')

        if not output_format:
            # guess format from filename
            _, ext = os.path.splitext(output_path)
            if len(ext) > 1:
                output_format = ext[1:].lower()
            else:
                output_format = 'dir'
        else:
            output_format = output_format.lower()

        if output_format not in ['pdf', 'dir']:
            raise ValueError('output_format "%s" is unsupported' % output_format)

        self._output_path = output_path
        self._output_format = output_format
        self._pdf_pages = None

        if output_format == 'pdf':
            # see http://matplotlib.org/faq/howto_faq.html#save-multiple-plots-to-one-pdf-file
            output_dir = os.path.dirname(output_path)
            output_basename, ext = os.path.splitext(os.path.basename(output_path))
            if not output_basename:
                raise ValueError('output_path is missing a basename')
            if not ext:
                ext = '.pdf'
            elif not (ext == '.pdf' or ext == '.PDF'):
                raise ValueError('output_path extension must be ".pdf"')
            self._output_path = os.path.join(output_dir, output_basename + ext)

    @property
    def output_path(self):
        return self._output_path

    @property
    def output_format(self):
        return self._output_format

    def savefig(self, file_name=None):
        is_pdf = self._output_format == "pdf"
        if is_pdf:
            file_path = self._output_path
        else:
            if not file_name:
                raise ValueError('file_name must be given')
            file_path = os.path.join(self._output_path, file_name)

        dir_path = os.path.dirname(file_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path, exist_ok=True)

        if is_pdf:
            if not self._pdf_pages:
                self._pdf_pages = PdfPages(file_path)
            file_object = self._pdf_pages
            file_format = 'pdf'
        else:
            file_object = file_path
            file_format = None

        # Save the current matplotlib pyplot figure
        plt.savefig(file_object, format=file_format)

    def close(self):
        if self._pdf_pages:
            self._pdf_pages.close()
            self._pdf_pages = None
