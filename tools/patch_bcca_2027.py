from pathlib import Path
import json
import re

path = Path("index.html")
html = path.read_text(encoding="utf-8")

replacements = {
    "<title>2027 캐나다 밴쿠버 겨울 스쿨링 캠프 | BCCA 정규수업 4주 + 미서부 투어 | TNS유학</title>":
        "<title>2027 캐나다 밴쿠버 겨울 스쿨링 캠프 | BCCA 정규수업 4주 | TNS유학</title>",
    '<meta name="description" content="2027년 1월 13일~2월 13일, 밴쿠버 명문 사립학교 BC Christian Academy 정규수업 4주와 LA 미서부 투어 5일. 초등 5학년~고등 1학년 20명 소수 정원. 비용 CAD 11,600.">':
        '<meta name="description" content="초5~고1 대상 2027 캐나다 겨울방학 스쿨링. BCCA 정규수업 4주와 미서부 4박5일, 홈스테이, 방과후 영어·수학을 결합한 5주 프로그램.">',
    '<meta property="og:description" content="현지 학생들과 같은 교실에서 보내는 5주. 초5~고1 20명 소수 정원 모집.">':
        '<meta property="og:description" content="BCCA 정규수업 4주 + 미서부 4박5일. 초5~고1 대상 5주 캐나다 겨울방학 스쿨링.">',
    '<meta name="twitter:description" content="현지 학생들과 같은 교실에서 보내는 5주. 초5~고1 20명 소수 정원 모집.">':
        '<meta name="twitter:description" content="BCCA 정규수업 4주 + 미서부 4박5일. 초5~고1 대상 5주 캐나다 겨울방학 스쿨링.">',
    "      LA 미서부 투어로 시작해, 밴쿠버 명문 사립학교 정규수업 4주로 이어집니다.":
        "      미서부 4박5일로 시작해, BCCA 정규수업 4주로 이어집니다.",
}

for old, new in replacements.items():
    if old not in html:
        raise SystemExit(f"Expected source text not found: {old[:90]}")
    html = html.replace(old, new, 1)

# Meta keywords are ignored by modern search engines and can encourage awkward keyword stuffing.
html = re.sub(r'\n<meta name="keywords"[^>]*>', '', html, count=1)

if '<meta name="robots"' not in html:
    marker = '<meta name="viewport" content="width=device-width, initial-scale=1.0">'
    html = html.replace(marker, marker + '\n<meta name="robots" content="index,follow,max-image-preview:large,max-snippet:-1">', 1)

schema = {
    "@context": "https://schema.org",
    "@graph": [
        {
            "@type": "WebPage",
            "@id": "https://bcca-winter.netlify.app/#webpage",
            "url": "https://bcca-winter.netlify.app/",
            "name": "2027 캐나다 밴쿠버 겨울 스쿨링 캠프 | BCCA 정규수업 4주",
            "description": "초5~고1 대상 2027 캐나다 겨울방학 스쿨링. BCCA 정규수업 4주와 미서부 4박5일, 홈스테이, 방과후 영어·수학을 결합한 5주 프로그램.",
            "inLanguage": "ko-KR",
            "about": {"@id": "https://bcca-winter.netlify.app/#event"}
        },
        {
            "@type": "EducationEvent",
            "@id": "https://bcca-winter.netlify.app/#event",
            "name": "2027 BCCA 겨울 스쿨링 캠프",
            "startDate": "2027-01-13",
            "endDate": "2027-02-13",
            "eventStatus": "https://schema.org/EventScheduled",
            "eventAttendanceMode": "https://schema.org/OfflineEventAttendanceMode",
            "location": {
                "@type": "Place",
                "name": "BCCA",
                "address": {
                    "@type": "PostalAddress",
                    "addressLocality": "Port Coquitlam",
                    "addressRegion": "BC",
                    "addressCountry": "CA"
                }
            },
            "organizer": {"@type": "Organization", "name": "TNS유학"},
            "offers": {
                "@type": "Offer",
                "price": "11600",
                "priceCurrency": "CAD",
                "availability": "https://schema.org/LimitedAvailability",
                "url": "https://bcca-winter.netlify.app/#inquiry"
            }
        },
        {
            "@type": "FAQPage",
            "@id": "https://bcca-winter.netlify.app/#faq-schema",
            "mainEntity": [
                {
                    "@type": "Question",
                    "name": "정규수업과 ESL 비중은 어떻게 되나요?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "일반적으로 정규수업 70~80%에 ESL 20~30%로 운영합니다. 고등학생(G9 이상)은 영어 수준과 학교 상황에 따라 정규 60% + ESL 40%로 조정될 수 있습니다. 실제 비율은 학생의 영어 수준과 학교 재량으로 결정됩니다."
                    }
                },
                {
                    "@type": "Question",
                    "name": "현재 학년 그대로 배정되나요?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "반드시 그렇지는 않습니다. 학교가 학생의 영어 수준과 당시 학급 상황을 함께 고려하기 때문에 현재 학년보다 한두 학년 위 또는 아래로 배정될 수 있습니다."
                    }
                },
                {
                    "@type": "Question",
                    "name": "초등학교 5학년도 참가할 수 있나요?",
                    "acceptedAnswer": {
                        "@type": "Answer",
                        "text": "가능하지만 정원이 가장 제한적입니다. 부모님과 떨어져 해외 캠프나 단독 프로그램에 참여한 경험이 있고 스스로 생활이 가능한 학생 위주로 등록을 받습니다. 초등 4학년은 개별 문의로 참가 여부를 확인합니다."
                    }
                }
            ]
        }
    ]
}

if 'https://bcca-winter.netlify.app/#faq-schema' not in html:
    block = '\n<script type="application/ld+json">\n' + json.dumps(schema, ensure_ascii=False, separators=(",", ":")) + '\n</script>\n'
    html = html.replace('</head>', block + '</head>', 1)

path.write_text(html, encoding="utf-8")
print("Patched index.html while preserving the existing layout and embedded images.")
