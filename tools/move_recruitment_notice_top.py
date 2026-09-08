from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

start_marker = '<section class="recruitment-notice-wrap" aria-labelledby="recruitment-notice-title">'
start = html.find(start_marker)
if start == -1:
    raise SystemExit('ERROR: recruitment notice section not found')
end = html.find('</section>', start)
if end == -1:
    raise SystemExit('ERROR: recruitment notice closing section not found')
end += len('</section>')
notice = html[start:end]

# Remove current placement first.
html = html[:start] + html[end:]

# The page header contains the navigation and hero, so place the notice immediately
# after the navigation, before the hero content begins.
nav_end = html.find('</nav>')
if nav_end != -1:
    insert_at = nav_end + len('</nav>')
else:
    body_open = html.find('<body>')
    if body_open == -1:
        raise SystemExit('ERROR: neither </nav> nor <body> found')
    insert_at = body_open + len('<body>')

html = html[:insert_at] + '\n\n' + notice + '\n\n' + html[insert_at:]

notice_pos = html.find(start_marker)
hero_pos = html.find('<h1>한국의 겨울방학은')
if notice_pos == -1 or hero_pos == -1:
    raise SystemExit('ERROR: validation anchors missing')
if notice_pos > hero_pos:
    raise SystemExit('ERROR: notice is still below hero')
if html.count('BCCA 스쿨링 캠프 14명 모집이 마감되었습니다') != 1:
    raise SystemExit('ERROR: recruitment notice duplicated or missing')

path.write_text(html, encoding='utf-8')
print('Moved recruitment notice immediately below navigation, before hero.')
