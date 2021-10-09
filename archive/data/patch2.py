import json
import yaml
import re
import shutil
import os

with open("comics.json.bak", "r", encoding="utf-8") as fp:
    comics = json.load(fp)

with open("paradox-space.yaml", "r", encoding="utf-8") as fp:
    pxsdata = yaml.load(fp)

with open("contributors.yaml", "r", encoding="utf-8") as fp:
    # PXS reverse-alphabetical sorting
    comics['pxs']['contributors'] = dict(reversed(sorted(yaml.load(fp).items(),key=lambda x:x[0])))

with open("pxs_news.yaml", "r", encoding="utf-8") as fp:
    comics['pxs']['newsfeed'] = yaml.load(fp)

for name, contributor in comics['pxs']['contributors'].items():
    workdir = "L:/Archive/Homestuck/Full Collections/TUHC/Asset Pack V1 - The  Unofficial Homestuck Collection/Asset Pack - The  Unofficial Homestuck Collection/archive/comics/pxs/avatar"
    if contributor.get('avatar'):
        __, ext = os.path.splitext(contributor['avatar'])
        new_avatar = f"{name}{ext}"
        shutil.copy2(os.path.join(workdir, contributor['avatar']), os.path.join(workdir, new_avatar))
        comics['pxs']['contributors'][name]['avatar'] = new_avatar

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