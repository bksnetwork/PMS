const E=s=>String(s??'').replace(/[&<>"]/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;'}[c]));let data=null,tab='dashboard';const C=document.querySelector('#content'),fallback={
  "tracked": 7,
  "species": 2,
  "pokemon": [
    {
      "dex_no": 425,
      "name": "Drifloon",
      "cp": 667,
      "gender": "M",
      "appraisal_stars": 3,
      "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/425.png"
    },
    {
      "dex_no": 425,
      "name": "Drifloon",
      "cp": 559,
      "gender": "F",
      "appraisal_stars": 3,
      "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/425.png"
    },
    {
      "dex_no": 425,
      "name": "Drifloon",
      "cp": 191,
      "gender": "M",
      "appraisal_stars": 3,
      "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/425.png"
    },
    {
      "dex_no": 425,
      "name": "Drifloon",
      "cp": 596,
      "gender": "F",
      "appraisal_stars": 1,
      "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/425.png"
    },
    {
      "dex_no": 425,
      "name": "Drifloon",
      "cp": 445,
      "gender": "M",
      "appraisal_stars": 1,
      "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/425.png"
    },
    {
      "dex_no": 425,
      "name": "Drifloon",
      "cp": 192,
      "gender": "M",
      "appraisal_stars": 0,
      "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/425.png"
    },
    {
      "dex_no": 426,
      "name": "Drifblim",
      "cp": 1381,
      "appraisal_stars": 3,
      "image_url": "https://raw.githubusercontent.com/PokeAPI/sprites/master/sprites/pokemon/other/official-artwork/426.png"
    }
  ],
  "storage": {
    "used": 1278,
    "capacity": 1325,
    "last_updated": "2026-09-27 00:20 ET"
  },
  "resources": {
    "stardust": 594642,
    "bulbasaur_candy": 86,
    "bulbasaur_candy_xl": 1,
    "gastly_candy": 53,
    "gastly_candy_xl": 2,
    "gengar_mega_energy": 0
  },
  "cleanup": {
    "total_transferred": 38,
    "transfer_queue": 0,
    "families": [
      {
        "family": "Drifloon",
        "status": "Complete — 23 transferred, 6 kept"
      },
      {
        "family": "Bulbasaur",
        "status": "Complete — 9 transferred, 3 kept"
      },
      {
        "family": "Gastly",
        "status": "Complete — 6 transferred, 5 kept; Gengar missing"
      }
    ]
  },
  "events": [
    {
      "date": "Oct 1, 6–7 PM",
      "name": "Seedot Spotlight Hour",
      "bonus": "2× Catch XP"
    },
    {
      "date": "Oct 8, 6–7 PM",
      "name": "Elgyem Spotlight Hour",
      "bonus": "2× Catch Candy"
    },
    {
      "date": "Oct 15, 6–7 PM",
      "name": "Stufful Spotlight Hour",
      "bonus": "2× Transfer Candy"
    },
    {
      "date": "Oct 22, 6–7 PM",
      "name": "Morelull Spotlight Hour",
      "bonus": "2× Catch Stardust"
    },
    {
      "date": "Oct 29, 6–7 PM",
      "name": "Gastly Spotlight Hour",
      "bonus": "2× Evolution XP"
    }
  ],
  "collection_status": {
    "tracked_records": 7,
    "note": "PMS currently contains verified detailed records only; family audits are preserved separately while full inventory import is built."
  }
};
document.querySelector('#copy-code').onclick=async function(){try{await navigator.clipboard.writeText('485010036135');this.textContent='Copied!'}catch(e){this.textContent='4850 1003 6135'}};
function card(p){return '<article class="poke-card"><img src="'+E(p.image_url)+'" alt="'+E(p.name)+'"><div><b>'+E(p.name)+'</b><small>#'+String(p.dex_no).padStart(4,'0')+'</small></div><p><span>CP '+(p.cp??'?')+'</span><span>'+(p.appraisal_stars??'?')+'★</span><span>'+E(p.gender||'—')+'</span></p></article>'}
function metric(v,l,s=''){return '<article class="metric"><b>'+E(v)+'</b><span>'+E(l)+'</span>'+(s?'<small>'+E(s)+'</small>':'')+'</article>'}
function familyRows(){return data.cleanup.families.map(f=>'<article class="row"><div><b>'+E(f.family)+'</b><small>'+E(f.status)+(f.transferred!=null?' · '+E(f.transferred)+' transferred':'')+(f.kept!=null?' · '+E(f.kept)+' kept':'')+(f.notes?' · '+E(f.notes):'')+'</small></div><span>›</span></article>').join('')}
function remainingRows(){return (data.cleanup.remaining_event_families||[]).map((f,i)=>'<article class="row"><div><b>'+(i+1)+'. '+E(f)+'</b><small>'+(i===0?'NEXT FAMILY':'Pending audit')+'</small></div><span>›</span></article>').join('')}
function eventRow(e){return '<article class="event"><div><b>'+E(e.name)+'</b><small>'+E(e.date)+'</small></div><span>'+E(e.bonus)+'</span></article>'}
function render(){if(!data)return;const pill=document.querySelector('#storage-pill');if(pill)pill.textContent=data.storage.used+' / '+data.storage.capacity;if(tab==='dashboard')C.innerHTML='<section class="metrics">'+metric(data.storage.used+' / '+data.storage.capacity,'Pokémon storage',(data.storage.capacity-data.storage.used)+' free')+metric(Number(data.resources.stardust).toLocaleString(),'Stardust')+metric(data.cleanup.total_transferred,'Transferred','this cleanup')+metric(data.collection_status?.tracked_records||data.tracked,'Detailed records','verified so far')+'</section><div class="two"><section><div class="section-title"><h2>Cleanup progress</h2><button data-go="cleanup">Open cleanup</button></div>'+familyRows()+'</section><section><div class="section-title"><h2>Upcoming</h2><button data-go="calendar">Calendar</button></div>'+data.events.slice(0,3).map(eventRow).join('')+'</section></div><div class="section-title"><h2>Verified Pokémon</h2><button data-go="pokemon">View all</button></div><div class="poke-grid">'+data.pokemon.map(card).join('')+'</div>';else if(tab==='pokemon')C.innerHTML='<h2>My Pokémon</h2><p class="notice">'+data.pokemon.length+' verified detailed records loaded. Family audits remain preserved separately while the full inventory import is built.</p><div class="poke-grid">'+data.pokemon.map(card).join('')+'</div>';else if(tab==='pokedex')C.innerHTML='<h2>Living Pokédex</h2><p class="notice">Master National/Regional Pokédex completion is the next data layer. PMS will separately track caught, currently owned, living-stage coverage, forms, shiny, costume, Shadow/Purified and visually distinct gender variants.</p><section class="metrics">'+metric(data.species,'Species detailed')+metric('—','National completion','master import pending')+metric('—','Kanto 001–151','master import pending')+'</section>';else if(tab==='families')C.innerHTML='<h2>Family audits</h2>'+familyRows()+'<div class="section-title"><h2>Remaining queue</h2></div>'+remainingRows();else if(tab==='cleanup')C.innerHTML='<section class="metrics">'+metric(data.cleanup.total_transferred,'Transferred')+metric(data.storage.capacity-data.storage.used,'Free slots')+metric(data.cleanup.confirmed_families||data.cleanup.families.length,'Families audited')+metric((data.cleanup.remaining_event_families||[]).length,'Families remaining')+'</section><div class="callout"><b>Resume point</b><p>'+E(data.resume?.current||'')+' <strong>Next: '+E(data.cleanup.next_family||'—')+'</strong></p></div><h2>Audited families</h2>'+familyRows()+'<div class="section-title"><h2>Remaining queue</h2></div>'+remainingRows();else if(tab==='resources')C.innerHTML='<h2>Resources</h2><p class="notice">Snapshot amounts update whenever we see or spend them.</p><div class="resource-grid">'+Object.entries(data.resources).map(([k,v])=>metric(typeof v==='number'?v.toLocaleString():v,k.replaceAll('_',' '))).join('')+'</div>';else if(tab==='research')C.innerHTML='<h2>Research planner</h2><div class="callout"><b>Collector-safe research</b><p>'+E((data.research_plan?.rules||[]).join(' · '))+'</p></div>'+(data.research_plan?.active_known_needs||[]).map(x=>'<article class="row"><div><b>'+E(x)+'</b></div></article>').join('');else C.innerHTML='<h2>Events & calendar</h2><p class="notice">Verify event bonuses before acting; use this to plan transfer queues, evolutions, raids and catch targets.</p>'+data.events.map(eventRow).join('');wire()}
function wire(){document.querySelectorAll('[data-go]').forEach(x=>x.onclick=()=>switchTab(x.dataset.go))}
function switchTab(t){tab=t;document.querySelectorAll('nav button').forEach(b=>b.classList.toggle('active',b.dataset.tab===t));render()}
document.querySelectorAll('nav button').forEach(b=>b.onclick=()=>switchTab(b.dataset.tab));(async()=>{try{const r=await fetch('public/data.json?v='+Date.now(),{cache:'no-store'});if(!r.ok)throw Error(r.status);data=await r.json()}catch(e){data=fallback}render()})();