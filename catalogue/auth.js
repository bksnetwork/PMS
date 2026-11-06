// GitHub OAuth via Firebase Authentication. No passwords or OAuth secrets in this public repository.
import { initializeApp } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-app.js';
import { getAuth, GithubAuthProvider, signInWithPopup, signInWithRedirect, getRedirectResult, onAuthStateChanged, signOut } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-auth.js';
import { getFirestore, doc, getDoc, setDoc } from 'https://www.gstatic.com/firebasejs/11.10.0/firebase-firestore.js';
import { firebaseConfig, ownerUid } from './auth-config.js';
const $=id=>document.getElementById(id);
const configured=Boolean(firebaseConfig?.apiKey&&firebaseConfig?.projectId&&firebaseConfig?.authDomain&&ownerUid);
const login=$('login'),logout=$('logout'),message=$('auth-message');
let user=null,db=null,auth=null;
function status(s){message.textContent=s;}
function state(edit){document.body.classList.toggle('owner-mode',edit);login.hidden=edit;logout.hidden=!edit;$('owner-status').textContent=edit?'Owner · Editing enabled':'Public gallery · View only';window.dispatchEvent(new CustomEvent('catalogue-auth',{detail:{canEdit:edit}}));}
state(false);
if(configured){
 const app=initializeApp(firebaseConfig);auth=getAuth(app);db=getFirestore(app);
 const provider=new GithubAuthProvider();provider.setCustomParameters({allow_signup:'false'});
 getRedirectResult(auth).catch(e=>status('GitHub sign-in: '+e.message));
 onAuthStateChanged(auth,async account=>{
  user=account?.uid===ownerUid&&account.providerData.some(p=>p.providerId==='github.com')?account:null;
  state(Boolean(user));
  if(account&&!user){status('This GitHub account is not the authorized owner.');await signOut(auth);return;}
  if(user){status('Signed in with GitHub.');try{const snap=await getDoc(doc(db,'collections',ownerUid));if(snap.exists())window.dispatchEvent(new CustomEvent('catalogue-cloud-load',{detail:snap.data()}));}catch(e){status('Cloud collection unavailable: '+e.message);}}
 });
 window.addEventListener('catalogue-cloud-save',async e=>{if(!user)return;try{await setDoc(doc(db,'collections',ownerUid),{collection:e.detail.collection,updatedAt:new Date().toISOString()});status('Collection synced to your account.');}catch(err){status('Cloud sync failed. Export a backup: '+err.message);}});
 login.onclick=async()=>{status('Connecting to GitHub…');try{const result=await signInWithPopup(auth,provider);if(result.user.uid!==ownerUid){await signOut(auth);status('This GitHub account is not authorized.');}}catch(e){if(['auth/popup-blocked','auth/operation-not-supported-in-this-environment'].includes(e.code)){await signInWithRedirect(auth,provider);}else{status('GitHub login failed: '+e.message);}}};
 logout.onclick=async()=>{await signOut(auth);status('Signed out.');};
}else{
 login.disabled=true;login.title='GitHub owner login requires Firebase configuration';
 status('Owner sign-in is being configured. The public gallery is available in read-only mode.');
}
