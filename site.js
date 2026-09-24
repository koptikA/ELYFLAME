const levels = [
  {level:1,label:'First steps',ages:'Age 3',program:'Recreational',apparatus:'Rope',title:'A little spark of something big.',text:'An introduction to movement, coordination, and playful exploration with the rope.'},
  {level:2,label:'Find a rhythm',ages:'Ages 4–5',program:'Recreational',apparatus:'Rope, ball',title:'Let curiosity lead.',text:'Playful movement, growing confidence, and a first friendship with the rope and ball.'},
  {level:3,label:'Build a base',ages:'Ages 6–7',program:'Competitive',apparatus:'Rope, ball, hoop',title:'A new chapter begins.',text:'Rope, ball, and hoop come together as athletes begin preparing for competition.'},
  {level:4,label:'Grow stronger',ages:'Ages 6+',program:'Competitive',apparatus:'+ Clubs',title:'Make room for the next challenge.',text:'Clubs join the repertoire, with a continued focus on stretching and apparatus skills.'},
  {level:5,label:'Find expression',ages:'Ages 7+',program:'Competitive',apparatus:'+ Ribbon (all five)',title:'Let expression unfold.',text:'The ribbon completes the apparatus repertoire as skills and flexibility develop.'},
  {level:6,label:'Take the stage',ages:'Ages 8+',program:'Competitive',apparatus:'All apparatus',title:'Bring ambition to the floor.',text:'A pathway toward serious competitive gymnastics, with placement assessed by the coach.'}
];
// Sample schedules only; replace with the academy's approved availability.
const programs = [
  {name:'Recreational',days:['Monday','Wednesday']},
  {name:'Competitive',days:['Tuesday','Thursday']},
  {name:'Stretching & Flexibility',days:['Friday','Saturday']}
];
const age=document.querySelector('#age'),experience=document.querySelector('#experience'),path=document.querySelector('.path');
path.innerHTML='<span class="path-spark" aria-hidden="true">✦</span>'+levels.map(l=>`<div class="level" data-level="${l.level}"><span class="level-number">${l.level}</span><div class="level-description"><p>${l.label}</p><small>${l.ages}</small><small class="apparatus">${l.apparatus}</small></div></div>`).join('')+'<span class="assessment-stop" hidden>Start with a coach assessment</span>';
function positionSpark(){
  const spark=path.querySelector('.path-spark'),target=path.querySelector('.level.active .level-number')||path.querySelector('.assessment-stop:not([hidden])');
  if(!target)return;
  const parent=path.getBoundingClientRect(),rect=target.getBoundingClientRect(),assessment=target.classList.contains('assessment-stop');
  const x=assessment?rect.left-parent.left-28:rect.left-parent.left+rect.width/2-10;
  const y=assessment?rect.top-parent.top+2:rect.top-parent.top-25;
  spark.style.transform=`translate(${x}px,${y}px)`;
}
function updateMatch(){
  const years=Number(age.value),competitive=experience.querySelector('[value="competitive"]');
  competitive.hidden=competitive.disabled=years<6;
  if(years<6&&experience.value==='competitive')experience.value='none';
  const assessment=years>=6||experience.value==='competitive',selected=years===3?levels[0]:levels[1];
  path.classList.toggle('needs-assessment',assessment);
  const stop=path.querySelector('.assessment-stop');stop.hidden=!assessment;
  if(assessment)stop.setAttribute('aria-current','step');else stop.removeAttribute('aria-current');
  path.querySelectorAll('.level').forEach(el=>{
    const active=!assessment&&Number(el.dataset.level)===selected.level;
    el.classList.toggle('active',active);el.classList.toggle('possible',assessment&&Number(el.dataset.level)>=3);
    if(active)el.setAttribute('aria-current','step');else el.removeAttribute('aria-current');
  });
  document.querySelector('#match-label').textContent=assessment?'Starting point / Coach assessment':`Possible starting point / Level ${selected.level}`;
  document.querySelector('#match-title').textContent=assessment?'Every path is individual.':selected.title;
  document.querySelector('#match-copy').textContent=assessment?"Age is only part of the picture. Tell us about your child's experience, and the coach will help find a suitable starting level at the trial.":selected.text;
  document.querySelector('#experience-note').hidden=assessment||experience.value!=='some';
  Object.assign(document.querySelector('#match-cta').dataset,{program:assessment?'Competitive':'Recreational',age:years,experience:experience.value});
  positionSpark();
}
age.addEventListener('change',updateMatch);experience.addEventListener('change',updateMatch);updateMatch();
const menu=document.querySelector('.menu-toggle'),nav=document.querySelector('#navigation');
function closeMenu(){menu.setAttribute('aria-expanded','false');nav.classList.remove('open');}
menu.addEventListener('click',()=>{const open=menu.getAttribute('aria-expanded')!=='true';menu.setAttribute('aria-expanded',String(open));nav.classList.toggle('open',open);});
nav.querySelectorAll('a').forEach(link=>link.addEventListener('click',closeMenu));
document.addEventListener('keydown',event=>{if(event.key==='Escape'&&nav.classList.contains('open')){closeMenu();menu.focus();}});
document.querySelectorAll('a[href^="#"]').forEach(link=>link.addEventListener('click',()=>{const target=document.getElementById(link.hash.slice(1));if(target?.tagName==='DETAILS')target.open=true;}));

