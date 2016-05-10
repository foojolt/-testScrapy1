# -*- coding: utf-8 -*-

import re

src = "shanghai-list-http.dat"
#／\／www.sgs.gov.cn\／notice\／notice\／view?uuid=9DfasM8QpxmvTU42ENS4iEGIlxBO65YX&tab=01" target="_blank">上海开滦海运有限公司<\／a><\／td>             \n

namePattern = re.compile( r'view[?]uuid=[^&]+&tab=01" target="_blank">(?P<name>[^<]+)' )

with open( src, 'r' ) as f:
    for line in f:
        for mat in namePattern.finditer( line ):
            gd = mat.groupdict()
            if gd.get("name"):
                print gd["name"]
