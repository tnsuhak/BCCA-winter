from pathlib import Path
import re

path = Path('index.html')
html = path.read_text(encoding='utf-8')

start = re.search(r'<section\b[^>]*\bid=["\']faq["\'][^>]*>', html, re.I)
if not start:
    raise SystemExit('FAQ section not found')
end = html.find('</section>', start.end())
if end < 0:
    raise SystemExit('FAQ section closing tag not found')
end += len('</section>')
faq = html[start.start():end]

# Keep every FAQ collapsed in the initial HTML state.
faq = re.sub(r'(<details\b[^>]*?)\s+open(?:\s*=\s*(?:["\']open["\']|open))?', r'\1', faq, flags=re.I)
faq = re.sub(r'aria-expanded\s*=\s*["\']true["\']', 'aria-expanded="false"', faq, flags=re.I)

def clean_state_classes(match):
    quote, value = match.group(1), match.group(2)
    tokens = value.split()
    state = {'open', 'active', 'is-open', 'expanded', 'show'}
    # Only strip state classes from FAQ/accordion-related elements.
    if any(('faq' in t.lower() or 'accordion' in t.lower()) for t in tokens):
        tokens = [t for t in tokens if t.lower() not in state]
    return 'class=' + quote + ' '.join(tokens) + quote

faq = re.sub(r'class=(["\'])(.*?)\1', clean_state_classes, faq, flags=re.I | re.S)
html = html[:start.start()] + faq + html[end:]

# Existing page JS may reopen the first item during initialization. Normalize once
# immediately after DOMContentLoaded, then leave the normal click behavior alone.
marker = 'tns-faq-initial-collapse'
if marker not in html:
    script = r'''<script id="tns-faq-initial-collapse">
(function(){
  function collapseFaqInitially(){
    var faq=document.getElementById('faq');
    if(!faq) return;
    faq.querySelectorAll('details[open]').forEach(function(el){el.removeAttribute('open');});
    faq.querySelectorAll('[aria-expanded="true"]').forEach(function(el){el.setAttribute('aria-expanded','false');});
    faq.querySelectorAll('[class]').forEach(function(el){
      var classes=Array.prototype.slice.call(el.classList);
      var related=/faq|accordion/i.test(classes.join(' ')) || !!el.closest('.faq-item,.faq-row,.accordion-item');
      if(!related) return;
      ['open','active','is-open','expanded','show'].forEach(function(c){el.classList.remove(c);});
    });
    faq.querySelectorAll('.faq-a,.faq-answer,.faq-content,.accordion-content,.accordion-body').forEach(function(el){
      el.style.removeProperty('max-height');
      el.style.removeProperty('height');
      if(el.style.display==='block') el.style.removeProperty('display');
    });
  }
  function run(){window.requestAnimationFrame(collapseFaqInitially);}
  if(document.readyState==='loading') document.addEventListener('DOMContentLoaded',run,{once:true});
  else run();
})();
</script>'''
    if '</body>' not in html:
        raise SystemExit('body closing tag not found')
    html = html.replace('</body>', script + '\n</body>', 1)

if marker not in html:
    raise SystemExit('FAQ collapse marker missing')
path.write_text(html, encoding='utf-8')
print('FAQ initial state normalized to collapsed')
