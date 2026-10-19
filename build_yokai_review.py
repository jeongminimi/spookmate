"""Build a local, read-only visual review page for the Supabase catalog."""

import csv
import html
import re
from pathlib import Path

from app import get_db, get_yokai_image_path


ROOT = Path(__file__).resolve().parent
OUTPUT = ROOT / "yokai_visual_review.html"


def decode_source_text(value: str) -> str:
    # The original CSV contains literal Unicode escapes in some text fields.
    return re.sub(r"\\u([0-9a-fA-F]{4})", lambda match: chr(int(match.group(1), 16)), value)


def main() -> None:
    source = next((ROOT / "데이터원본").glob("Spooksheet.csv"))
    with source.open(encoding="utf-8-sig", newline="") as file:
        descriptions = {
            int(row[0]): (decode_source_text(row[3]), row[4])
            for row in list(csv.reader(file))[1:]
        }

    connection = get_db()
    try:
        with connection.cursor() as cursor:
            cursor.execute("SELECT id, name FROM yokai_compendium ORDER BY CAST(id AS INTEGER)")
            yokai = cursor.fetchall()
    finally:
        connection.close()

    if len(yokai) != 73:
        raise ValueError(f"Expected 73 DB entries, got {len(yokai)}")

    cards = []
    images = set()
    for item in yokai:
        yokai_id = int(item["id"])
        name = item["name"].strip()
        image = get_yokai_image_path(yokai_id, name)
        if not image or not (ROOT / image).is_file() or image in images:
            raise ValueError(f"Unresolved or duplicate image for DB ID {yokai_id}")
        images.add(image)
        description, source_url = descriptions[yokai_id]
        escaped_name = html.escape(name)
        source_html = (
            f'<a href="{html.escape(source_url)}" target="_blank" rel="noopener noreferrer">설화 출처 보기</a>'
            if source_url.startswith(("https://", "http://"))
            else "<small>온라인 출처 링크 없음</small>"
        )
        cards.append(f"""
        <article class="card" data-id="{yokai_id}" data-name="{escaped_name}" data-image="{html.escape(image)}">
          <img src="{html.escape(image)}" alt="{escaped_name}" loading="lazy">
          <div class="body">
            <h2><span>#{yokai_id:02d}</span> {escaped_name}</h2>
            <small>{html.escape(image)}</small>
            <p class="description">{html.escape(description)}</p>
            {source_html}
            <label>판정
              <select class="decision">
                <option value="">아직 확인하지 않음</option>
                <option value="match">그림과 이름이 맞음</option>
                <option value="uncertain">판단 보류</option>
                <option value="mismatch">그림이 다름</option>
              </select>
            </label>
            <textarea class="note" placeholder="다르다면 보이는 특징이나 추정 이름을 적으세요."></textarea>
          </div>
        </article>""")

    page = """<!doctype html>
<html lang="ko"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>요괴 그림·이름 검수</title>
<style>
*{box-sizing:border-box}body{margin:0;background:#15171c;color:#f4f1e9;font:16px/1.55 system-ui,sans-serif}
header{position:sticky;top:0;z-index:1;background:#15171cf2;border-bottom:1px solid #555;padding:15px max(20px,calc((100vw - 1400px)/2))}
h1{font-size:1.35rem;margin:0 0 4px}header p{margin:0 0 10px;color:#bbb;font-size:.88rem}
.toolbar{display:flex;gap:12px;align-items:center;flex-wrap:wrap}select,button,textarea{font:inherit;border:1px solid #777;border-radius:5px;background:#272a32;color:#fff;padding:7px}
button{cursor:pointer;background:#a77938;color:#111;font-weight:700;border:0}#progress{margin-left:auto}
main{max-width:1400px;margin:auto;padding:20px;display:grid;grid-template-columns:repeat(auto-fit,minmax(320px,1fr));gap:20px}
.card{background:#24272e;border:2px solid #484d58;border-radius:8px;overflow:hidden}.card[data-status=match]{border-color:#4ca889}.card[data-status=mismatch]{border-color:#e36868}.card[data-status=uncertain]{border-color:#e0b05b}
.card img{display:block;width:100%;aspect-ratio:1;object-fit:contain;background:#101216}.body{padding:15px}
h2{font-size:1.1rem;margin:0}h2 span,small{color:#c7a66a}small{display:block}.description{min-height:7.5em;margin:12px 0;white-space:pre-line}
a{color:#b7d5ff;font-size:.88rem}label{display:block;margin-top:16px;font-weight:700}label select,.note{display:block;width:100%;margin-top:5px}.note{height:70px;resize:vertical}
.card[hidden]{display:none}
</style></head><body>
<header><h1>요괴 그림·이름 검수</h1><p>Supabase 이름 · 로컬 그림 · 원본 설화 설명을 비교하세요. 판정은 이 브라우저에만 저장되며 DB나 실제 매핑은 바뀌지 않습니다.</p>
<div class="toolbar"><label>보기 <select id="filter"><option value="all">전체</option><option value="pending">미검수</option><option value="issues">판단 보류·불일치</option></select></label>
<button id="export">판정 JSON 저장</button><span id="progress"></span></div></header>
<main>__CARDS__</main>
<script>
const key='spookmate-yokai-review-v1';
let saved={};try{saved=JSON.parse(localStorage.getItem(key)||'{}')}catch{}
const cards=[...document.querySelectorAll('.card')];
function refresh(){
 let reviewed=0,issues=0;
 for(const card of cards){
  const id=card.dataset.id, record=saved[id]||{};
  card.querySelector('.decision').value=record.status||'';
  card.querySelector('.note').value=record.note||'';
  card.dataset.status=record.status||'';
  if(record.status)reviewed++;
  if(record.status==='uncertain'||record.status==='mismatch')issues++;
  const filter=document.querySelector('#filter').value;
  card.hidden=filter==='pending'&&!!record.status || filter==='issues'&&!['uncertain','mismatch'].includes(record.status);
 }
 document.querySelector('#progress').textContent=`확인 ${reviewed}/73 · 보류/불일치 ${issues}`;
}
document.querySelector('main').addEventListener('input',event=>{
 const card=event.target.closest('.card');if(!card)return;
 saved[card.dataset.id]={status:card.querySelector('.decision').value,note:card.querySelector('.note').value};
 try{localStorage.setItem(key,JSON.stringify(saved))}catch{}
 refresh();
});
document.querySelector('#filter').addEventListener('change',refresh);
document.querySelector('#export').addEventListener('click',()=>{
 const result=cards.map(card=>({id:Number(card.dataset.id),name:card.dataset.name,image_url:card.dataset.image,...(saved[card.dataset.id]||{status:'',note:''})}));
 const link=document.createElement('a');link.href=URL.createObjectURL(new Blob([JSON.stringify(result,null,2)],{type:'application/json'}));
 link.download='yokai_image_review.json';link.click();setTimeout(()=>URL.revokeObjectURL(link.href),1000);
});
refresh();
</script></body></html>"""
    OUTPUT.write_text(page.replace("__CARDS__", "\n".join(cards)), encoding="utf-8")
    print(f"Built {OUTPUT.name} with {len(cards)} DB entries and {len(images)} unique images")


if __name__ == "__main__":
    main()