// Move the one fallback form into the native dialog; never clone IDs or field values.
const dialog=document.querySelector('#booking-dialog'),form=document.querySelector('#trial-form'),panel=document.querySelector('#booking-panel');
const entry=document.querySelector('#booking-entry'),confirmation=document.querySelector('#booking-confirmation'),submit=document.querySelector('#booking-submit');
const status=document.querySelector('#form-status'),summary=document.querySelector('#error-summary'),program=document.querySelector('#program'),day=document.querySelector('#preferred-day');
const fields=[...form.querySelectorAll('input,select')],hints=new Map(fields.map(field=>[field.id,field.getAttribute('aria-describedby')||'']));
let initialized=false,submitting=false,submissionVersion=0;
form.noValidate=true;
document.querySelector('#dialog-content').append(panel);document.querySelector('#booking-home').hidden=true;
document.querySelector('.enhanced-trial').hidden=false;document.querySelector('#trial').classList.add('enhanced');
function populateDays(){
  const previous=day.value,schedule=programs.find(p=>p.name===program.value);
  day.replaceChildren(new Option('Select a preferred day',''));
  (schedule?.days||[]).forEach(value=>day.add(new Option(`${value} [sample]`,value)));
  if(schedule?.days.includes(previous))day.value=previous;
}
program.addEventListener('change',populateDays);
function openBooking(link){
  if(submitting)cancelSubmission();
  if(!initialized||link.id==='match-cta'){
    const match=document.querySelector('#match-cta').dataset;
    program.value=match.program;document.querySelector('#trial-age').value=match.age;document.querySelector('#trial-experience').value=match.experience;
  }
  if(link.dataset.program)program.value=link.dataset.program;
  if(link.dataset.program==='Stretching & Flexibility'&&!initialized)document.querySelector('#trial-age').value='';
  initialized=true;populateDays();
  if(!submitting){entry.hidden=false;confirmation.hidden=true;dialog.setAttribute('aria-labelledby','booking-title');}
  closeMenu();dialog.showModal();dialog.scrollTop=0;
}
document.querySelectorAll('a[href="#trial"]').forEach(link=>link.addEventListener('click',event=>{event.preventDefault();openBooking(link);}));
document.querySelector('.close-dialog').addEventListener('click',()=>dialog.close());
dialog.addEventListener('close',()=>{if(!dialog.open&&submitting)cancelSubmission();});
dialog.addEventListener('click',event=>{if(event.target!==dialog)return;const r=dialog.getBoundingClientRect();if(event.clientX<r.left||event.clientX>r.right||event.clientY<r.top||event.clientY>r.bottom)dialog.close();});
document.querySelector('#edit-booking').addEventListener('click',()=>{confirmation.hidden=true;entry.hidden=false;dialog.setAttribute('aria-labelledby','booking-title');document.querySelector('#child-name').focus();});
function errorFor(field){
  const value=field.value.trim();
  switch(field.id){
    case 'child-name':return value.length<2||value.length>50?"Enter your child's name using 2 to 50 characters":'';
    case 'trial-age':return !value?"Enter your child's age":!Number.isInteger(Number(value))||Number(value)<3||Number(value)>99?"Enter your child's age as a whole number from 3 to 99":'';
    case 'trial-experience':return !['none','some','competitive'].includes(value)?"Select your child's gymnastics experience":'';
    case 'program':return !programs.some(p=>p.name===value)?'Select a program':'';
    case 'preferred-day':return !programs.find(p=>p.name===program.value)?.days.includes(value)?'Select a preferred day for this program':'';
    case 'parent':return value.length<2||value.length>80?'Enter the parent’s name using 2 to 80 characters':'';
    case 'phone':return value.replace(/\D/g,'').length!==10?'Enter a 10-digit US phone number':'';
    case 'email':return !value||!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(value)?'Enter an email address, like name@example.com':'';
    case 'consent':return !field.checked?'Agree to be contacted about the trial lesson':'';
    default:return '';
  }
}
function setError(field,message){
  const error=document.getElementById(`${field.id}-error`);error.textContent=message;error.hidden=!message;
  field.closest('.field').classList.toggle('has-error',Boolean(message));
  if(message)field.setAttribute('aria-invalid','true');else field.removeAttribute('aria-invalid');
  const describedBy=[hints.get(field.id),message?error.id:''].filter(Boolean).join(' ');
  if(describedBy)field.setAttribute('aria-describedby',describedBy);else field.removeAttribute('aria-describedby');
}
function refreshErrorSummary(){
  const list=summary.querySelector('ul');list.replaceChildren();
  fields.filter(f=>f.getAttribute('aria-invalid')==='true').forEach(field=>{
    const li=document.createElement('li'),link=document.createElement('a');link.href=`#${field.id}`;link.textContent=document.getElementById(`${field.id}-error`).textContent;
    link.addEventListener('click',event=>{event.preventDefault();field.focus();});li.append(link);list.append(li);
  });
  summary.hidden=!list.children.length;submit.classList.toggle('has-error',!summary.hidden);
}
fields.forEach(field=>field.addEventListener('input',()=>{if(field.getAttribute('aria-invalid')==='true'){setError(field,errorFor(field));refreshErrorSummary();}}));
document.querySelector('#phone').addEventListener('input',event=>{
  const input=event.target,old=input.value,caret=input.selectionStart??old.length;
  let digits=old.replace(/\D/g,'');if(digits.length===11&&digits.startsWith('1'))digits=digits.slice(1);
  if(digits.length>10)return; // Preserve invalid overlong input so validation can explain it.
  const digitsBefore=old.slice(0,caret).replace(/\D/g,'').length;
  input.value=digits.length>6?`(${digits.slice(0,3)}) ${digits.slice(3,6)}-${digits.slice(6)}`:digits.length>3?`(${digits.slice(0,3)}) ${digits.slice(3)}`:digits?`(${digits}`:'';
  let position=0,count=0;while(position<input.value.length&&count<digitsBefore){if(/\d/.test(input.value[position]))count++;position++;}input.setSelectionRange(position,position);
});
function bookingRows(){
  return [['Child',form.elements.childName.value],['Age',form.elements.age.value],['Experience',form.elements.experience.selectedOptions[0].text],['Program',program.value],['Preferred day',`${day.value} [sample]`],['Parent',form.elements.parent.value],['Phone',form.elements.phone.value],['Email',form.elements.email.value],['Trial fee','$10, after academy confirmation']];
}
function resetLoading(){
  fields.forEach(field=>field.disabled=false);submitting=false;submit.disabled=false;form.removeAttribute('aria-busy');
  form.querySelector('.submit-label').textContent='Book a Trial';form.querySelector('.spinner').hidden=true;form.querySelector('.submit-arrow').hidden=false;
}
function cancelSubmission(){submissionVersion++;resetLoading();status.textContent='';}
function showConfirmation(rows){
  const list=document.querySelector('#booking-summary');list.replaceChildren();
  rows.forEach(([label,value])=>{const dt=document.createElement('dt'),dd=document.createElement('dd');dt.textContent=label;dd.textContent=value;list.append(dt,dd);});
  entry.hidden=true;confirmation.hidden=false;dialog.setAttribute('aria-labelledby','confirmation-title');dialog.scrollTop=0;if(dialog.open)document.querySelector('#confirmation-title').focus();
}
form.addEventListener('submit',async event=>{
  event.preventDefault();if(submitting)return;
  fields.forEach(field=>setError(field,errorFor(field)));refreshErrorSummary();
  // In the dialog, keep the title in view: scroll to top, then focus the summary without scrolling.
  if(!summary.hidden){status.textContent='Check the highlighted fields.';if(dialog.open){dialog.scrollTop=0;summary.focus({preventScroll:true});}else summary.focus();return;}
  const version=++submissionVersion,rows=bookingRows();
  submitting=true;submit.disabled=true;form.setAttribute('aria-busy','true');
  form.querySelector('.submit-label').textContent='Booking…';form.querySelector('.spinner').hidden=false;form.querySelector('.submit-arrow').hidden=true;status.textContent='Preparing your prototype confirmation…';fields.forEach(field=>field.disabled=true);
  try{
    // Local-only simulation. No network request, storage, email, or payment.
    await new Promise(resolve=>setTimeout(resolve,650));if(version!==submissionVersion)return;showConfirmation(rows);status.textContent='';
  }catch{status.textContent='Something went wrong. Your details are still here. Please try again.';submit.classList.add('has-error');}
  finally{
    if(version===submissionVersion)resetLoading();
  }
});

