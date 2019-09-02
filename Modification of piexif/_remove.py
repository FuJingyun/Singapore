import io

from ._common import *
from piexif import _webp

def remove(src, new_file=None):
    """
    py:function:: piexif.remove(filename)

    Remove exif from JPEG.

    :param str filename: JPEG
    """
    global file_type
    output_is_file = False
    if src[0:2] == b"\xff\xd8":
        src_data = src
        file_type = "jpeg"
        
        
        
        
        
        
        
    elif src[0:4] == b"RIFF" and src[8:12] == b"WEBP":
        src_data = src
        file_type = "webp"
    else:
        with open(src, 'rb') as f:
            src_data = f.read()
        output_is_file = True
        if src_data[0:2] == b"\xff\xd8":
            file_type = "jpeg"
        elif src_data[0:4] == b"RIFF" and src_data[8:12] == b"WEBP":
            file_type = "webp"


#     f = open(filename, "rb")
#    data = f.read(6)
#
#    if data[0:2] != b"\xff\xd8":
#
#



    if file_type == "jpeg" and src_data[0:2] == b"\xff\xd8" :
        segments = split_into_segments(src_data)
        exif = get_exif_seg(segments)
        global new_data
        if exif:
            new_data = src_data.replace(exif, b"")
        else:
            new_data = src_data
    elif file_type == "webp":
        try:
            new_data = _webp.remove(src_data)
        except ValueError:
            new_data = src_data
        except e:
            print(e.args)
            raise ValueError("Error occurred.")

    if isinstance(new_file, io.BytesIO):
        new_file.write(new_data)
        new_file.seek(0)
    elif new_file:
        with open(new_file, "wb+") as f:
            f.write(new_data)
    elif output_is_file:
        with open(src, "wb+") as f:
            f.write(new_data)
    else:
        raise ValueError("Give a second argument to 'remove' to output file")