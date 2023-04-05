import base64, zlib
code = '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'
exec(zlib.decompress(base64.b64decode(code.encode())).decode(), globals())
