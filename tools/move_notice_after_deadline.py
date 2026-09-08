from pathlib import Path

path = Path('index.html')
html = path.read_text(encoding='utf-8')

start_marker = '<section class="recruitment-notice-wrap" aria-labelledby="recruitment-notice-title">'
start = html.find(start_marker)
if start == -1:
    raise SystemExit('ERROR: recruitment notice not found')
end = html.find('</section>', start)
if end == -1:
    raise SystemExit('ERROR: recruitment notice end not found')
end += len('</section>')
notice = html[start:end]

# Remove the current notice placement.
html = html[:start] + html[end:]

# Place the notice immediately after the gold deadline strip and before 01 PROGRAM.
deadline_start = html.find('<div class="deadline" id="deadline">')
if deadline_start == -1:
    raise SystemExit('ERROR: deadline strip not found')
deadline_end = html.find('</div>', deadline_start)
if deadline_end == -1:
    raise SystemExit('ERROR: deadline strip closing div not found')
deadline_end += len('</div>')

html = html[:deadline_end] + '\n\n' + notice + '\n\n' + html[deadline_end:]

notice_pos = html.find(start_marker)
deadline_pos = html.find('<div class="deadline" id="deadline">')
info_pos = html.find('<section id="information">')
if not (deadline_pos != -1 and notice_pos != -1 and info_pos != -1 and deadline_pos < notice_pos < info_pos):
    raise SystemExit('ERROR: notice is not between deadline strip and information section')
if html.count('BCCA 스쿨링 캠프 14명 모집이 마감되었습니다') != 1:
    raise SystemExit('ERROR: recruitment notice duplicated or missing')

path.write_text(html, encoding='utf-8')
print('Moved recruitment notice after deadline strip, before 01 PROGRAM.')
