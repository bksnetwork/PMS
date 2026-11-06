#!/usr/bin/env node
// Catch missing DOM references that previously left the catalogue blank.
const fs=require('node:fs');
const html=fs.readFileSync('catalogue/index.html','utf8');
const app=fs.readFileSync('catalogue/app.js','utf8');
const auth=fs.readFileSync('catalogue/auth.js','utf8');
const ids=new Set([...html.matchAll(/\bid="([^"]+)"/g)].map(m=>m[1]));
let missing=0;
for(const [source,code] of [['app.js',app],['auth.js',auth]]){
  for(const match of code.matchAll(/\$\('([^']+)'\)/g)){
    if(!ids.has(match[1])){console.error(source+': missing HTML element #'+match[1]);missing++;}
  }
}
if(missing)process.exit(1);
console.log('All referenced HTML IDs exist ('+ids.size+' total).');
