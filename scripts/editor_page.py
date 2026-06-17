# -*- coding: utf-8 -*-
"""The single-page web UI for editor.py (one big HTML string named PAGE)."""

PAGE = r"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Site content editor</title>
<style>
  :root{
    --accent:#1f6feb; --bg:#f6f7f9; --card:#fff; --line:#e3e6ea;
    --text:#1b1f24; --muted:#6b7480; --danger:#c0392b; --ok:#1e8e54;
  }
  *{box-sizing:border-box}
  body{margin:0;font:15px/1.5 -apple-system,BlinkMacSystemFont,"Segoe UI",Roboto,Helvetica,Arial,sans-serif;
       color:var(--text);background:var(--bg)}
  header{position:sticky;top:0;z-index:5;background:var(--card);border-bottom:1px solid var(--line);
         padding:14px 20px;display:flex;align-items:center;gap:18px}
  header h1{font-size:17px;margin:0;font-weight:650}
  header .hint{color:var(--muted);font-size:13px}
  .tabs{display:flex;gap:6px;margin-left:auto}
  .tab{border:1px solid var(--line);background:#fff;border-radius:8px;padding:7px 14px;cursor:pointer;font-size:14px}
  .tab.active{background:var(--accent);color:#fff;border-color:var(--accent)}
  main{max-width:920px;margin:22px auto;padding:0 18px 80px}
  .panel{display:none}.panel.active{display:block}
  .row{background:var(--card);border:1px solid var(--line);border-radius:10px;padding:14px 16px;margin-bottom:10px}
  .row h3{margin:0 0 4px;font-size:15px}
  .row .meta{color:var(--muted);font-size:13px}
  .pill{display:inline-block;font-size:11px;padding:1px 8px;border-radius:20px;border:1px solid var(--line);margin-left:6px;vertical-align:middle}
  .pill.pub{background:#e8f3ff;border-color:#bcdcff;color:#1559b8}
  .pill.pre{background:#f3f0ff;border-color:#dcd2ff;color:#6a45c9}
  .pill.sel{background:#eafaf0;border-color:#bfe9cf;color:var(--ok)}
  .actions{margin-top:10px;display:flex;gap:8px;flex-wrap:wrap}
  button{font:inherit;border:1px solid var(--line);background:#fff;border-radius:8px;padding:6px 12px;cursor:pointer}
  button:hover{border-color:#c7ccd2}
  button.primary{background:var(--accent);color:#fff;border-color:var(--accent)}
  button.danger{color:var(--danger);border-color:#eccfcc}
  button.ghost{background:transparent}
  .add-bar{margin:6px 0 18px;display:flex;gap:8px}
  label{display:block;font-size:13px;color:var(--muted);margin:10px 0 4px}
  input[type=text],textarea,select{width:100%;padding:9px 10px;border:1px solid var(--line);border-radius:8px;font:inherit;background:#fff}
  textarea{min-height:70px;resize:vertical}
  .grid2{display:grid;grid-template-columns:1fr 1fr;gap:0 14px}
  .check{display:flex;align-items:center;gap:8px;margin-top:12px}
  .check input{width:auto}
  dialog{border:none;border-radius:14px;padding:0;max-width:640px;width:92vw;box-shadow:0 18px 60px rgba(0,0,0,.25)}
  dialog::backdrop{background:rgba(20,24,28,.45)}
  .dlg-head{padding:16px 20px;border-bottom:1px solid var(--line);font-weight:650}
  .dlg-body{padding:6px 20px 4px;max-height:65vh;overflow:auto}
  .dlg-foot{padding:14px 20px;border-top:1px solid var(--line);display:flex;gap:10px;justify-content:flex-end;align-items:center}
  .reorder{display:flex;flex-direction:column;gap:2px;margin-right:4px}
  .reorder button{padding:1px 7px;line-height:1.1;font-size:12px}
  .toast{position:fixed;left:50%;bottom:26px;transform:translateX(-50%);background:#1b1f24;color:#fff;
         padding:10px 16px;border-radius:10px;font-size:14px;opacity:0;transition:opacity .2s;pointer-events:none;z-index:50}
  .toast.show{opacity:1}
  .toast.err{background:var(--danger)}
  .empty{color:var(--muted);padding:20px;text-align:center}
  .muted{color:var(--muted)}
  .small{font-size:12px}
  .flex{display:flex;align-items:center;gap:10px}
  .grow{flex:1}
  .savehint{color:var(--muted);font-size:12px;margin-right:auto}
  code{background:#eef0f2;padding:1px 5px;border-radius:5px;font-size:12px}
</style>
</head>
<body>
<header>
  <h1>Site content editor</h1>
  <span class="hint">edits local files &middot; preview with <code>hugo server</code></span>
  <div class="tabs">
    <button class="tab active" data-tab="papers">Papers</button>
    <button class="tab" data-tab="awards">Awards</button>
    <button class="tab" data-tab="news">News</button>
  </div>
</header>

<main>
  <section class="panel active" id="papers">
    <div class="add-bar">
      <button class="primary" onclick="openPaper()">+ Add paper</button>
      <span class="savehint" id="papers-hint">Use ▲ ▼ to set the order papers appear in (applies within each section &amp; area).</span>
      <button class="ghost" id="papers-save" onclick="savePaperOrder()" disabled>Save order</button>
    </div>
    <div id="papers-list"></div>
  </section>

  <section class="panel" id="awards">
    <div class="add-bar">
      <button class="primary" onclick="openAward()">+ Add award</button>
      <span class="savehint" id="awards-dirty"></span>
      <button class="ghost" id="awards-save" onclick="saveAwards()" disabled>Save changes</button>
    </div>
    <div id="awards-list"></div>
  </section>

  <section class="panel" id="news">
    <div class="add-bar">
      <button class="primary" onclick="openNews()">+ Add news item</button>
      <span class="savehint" id="news-dirty"></span>
      <button class="ghost" id="news-save" onclick="saveNews()" disabled>Save changes</button>
    </div>
    <div id="news-list"></div>
  </section>
</main>

<!-- Paper dialog -->
<dialog id="paper-dlg">
  <form method="dialog">
    <div class="dlg-head" id="paper-title">Add paper</div>
    <div class="dlg-body">
      <div id="paper-add-only">
        <label>arXiv ID <span class="small muted">(auto-fills title &amp; authors)</span></label>
        <div class="flex">
          <input type="text" id="p-arxiv" class="grow" placeholder="e.g. 2505.20177">
          <button type="button" onclick="fetchArxiv()">Fetch</button>
        </div>
        <p class="small muted" id="p-fetched" style="margin:6px 0 0"></p>
      </div>
      <label>Title</label>
      <input type="text" id="p-title">
      <div id="p-manual">
        <label>Authors <span class="small muted">(semicolon or new line separated; your name is bolded automatically)</span></label>
        <textarea id="p-authors" placeholder="Jane Doe; Konstantinos Stavropoulos; John Roe"></textarea>
        <label>Year</label>
        <input type="text" id="p-year" placeholder="2025">
      </div>
      <div class="grid2">
        <div>
          <label>Research area</label>
          <select id="p-topic"></select>
        </div>
        <div>
          <label>Status</label>
          <select id="p-status">
            <option value="published">Published (in Selected + All)</option>
            <option value="preprint">Preprint (All only)</option>
          </select>
        </div>
      </div>
      <label>Venue <span class="small muted">(e.g. NeurIPS 2025; leave blank for "Under review")</span></label>
      <input type="text" id="p-venue">
      <label>Distinction badge <span class="small muted">(optional, e.g. Spotlight &middot; NeurIPS 2025)</span></label>
      <input type="text" id="p-award">
      <div class="grid2">
        <div><label>Link URL <span class="small muted">(title links here)</span></label><input type="text" id="p-url"></div>
        <div><label>PDF URL <span class="small muted">(optional)</span></label><input type="text" id="p-pdf"></div>
      </div>
    </div>
    <div class="dlg-foot">
      <span class="savehint" id="p-err"></span>
      <button type="button" onclick="closeDlg('paper-dlg')">Cancel</button>
      <button type="button" class="primary" id="p-save" onclick="savePaper()">Save</button>
    </div>
  </form>
</dialog>

<!-- Award dialog -->
<dialog id="award-dlg">
  <form method="dialog">
    <div class="dlg-head" id="award-title">Add award</div>
    <div class="dlg-body">
      <label>Title</label>
      <input type="text" id="a-title">
      <div class="grid2">
        <div><label>Date <span class="small muted">(e.g. 2025, or 2022 – 2025)</span></label><input type="text" id="a-date"></div>
        <div><label>Link URL <span class="small muted">(optional)</span></label><input type="text" id="a-url"></div>
      </div>
      <label>Description <span class="small muted">(Markdown allowed: *italics*, [links](url))</span></label>
      <textarea id="a-desc"></textarea>
      <div class="check"><input type="checkbox" id="a-selected"><label for="a-selected" style="margin:0;color:var(--text)">Show in the "Selected" highlights tab</label></div>
    </div>
    <div class="dlg-foot">
      <button type="button" onclick="closeDlg('award-dlg')">Cancel</button>
      <button type="button" class="primary" onclick="commitAward()">Done</button>
    </div>
  </form>
</dialog>

<!-- News dialog -->
<dialog id="news-dlg">
  <form method="dialog">
    <div class="dlg-head" id="news-dlg-title">Add news item</div>
    <div class="dlg-body">
      <label>Date <span class="small muted">(free text, e.g. June 2026 or Fall 2026)</span></label>
      <input type="text" id="n-date">
      <label>Text <span class="small muted">(HTML allowed: &lt;strong&gt;, &lt;a href="..."&gt;...&lt;/a&gt;)</span></label>
      <textarea id="n-body"></textarea>
    </div>
    <div class="dlg-foot">
      <button type="button" onclick="closeDlg('news-dlg')">Cancel</button>
      <button type="button" class="primary" onclick="commitNews()">Done</button>
    </div>
  </form>
</dialog>

<div class="toast" id="toast"></div>

<script>
let S = {areas:[], papers:[], awards:[], news:[], me:""};
let awardsDraft = null, newsDraft = null, papersDraft = null;
let editIdx = -1;
const $ = s => document.querySelector(s);
const esc = s => (s==null?"":String(s)).replace(/[&<>"]/g,c=>({"&":"&amp;","<":"&lt;",">":"&gt;",'"':"&quot;"}[c]));

function toast(msg, err){
  const t=$("#toast"); t.textContent=msg; t.className="toast show"+(err?" err":"");
  setTimeout(()=>t.className="toast",2200);
}
async function api(path, body){
  const r = await fetch(path,{method:"POST",headers:{"Content-Type":"application/json"},body:JSON.stringify(body||{})});
  const j = await r.json();
  if(!r.ok || j.error) throw new Error(j.error||("HTTP "+r.status));
  return j;
}
async function load(){
  const r = await fetch("/api/state"); S = await r.json();
  awardsDraft = JSON.parse(JSON.stringify(S.awards));
  newsDraft = JSON.parse(JSON.stringify(S.news));
  papersDraft = JSON.parse(JSON.stringify(S.papers));
  renderPapers(); renderAwards(); renderNews();
  markPapers(false); markAwards(false); markNews(false);
}

/* ---------- tabs ---------- */
document.querySelectorAll(".tab").forEach(t=>t.onclick=()=>{
  document.querySelectorAll(".tab").forEach(x=>x.classList.remove("active"));
  document.querySelectorAll(".panel").forEach(x=>x.classList.remove("active"));
  t.classList.add("active"); $("#"+t.dataset.tab).classList.add("active");
});
function closeDlg(id){ $("#"+id).close(); }

/* ---------- PAPERS ---------- */
function markPapers(d){ $("#papers-save").disabled=!d; if(d) $("#papers-hint").textContent="Unsaved order changes"; }
function renderPapers(){
  const el=$("#papers-list");
  if(!papersDraft.length){ el.innerHTML='<div class="empty">No papers yet.</div>'; return; }
  el.innerHTML = papersDraft.map((p,i)=>{
    const pill = p.featured ? '<span class="pill pub">Published</span>' : '<span class="pill pre">Preprint</span>';
    const award = p.award ? ' <span class="pill sel">'+esc(p.award)+'</span>' : '';
    const authors = esc(p.authors.join(", "));
    const venue = p.venue?(" &middot; <i>"+esc(p.venue)+"</i>"):"";
    return `<div class="row"><div class="flex">
      <div class="reorder">
        <button ${i==0?"disabled":""} onclick="moveP(${i},-1)">▲</button>
        <button ${i==papersDraft.length-1?"disabled":""} onclick="moveP(${i},1)">▼</button>
      </div>
      <div class="grow">
        <h3>${esc(p.title)} ${pill}${award}</h3>
        <div class="meta">${authors}</div>
        <div class="meta small">${esc(p.category)||"<span class='muted'>no area</span>"}${venue}</div>
      </div></div>
      <div class="actions">
        <button onclick="openPaper(${i})">Edit</button>
        ${p.url?`<button class="ghost" onclick="window.open('${esc(p.url)}','_blank')">Open link</button>`:""}
        <button class="danger" onclick="delPaper(${i})">Delete</button>
      </div></div>`;
  }).join("");
}
function moveP(i,d){ const j=i+d; [papersDraft[i],papersDraft[j]]=[papersDraft[j],papersDraft[i]]; renderPapers(); markPapers(true); }
async function savePaperOrder(){
  try{ await api("/api/papers/reorder",{order:papersDraft.map(p=>p.slug)}); await load(); toast("Order saved"); }
  catch(e){ toast(e.message,true); }
}
function fillTopics(sel){
  const opts = S.areas.map(a=>`<option>${esc(a)}</option>`).join("")+`<option>Other</option>`;
  $("#p-topic").innerHTML = opts;
  if(sel){ $("#p-topic").value = sel; if($("#p-topic").value!==sel){ $("#p-topic").innerHTML += `<option>${esc(sel)}</option>`; $("#p-topic").value=sel; } }
}
function openPaper(i){
  editIdx = (i==null?-1:i);
  const adding = editIdx<0;
  $("#paper-title").textContent = adding?"Add paper":"Edit paper";
  $("#paper-add-only").style.display = adding?"block":"none";
  $("#p-manual").style.display = adding?"block":"none";
  $("#p-err").textContent=""; $("#p-fetched").textContent="";
  fillTopics(adding?null:papersDraft[i].category);
  if(adding){
    ["p-arxiv","p-title","p-authors","p-year","p-venue","p-award","p-url","p-pdf"].forEach(id=>$("#"+id).value="");
    $("#p-status").value="published";
  }else{
    const p=papersDraft[i];
    $("#p-title").value=p.title; $("#p-venue").value=p.venue; $("#p-award").value=p.award;
    $("#p-url").value=p.url; $("#p-pdf").value=p.url_pdf; $("#p-status").value=p.status;
  }
  $("#paper-dlg").showModal();
}
async function fetchArxiv(){
  const id=$("#p-arxiv").value.trim(); if(!id){ return; }
  $("#p-fetched").textContent="Fetching…";
  try{
    const j=await api("/api/arxiv",{arxiv:id});
    $("#p-title").value=j.meta.title;
    $("#p-authors").value=j.meta.authors.join("; ");
    $("#p-year").value=j.meta.year;
    $("#p-url").value=j.meta.url; $("#p-pdf").value=j.meta.pdf;
    $("#p-fetched").textContent="Filled from arXiv: "+j.meta.authors.length+" authors, "+j.meta.year+".";
  }catch(e){ $("#p-fetched").textContent="Could not fetch: "+e.message; }
}
async function savePaper(){
  const adding = editIdx<0;
  try{
    if(adding){
      await api("/api/paper/add",{
        arxiv:$("#p-arxiv").value.trim(), title:$("#p-title").value.trim(),
        authors:$("#p-authors").value.trim(), year:$("#p-year").value.trim(),
        topic:$("#p-topic").value, status:$("#p-status").value,
        venue:$("#p-venue").value.trim(), award:$("#p-award").value.trim(),
        url:$("#p-url").value.trim(), pdf:$("#p-pdf").value.trim(),
      });
    }else{
      await api("/api/paper/edit",{
        slug:papersDraft[editIdx].slug, title:$("#p-title").value.trim(),
        category:$("#p-topic").value, status:$("#p-status").value,
        venue:$("#p-venue").value.trim(), award:$("#p-award").value,
        url:$("#p-url").value.trim(), url_pdf:$("#p-pdf").value,
      });
    }
    $("#paper-dlg").close(); await load(); toast(adding?"Paper added":"Paper updated");
  }catch(e){ $("#p-err").textContent=e.message; }
}
async function delPaper(i){
  if(!confirm("Delete \""+papersDraft[i].title+"\"? This removes its folder.")) return;
  try{ await api("/api/paper/delete",{slug:papersDraft[i].slug}); await load(); toast("Paper deleted"); }
  catch(e){ toast(e.message,true); }
}

/* ---------- AWARDS (draft + explicit save) ---------- */
function markAwards(d){ $("#awards-save").disabled=!d; $("#awards-dirty").textContent=d?"Unsaved changes":""; }
function renderAwards(){
  const el=$("#awards-list");
  if(!awardsDraft.length){ el.innerHTML='<div class="empty">No awards yet.</div>'; return; }
  el.innerHTML = awardsDraft.map((a,i)=>`<div class="row"><div class="flex">
      <div class="reorder">
        <button ${i==0?"disabled":""} onclick="moveAward(${i},-1)">▲</button>
        <button ${i==awardsDraft.length-1?"disabled":""} onclick="moveAward(${i},1)">▼</button>
      </div>
      <div class="grow">
        <h3>${esc(a.title)} ${a.selected?'<span class="pill sel">Selected</span>':""}</h3>
        <div class="meta small">${esc(a.date)}</div>
        <div class="meta">${esc(a.description)}</div>
      </div>
    </div>
    <div class="actions">
      <button onclick="openAward(${i})">Edit</button>
      <button class="danger" onclick="delAward(${i})">Delete</button>
    </div></div>`).join("");
}
function openAward(i){
  editIdx=(i==null?-1:i);
  $("#award-title").textContent = editIdx<0?"Add award":"Edit award";
  const a = editIdx<0?{title:"",date:"",url:"",description:"",selected:true}:awardsDraft[i];
  $("#a-title").value=a.title; $("#a-date").value=a.date; $("#a-url").value=a.url||"";
  $("#a-desc").value=a.description; $("#a-selected").checked=!!a.selected;
  $("#award-dlg").showModal();
}
function commitAward(){
  const a={title:$("#a-title").value.trim(),date:$("#a-date").value.trim(),
           url:$("#a-url").value.trim(),description:$("#a-desc").value.trim(),
           selected:$("#a-selected").checked};
  if(!a.title){ toast("Title is required",true); return; }
  if(editIdx<0) awardsDraft.push(a); else awardsDraft[editIdx]=a;
  $("#award-dlg").close(); renderAwards(); markAwards(true);
}
function moveAward(i,d){ const j=i+d; [awardsDraft[i],awardsDraft[j]]=[awardsDraft[j],awardsDraft[i]]; renderAwards(); markAwards(true); }
function delAward(i){ if(!confirm("Remove this award?"))return; awardsDraft.splice(i,1); renderAwards(); markAwards(true); }
async function saveAwards(){
  try{ await api("/api/awards/save",{awards:awardsDraft}); await load(); toast("Awards saved"); }
  catch(e){ toast(e.message,true); }
}

/* ---------- NEWS (draft + explicit save) ---------- */
function markNews(d){ $("#news-save").disabled=!d; $("#news-dirty").textContent=d?"Unsaved changes":""; }
function renderNews(){
  const el=$("#news-list");
  if(!newsDraft.length){ el.innerHTML='<div class="empty">No news items yet.</div>'; return; }
  el.innerHTML = newsDraft.map((n,i)=>`<div class="row"><div class="flex">
      <div class="reorder">
        <button ${i==0?"disabled":""} onclick="moveNews(${i},-1)">▲</button>
        <button ${i==newsDraft.length-1?"disabled":""} onclick="moveNews(${i},1)">▼</button>
      </div>
      <div class="grow">
        <h3 style="font-weight:600">${esc(n.date)}</h3>
        <div class="meta">${esc(n.body)}</div>
      </div></div>
    <div class="actions">
      <button onclick="openNews(${i})">Edit</button>
      <button class="danger" onclick="delNews(${i})">Delete</button>
    </div></div>`).join("");
}
function openNews(i){
  editIdx=(i==null?-1:i);
  $("#news-dlg-title").textContent = editIdx<0?"Add news item":"Edit news item";
  const n = editIdx<0?{date:"",body:""}:newsDraft[i];
  $("#n-date").value=n.date; $("#n-body").value=n.body;
  $("#news-dlg").showModal();
}
function commitNews(){
  const n={date:$("#n-date").value.trim(),body:$("#n-body").value.trim()};
  if(!n.date && !n.body){ toast("Add a date or text",true); return; }
  if(editIdx<0) newsDraft.unshift(n); else newsDraft[editIdx]=n;
  $("#news-dlg").close(); renderNews(); markNews(true);
}
function moveNews(i,d){ const j=i+d; [newsDraft[i],newsDraft[j]]=[newsDraft[j],newsDraft[i]]; renderNews(); markNews(true); }
function delNews(i){ if(!confirm("Remove this news item?"))return; newsDraft.splice(i,1); renderNews(); markNews(true); }
async function saveNews(){
  try{ await api("/api/news/save",{news:newsDraft}); await load(); toast("News saved"); }
  catch(e){ toast(e.message,true); }
}

load();
</script>
</body>
</html>
"""
