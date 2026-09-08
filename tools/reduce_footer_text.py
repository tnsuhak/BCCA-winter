from pathlib import Path
p=Path('index.html')
s=p.read_text(encoding='utf-8')
old1=".tags span{\n  border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:8px 16px;\n  font-size:13.5px;color:#c2d3e2;font-weight:300;\n}"
new1=".tags span{\n  border:1px solid rgba(255,255,255,.22);border-radius:999px;padding:7px 13px;\n  font-size:11.5px;color:#c2d3e2;font-weight:300;\n}"
old2=".disclaimer{\n  margin-top:32px;padding-top:26px;border-top:1px solid rgba(255,255,255,.14);\n  font-size:13.5px;color:#93a8bb;font-weight:300;line-height:1.9;\n}"
new2=".disclaimer{\n  margin-top:28px;padding-top:22px;border-top:1px solid rgba(255,255,255,.14);\n  font-size:11.8px;color:#93a8bb;font-weight:300;line-height:1.7;\n}"
if old1 not in s: raise SystemExit('tags css not found')
if old2 not in s: raise SystemExit('disclaimer css not found')
s=s.replace(old1,new1,1).replace(old2,new2,1)
insert='''\n@media(max-width:760px){\n  .tags{gap:7px;margin-top:24px;}\n  .tags span{font-size:10.5px;padding:6px 11px;}\n  .disclaimer{font-size:10.8px;line-height:1.65;margin-top:24px;padding-top:20px;}\n}\n'''
anchor='''.note{margin-top:26px;font-size:14.5px;color:#6b7787;font-weight:300;text-align:center;}'''
if anchor in s and insert.strip() not in s:
    s=s.replace(anchor,anchor+insert,1)
p.write_text(s,encoding='utf-8')
print('Reduced footer tag and disclaimer text sizes.')
