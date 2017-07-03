#!/usr/bin/env python3

"""Simple HTTP Server With Upload.

This module builds on BaseHTTPServer by implementing the standard GET
and HEAD requests in a fairly straightforward manner.

see: https://gist.github.com/UniIsland/3346170
"""


__version__ = "0.1"
__all__ = ["SimpleHTTPRequestHandler"]
__author__ = "bones7456"
__home_page__ = "http://li2z.cn/"

cookies = []

import codecs
import os
import posixpath
import http.server
# import urllib.request, urllib.parse, urllib.error
import urllib.parse
import cgi
import shutil
import mimetypes
import re
from io import BytesIO

import db


class SimpleHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    """Simple HTTP request handler with GET/HEAD/POST commands.

    This serves files from the current directory and any of its
    subdirectories.  The MIME type for files is determined by
    calling the .guess_type() method. And can reveive file uploaded
    by client.

    The GET/HEAD/POST requests are identical except that the HEAD
    request omits the actual contents of the file.

    """

    server_version = "SimpleHTTPWithUpload/" + __version__

    def do_GET(self):
        """Serve a GET request."""
        f = self.send_head()
        if f:
            self.copyfile(f, self.wfile)
            f.close()

    def do_HEAD(self):
        """Serve a HEAD request."""
        f = self.send_head()
        if f:
            f.close()

    def do_POST(self):
        """Serve a POST request."""
        info = self.deal_post_data()
        info['ip'] = self.client_address[0]
        print(info)

        f = BytesIO()

        result = codecs.open('result.html', 'r', 'utf-8').read()
        print(result)
        if info['error']:
            h5 = '<h5 class="error">' + info['message'] + '</h5>'
        else:
            insert_image = db.insert_image(info)
            #print('INSERT IMAGE:', insert_image)
            if insert_image[0]:
                h5 = '<h5>' + 'Se ha enviado a imprimir tu imagen <b>"' + \
                    info['name'] + info['ext'] + '"</b></h5>'
                os.remove(info['path'])
            else:
                h5 = '<h5 class="error">' + insert_image[1] + '</h5>'

        result = result.replace('__RESULT__', h5)

        f.write(result.encode('UTF-8'))

        length = f.tell()
        f.seek(0)

        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        if f:
            self.copyfile(f, self.wfile)
            f.close()
        return

    def deal_post_data(self):
        data = {}

        content_type = self.headers['content-type']
        if not content_type:
            data['error'] = True
            data['message'] = "Content-Type header doesn't contain boundary"
            return data
        boundary = content_type.split("=")[1].encode()
        remainbytes = int(self.headers['content-length'])
        line = self.rfile.readline()
        remainbytes -= len(line)
        if not boundary in line:
            data['error'] = True
            data['message'] = "Content NOT begin with boundary"
            return data

        # print('NOMBRE #############################################')
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(
            r'Content-Disposition.*name="nombre"', line.decode())
        if not fn:
            data['error'] = True
            data['message'] = "Falta el nombre..."
            return data
        line = self.rfile.readline()
        remainbytes -= len(line)
        value = self.rfile.readline()
        remainbytes -= len(value)
        value = value.decode()[0:-1]
        if value.endswith('\r'):
            value = value[0:-1]
        data['usuario'] = value
        line = self.rfile.readline()
        remainbytes -= len(line)

        # print('CORREO #############################################')
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(
            r'Content-Disposition.*name="correo"', line.decode())
        if not fn:
            data['error'] = True
            data['message'] = "Falta el apellido..."
            return data
        line = self.rfile.readline()
        remainbytes -= len(line)
        value = self.rfile.readline()
        remainbytes -= len(value)
        value = value.decode()[0:-1]
        if value.endswith('\r'):
            value = value[0:-1]
        data['correo'] = value
        line = self.rfile.readline()
        remainbytes -= len(line)

        # print('EMPRESA #############################################')
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(
            r'Content-Disposition.*name="empresa"', line.decode())
        if not fn:
            data['error'] = True
            data['message'] = "Falta la empresa..."
            return data
        line = self.rfile.readline()
        remainbytes -= len(line)
        value = self.rfile.readline()
        remainbytes -= len(value)
        value = value.decode()[0:-1]
        if value.endswith('\r'):
            value = value[0:-1]
        data['empresa'] = value
        line = self.rfile.readline()
        remainbytes -= len(line)

        # print('CARGO #############################################')
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(
            r'Content-Disposition.*name="cargo"', line.decode())
        if not fn:
            data['error'] = True
            data['message'] = "Falta el cargo..."
            return data
        line = self.rfile.readline()
        remainbytes -= len(line)
        value = self.rfile.readline()
        remainbytes -= len(value)
        value = value.decode()[0:-1]
        if value.endswith('\r'):
            value = value[0:-1]
        data['cargo'] = value
        line = self.rfile.readline()
        remainbytes -= len(line)

        # print('CODIGO #############################################')
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(
            r'Content-Disposition.*name="codigo"', line.decode())
        if not fn:
            data['error'] = True
            data['message'] = "Falta el código..."
            return data
        line = self.rfile.readline()
        remainbytes -= len(line)
        value = self.rfile.readline()
        remainbytes -= len(value)
        value = value.decode()[0:-1]
        if value.endswith('\r'):
            value = value[0:-1]
        data['codigo'] = value

        # validar codigo
        valid_code = db.valid_code(value)
        if not valid_code[0]:
            data['error'] = True
            data['message'] = valid_code[1]
            # return data

        line = self.rfile.readline()
        remainbytes -= len(line)

        # print('ESTILO #############################################')
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(
            r'Content-Disposition.*name="estilo"', line.decode())
        if not fn:
            data['error'] = True
            data['message'] = "Falta el estilo..."
            return data
        line = self.rfile.readline()
        remainbytes -= len(line)
        value = self.rfile.readline()
        remainbytes -= len(value)
        value = value.decode()[0:-1]
        if value.endswith('\r'):
            value = value[0:-1]
        data['estilo'] = value
        line = self.rfile.readline()
        remainbytes -= len(line)

        # print('IMAGEN #############################################')
        line = self.rfile.readline()
        remainbytes -= len(line)
        fn = re.findall(
            r'Content-Disposition.*name="imagen"; filename="(.*)"', line.decode())
        if not fn:
            data['error'] = True
            data['message'] = "No se encuentra el nombre de la imagen..."
            return data
        path = self.translate_path(self.path) + '/uploads'
        filename = fn[0]
        fn = os.path.join(path, fn[0])
        line = self.rfile.readline()
        remainbytes -= len(line)
        line = self.rfile.readline()
        remainbytes -= len(line)
        try:
            out = open(fn, 'wb')
        except IOError:
            data['error'] = True
            data['message'] = "No se pudo enviar la imagen"
            return data

        preline = self.rfile.readline()
        remainbytes -= len(preline)
        while remainbytes > 0:
            line = self.rfile.readline()
            remainbytes -= len(line)
            if boundary in line:
                preline = preline[0:-1]
                if preline.endswith(b'\r'):
                    preline = preline[0:-1]
                out.write(preline)
                out.close()
                data['name'], data['ext'] = os.path.splitext(filename)
                data['path'] = 'uploads/' + filename
                data['error'] = False
                return data
            else:
                out.write(preline)
                preline = line
        data['error'] = True
        data['message'] = "Error al enviar los datos"
        return data

    def send_head(self):
        """Common code for GET and HEAD commands.

        This sends the response code and MIME headers.

        Return value is either a file object (which has to be copied
        to the outputfile by the caller unless the command was HEAD,
        and must be closed by the caller under all circumstances), or
        None, in which case the caller has nothing further to do.

        """
        path = self.translate_path(self.path)
        f = None
        if os.path.isdir(path):
            if not self.path.endswith('/'):
                # redirect browser - doing basically what apache does
                print('redirect to', self.path + '/')
                self.send_response(301)
                self.send_header("Location",  self.path + '/')
                self.end_headers()
                return None
            for index in "index.html", "index.htm":
                index = os.path.join(path, index)
                if os.path.exists(index):
                    path = index
                    break
            else:
                return self.list_directory(path)

        if self.path.endswith('.py') or self.path.endswith('.txt'):
            print(self.client_address)
            if '127.0.0.1' not in self.client_address:
                return self.list_directory(self.path)

        ctype = self.guess_type(path)
        try:
            # Always read in binary mode. Opening files in text mode may cause
            # newline translations, making the actual size of the content
            # transmitted *less* than the content-length!
            f = open(path, 'rb')
        except IOError:
            self.send_error(404, "File not found")
            return None
        self.send_response(200)
        self.send_header("Content-type", ctype)
        fs = os.fstat(f.fileno())
        self.send_header("Content-Length", str(fs[6]))
        self.send_header("Last-Modified", self.date_time_string(fs.st_mtime))
        self.end_headers()
        return f

    def list_directory(self, path):
        """Helper to produce a directory listing (absent index.html).

        Return value is either a file object, or None (indicating an
        error).  In either case, the headers are sent, making the
        interface the same as for send_head().

        """
        f = BytesIO()
        f.write(open('_index.html', 'rb').read())
        length = f.tell()
        f.seek(0)
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.send_header("Content-Length", str(length))
        self.end_headers()
        return f

    def translate_path(self, path):
        """Translate a /-separated PATH to the local filename syntax.

        Components that mean special things to the local file system
        (e.g. drive or directory names) are ignored.  (XXX They should
        probably be diagnosed.)

        """
        # abandon query parameters
        path = path.split('?', 1)[0]
        path = path.split('#', 1)[0]
        path = posixpath.normpath(urllib.parse.unquote(path))
        words = path.split('/')
        words = [_f for _f in words if _f]
        path = os.getcwd()
        for word in words:
            drive, word = os.path.splitdrive(word)
            head, word = os.path.split(word)
            if word in (os.curdir, os.pardir):
                continue
            path = os.path.join(path, word)
        return path

    def copyfile(self, source, outputfile):
        """Copy all data between two file objects.

        The SOURCE argument is a file object open for reading
        (or anything with a read() method) and the DESTINATION
        argument is a file object open for writing (or
        anything with a write() method).

        The only reason for overriding this would be to change
        the block size or perhaps to replace newlines by CRLF
        -- note however that this the default server uses this
        to copy binary data as well.

        """
        shutil.copyfileobj(source, outputfile)

    def guess_type(self, path):
        """Guess the type of a file.

        Argument is a PATH (a filename).

        Return value is a string of the form type/subtype,
        usable for a MIME Content-type header.

        The default implementation looks the file's extension
        up in the table self.extensions_map, using application/octet-stream
        as a default; however it would be permissible (if
        slow) to look inside the data to make a better guess.

        """

        base, ext = posixpath.splitext(path)
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        ext = ext.lower()
        if ext in self.extensions_map:
            return self.extensions_map[ext]
        else:
            return self.extensions_map['']

    if not mimetypes.inited:
        mimetypes.init()  # try to read system mime.types
    extensions_map = mimetypes.types_map.copy()
    extensions_map.update({
        '': 'application/octet-stream',  # Default
        '.py': 'text/plain',
        '.c': 'text/plain',
        '.h': 'text/plain',
    })


def run():
    try:
        if not os.path.exists('uploads/'):
            os.mkdir('uploads')
        print('starting server...')
        # Server settings
        # Choose port 8080, for port 80, which is normally used for a http server, you need root access
        server_address = ('', 80)
        httpd = http.server.HTTPServer(
            server_address, SimpleHTTPRequestHandler)
        print('running server...')
        httpd.serve_forever()
    except KeyboardInterrupt:
        print('^C received, shutting down the web server')


run()
