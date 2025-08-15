const taskInput=document.getElementById("taskInput");
const addBtn=document.getElementById("addBtn");
const voiceBtn=document.getElementById("voiceBtn");
const taskList=document.getElementById("taskList");

let tasks=JSON.parse(localStorage.getItem("tasks")||"[]");
render();

addBtn.addEventListener("click",()=>{ add(taskInput.value); taskInput.value=""; });
taskInput.addEventListener("keydown",(e)=>{ if(e.key==="Enter"){ add(taskInput.value); taskInput.value=""; }});

function add(text){
  text=(text||"").trim();
  if(!text) return;
  tasks.push({text,done:false});
  save();
}

function toggle(i){ tasks[i].done=!tasks[i].done; save(); }
function delTask(i){ tasks.splice(i,1); save(); }

function render(){
  taskList.innerHTML="";
  tasks.forEach((t,i)=>{
    const li=document.createElement("li");
    if(t.done) li.classList.add("done");
    const label=document.createElement("span");
    label.textContent=t.text;
    label.addEventListener("click",()=>toggle(i));
    const actions=document.createElement("div");
    actions.className="actions";
    const doneBtn=document.createElement("button"); doneBtn.textContent="✔"; doneBtn.onclick=()=>toggle(i);
    const delBtn=document.createElement("button"); delBtn.textContent="❌"; delBtn.onclick=()=>delTask(i);
    actions.append(doneBtn,delBtn);
    li.append(label,actions);
    taskList.append(li);
  });
}

function save(){ localStorage.setItem("tasks",JSON.stringify(tasks)); render(); }

// Voice (Web Speech API)
voiceBtn.addEventListener("click",()=>{
  const SR=window.SpeechRecognition||window.webkitSpeechRecognition;
  if(!SR){ alert("SpeechRecognition not supported in this browser. Try Chrome."); return; }
  const rec=new SR();
  rec.lang="en-US";
  rec.interimResults=false;
  rec.onresult=(e)=>{
    const speech=e.results[0][0].transcript.toLowerCase();
    if(speech.startsWith("add task")) add(speech.replace("add task","").trim());
    else add(speech);
  };
  rec.start();
});
