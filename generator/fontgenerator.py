import os
from fontTools.ttLib import TTFont

def get_font_info(font_path):
    font = TTFont(font_path)
    
    # 패밀리명, 웨이트, 스타일 초기화
    family_name = None
    weight = None
    style = None
    
    # name 테이블에서 패밀리명과 스타일 가져오기
    name_table = font['name']
    for record in name_table.names:
        name = record.string.decode('utf-16-be' if record.isUnicode() else 'latin-1')
        if record.nameID == 1:  # Font Family name
            family_name = name
        elif record.nameID == 2:  # Font Subfamily name (often contains style information)
            style = name
    
    # OS/2 테이블에서 웨이트 가져오기
    os2_table = font['OS/2']
    weight_class = os2_table.usWeightClass

    if weight_class <= 400:
        weight = 'normal'
    else:
        weight = 'bold'

    if style == 'Regular':
        style = 'normal'
    elif style == 'Italic':
        style = 'italic'
    elif style == 'Bold':
        style = 'bold'
    elif style == 'Bold Italic':
        style = 'italic'
    
    return family_name, font_path, weight, style

dir = "../fonts/"

li = [ str(f) for f in os.listdir(dir) ]

form = """
@font-face {
	font-family: '%s';
	src: url('%s') format('opentype');
	font-weight: %s;
	font-style: %s;
}
"""

res = ""

for i in li:
    res += (form % get_font_info(dir + i))

f = open('../css/fonts.css', 'w')
f.write(res)
f.close()