// Layout-only geometry; CSS drives the draw/rewind. No scroll handler.
const main=document.querySelector('main'),ribbon=document.querySelector('.page-ribbon'),ribbonLine=ribbon.querySelector('path');
const ribbonTiming=document.createElement('style');document.head.append(ribbonTiming);
function layoutRibbon(){
  const width=main.clientWidth,height=main.offsetHeight,mobile=width<=760,mainTop=main.getBoundingClientRect().top;
  const bounds=el=>{const r=el.getBoundingClientRect();return{x:r.left-main.getBoundingClientRect().left,y:r.top-mainTop,w:r.width,h:r.height};};
  const photo=bounds(document.querySelector('.hero-photo')),left=width*(mobile?.025:.035),right=width*(mobile?.975:.965);
  const gradient=ribbon.querySelector('linearGradient');
  Object.entries({gradientUnits:'userSpaceOnUse',x1:photo.x,y1:photo.y,x2:photo.x+photo.w,y2:photo.y+photo.h}).forEach(([key,value])=>gradient.setAttribute(key,value));
  let x=right,y=photo.y+photo.h+25;
  let d=`M ${photo.x+photo.w*.8} ${photo.y-18} C ${photo.x-photo.w*.28} ${photo.y-70} ${photo.x-photo.w*.2} ${photo.y+photo.h*.8} ${photo.x+photo.w*.7} ${photo.y+photo.h*.72} C ${photo.x+photo.w*1.3} ${photo.y+photo.h*.65} ${photo.x+photo.w*.88} ${photo.y+photo.h*.05} ${photo.x+photo.w*.58} ${photo.y+photo.h*.48} C ${photo.x+photo.w*.28} ${photo.y+photo.h} ${right} ${photo.y+photo.h+60} ${x} ${y}`;
  [...main.querySelectorAll(':scope > section')].slice(1).filter(el=>el.getClientRects().length>0).forEach((section,index)=>{
    const box=bounds(section),transitionY=box.y+(mobile?47:65),nextX=section.id==='about'?left:index%2===0?left:right;
    const mid=width*.5,spread=width*(mobile?.23:.27),loop=mobile?32:49;
    // Wide E-like loops live inside reserved whitespace above each section.
    const entryX=x<mid?width*.14:width*.86;
    const approachY=transitionY-loop-12;
    d+=` C ${x} ${y+45} ${x} ${approachY-35} ${x} ${approachY} C ${x} ${transitionY-15} ${entryX} ${transitionY-15} ${entryX} ${transitionY-15}`;
    d+=` C ${mid} ${transitionY-15} ${mid-spread} ${transitionY-loop} ${mid} ${transitionY-loop} C ${mid+spread} ${transitionY-loop} ${mid+spread} ${transitionY+loop} ${mid} ${transitionY+loop} C ${mid-spread} ${transitionY+loop} ${nextX} ${transitionY+20} ${nextX} ${transitionY+65}`;
    x=nextX;y=transitionY+65;
    if(section.id==='about'&&!mobile){
      const art=bounds(section.querySelector('.about-art'));
      d+=` C ${x} ${art.y+50} ${art.x+art.w*.7} ${art.y+art.h*.2} ${art.x+art.w*.45} ${art.y+art.h*.55} C ${art.x+art.w*.15} ${art.y+art.h*.9} ${left} ${art.y+art.h-30} ${left} ${art.y+art.h}`;
      x=left;y=art.y+art.h;
    }
  });
  d+=` C ${x} ${y+40} ${x} ${height-65} ${x} ${height-40} C ${x} ${height-12} ${width*.8} ${height-12} ${width*.65} ${height-12}`;
  ribbon.setAttribute('viewBox',`0 0 ${width} ${height}`);ribbonLine.setAttribute('d',d);
  const length=ribbonLine.getTotalLength(),samples=[];
  // Bound sampling work even as content makes the page longer.
  const sampleStep=Math.max(24,length/160);
  for(let distance=0;distance<=length;distance+=sampleStep)samples.push({distance,y:ribbonLine.getPointAtLength(distance).y});
  const range=document.documentElement.scrollHeight-innerHeight,documentTop=mainTop+scrollY,frames=[];let cursor=0;
  for(let percent=0;percent<=100;percent++){
    const target=percent===0?photo.y+photo.h*.5:range*percent/100+innerHeight*.75-documentTop;
    while(cursor<samples.length-1&&samples[cursor].y<target)cursor++;
    frames.push(`${percent}%{stroke-dashoffset:${percent===100?0:Math.max(0,1000*(1-samples[cursor].distance/length)).toFixed(3)}}`);
  }
  ribbonTiming.textContent=`@keyframes ribbon-unfold{${frames.join('')}}`;positionSpark();
}
let layoutFrame;
function scheduleLayout(){cancelAnimationFrame(layoutFrame);layoutFrame=requestAnimationFrame(layoutRibbon);}
new ResizeObserver(scheduleLayout).observe(main);window.addEventListener('resize',scheduleLayout);document.fonts.ready.then(scheduleLayout);scheduleLayout();
const mobileTrial=document.querySelector('.mobile-trial'),visibleActions=new Set();
const actionObserver=new IntersectionObserver(entries=>{
  entries.forEach(entry=>{if(entry.isIntersecting&&entry.intersectionRatio>=.75)visibleActions.add(entry.target);else visibleActions.delete(entry.target);});
  const hidden=visibleActions.size>0;mobileTrial.classList.toggle('is-muted',hidden);mobileTrial.inert=hidden;mobileTrial.setAttribute('aria-hidden',String(hidden));
},{rootMargin:'-110px 0px -88px 0px',threshold:[0,.75,1]});
document.querySelectorAll('main a.button[href="#trial"]').forEach(el=>actionObserver.observe(el));
