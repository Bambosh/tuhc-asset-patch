import json
import yaml
import re

with open("comics.json.bak", "r", encoding="utf-8") as fp:
    comics = json.load(fp)

with open("paradox-space.yaml", "r", encoding="utf-8") as fp:
    pxsdata = yaml.load(fp)

with open("contributors.yaml", "r", encoding="utf-8") as fp:
    comics['pxs']['contributors'] = yaml.load(fp)

for i, comicid in enumerate(comics['pxs']['list']):
    ikey = str(i + 1)
    tags = {
        pikey: re.findall(r"#(.+?)(?= #|$)", pxsdata[ikey]['pages'][pikey].get('tags'))
        for pikey in pxsdata[ikey]['pages']
        if pxsdata[ikey]['pages'][pikey].get('tags')
    }
    if tags:
        comics['pxs']['comics'][comicid]['tags'] = tags

for i, comicid in enumerate(comics['pxs']['list']):
    ikey = str(i + 1)
    for pikey in pxsdata[ikey]['pages']:
        if pxsdata[ikey]['pages'][pikey].get('alt'):
            alt1, alt2 = pxsdata[ikey]['pages'][pikey]['alt'], comics['pxs']['comics'][comicid]['titleText'][pikey]
            if alt1 != alt2:
                if alt1.strip() != alt2.strip():
                    print(i, comicid)
                    print(alt1, alt2, sep="\n")
                comics['pxs']['comics'][comicid]['titleText'][pikey] = alt1

with open("comics.json", "w", encoding="utf-8") as fp:
    json.dump(comics, fp, ensure_ascii=False, indent=2)