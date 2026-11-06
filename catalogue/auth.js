// Firebase owner authentication. Set credentials in auth-config.js before enabling.
// No passwords or private keys belong in this public repository.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js';
import { getAuth, onAuthStateChanged, signInWithEmailAndPassword, signOut } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js';
import { getFirestore, doc, getDoc, setDoc } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js';
import { firebaseConfig, ownerUid } from './auth-config.js';
const $=id=>document.getElementById(id);
const configured=Boolean(firebaseConfig?.apiKey&&firebaseConfig?.projectId&&ownerUid);
const login=$('login'),logout=$('logout'),form=$('login-form'),message=$('auth-message');
let user=null,db=null,auth=null;
function state(edit){document.body.classList.toggle('owner-mode',edit);login.hidden=edit;logout.hidden=!edit;$('owner-status').textContent=edit?'Owner · Editing enabled':'Public gallery · View only';window.dispatchEvent(new CustomEvent('catalogue-auth',{detail:{canEdit:edit}}));}
state(false);
if(configured){
 const app=initializeApp(firebaseConfig);auth=getAuth(app);db=getFirestore(app);
 onAuthStateChanged(auth,async account=>{
  user=account?.uid===ownerUid?account:null;
  state(Boolean(user));
  if(user){try{const snap=await getDoc(doc(db,'collections',ownerUid));if(snap.exists())window.dispatchEvent(new CustomEvent('catalogue-cloud-load',{detail:snap.data()}));}catch(e){message.textContent='Cloud collection unavailable: '+e.message;}}
 });
 window.addEventListener('catalogue-cloud-save',async e=>{if(!user)return;try{await setDoc(doc(db,'collections',ownerUid),{collection:e.detail.collection,updatedAt:new Date().toISOString()});message.textContent='Collection synced';}catch(err){message.textContent='Cloud sync failed. Export a backup: '+err.message;}});
}else{login.disabled=true;login.title='Owner login requires Firebase configuration';message.textContent='Owner login setup pending. Gallery remains public and read-only.';}
login.onclick=()=>{$('login-dialog').showModal();};
logout.onclick=async()=>{if(auth)await signOut(auth);};
$('cancel-login').onclick=()=>{$('login-dialog').close();};
form.onsubmit=async e=>{e.preventDefault();if(!auth)return;message.textContent='Signing in…';try{const result=await signInWithEmailAndPassword(auth,$('email').value,$('password').value);if(result.user.uid!==ownerUid){await signOut(auth);throw Error('This account is not authorized to edit.');}$('login-dialog').close();$('password').value='';message.textContent='';}catch(err){message.textContent=err.message;}};
