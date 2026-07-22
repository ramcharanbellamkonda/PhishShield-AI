let lastResult = null;
let lastUrl = "";
window.onload = function () {

    document.getElementById("checkBtn").addEventListener("click", checkURL);

    document.getElementById("themeBtn").addEventListener("click", toggleTheme);

    loadTheme();

    loadHistory();

};

async function checkURL() {

    const url = document.getElementById("url").value.trim();
    lastUrl = url;

    if(url===""){
        alert("Enter a URL");
        return;
    }

    document.getElementById("loading").style.display="block";
    document.getElementById("resultCard").style.display="none";

    try{

        const response=await fetch("/predict",{

            method:"POST",

            headers:{
                "Content-Type":"application/json"
            },

            body:JSON.stringify({
                url:url
            })

        });

        const data=await response.json();

        document.getElementById("loading").style.display="none";

        showResult(data);

        saveHistory(url,data.prediction);

    }

    catch(err){

        document.getElementById("loading").style.display="none";

        alert("Server Error");

        console.log(err);

    }

}

function showResult(data){
    lastResult = data;

    const card=document.getElementById("resultCard");

    const prediction=document.getElementById("prediction");

    const confidence=document.getElementById("confidence");

    const risk=document.getElementById("risk");

    const progress=document.getElementById("progressBar");

    const icon=document.getElementById("icon");

    const analysis=document.getElementById("analysisList");

    card.style.display="block";

    prediction.innerHTML=data.prediction;

    const circularProgress=document.querySelector(".circular-progress");

const progressValue=document.getElementById("scoreValue");

let startValue=0;

let endValue=Math.round(data.confidence);

let speed=15;

let animation=setInterval(()=>{

startValue++;

progressValue.innerHTML=startValue+"%";

circularProgress.style.background=

`conic-gradient(#22c55e ${startValue*3.6}deg,#1e293b 0deg)`;

if(startValue>=endValue){

clearInterval(animation);

}

},speed);

    confidence.innerHTML="Confidence : "+data.confidence+"%";

    risk.innerHTML="Risk : "+data.risk;

    progress.style.width=data.confidence+"%";

    analysis.innerHTML="";
    document.getElementById("urlInfoCard").style.display="block";

document.getElementById("protocol").innerHTML=data.url_info.protocol;

document.getElementById("domain").innerHTML=data.url_info.domain;

document.getElementById("subdomain").innerHTML=data.url_info.subdomain;

document.getElementById("length").innerHTML=data.url_info.length;

    data.analysis.forEach(item=>{

        const li=document.createElement("li");

        li.innerHTML="✔ "+item;

        analysis.appendChild(li);

    });

    if(data.prediction==="Legitimate"){

        icon.innerHTML="🛡️";

        progress.style.background="#16A34A";

        prediction.style.color="#16A34A";

    }

    else{

        icon.innerHTML="🚨";

        progress.style.background="#DC2626";

        prediction.style.color="#DC2626";

    }

}

function saveHistory(url,result){

    let history=JSON.parse(localStorage.getItem("history")) || [];

    history.unshift({
        url:url,
        result:result
    });

    history=history.slice(0,5);

    localStorage.setItem("history",JSON.stringify(history));

    loadHistory();

}

function loadHistory(){

    const list=document.getElementById("historyList");

    list.innerHTML="";

    const history=JSON.parse(localStorage.getItem("history")) || [];

    history.forEach(item=>{

        const li=document.createElement("li");

        li.innerHTML=item.result==="Legitimate"

        ? "🟢 "+item.url

        : "🔴 "+item.url;

        list.appendChild(li);

    });

}

function toggleTheme(){

    document.body.classList.toggle("dark");

    localStorage.setItem(

        "theme",

        document.body.classList.contains("dark")

    );

}

function loadTheme(){

    if(localStorage.getItem("theme")==="true"){

        document.body.classList.add("dark");

    }

}
function downloadReport(){

if(lastResult==null){

alert("Scan a website first.");

return;

}

const report=`

AI PHISHING DETECTOR
=============================

URL : ${lastUrl}

Prediction : ${lastResult.prediction}

Confidence : ${lastResult.confidence}%

Risk : ${lastResult.risk}

Protocol : ${lastResult.url_info.protocol}

Domain : ${lastResult.url_info.domain}

Subdomain : ${lastResult.url_info.subdomain}

URL Length : ${lastResult.url_info.length}

Security Analysis

${lastResult.analysis.join("\n")}

`;

const blob=new Blob([report],{type:"text/plain"});

const a=document.createElement("a");

a.href=URL.createObjectURL(blob);

a.download="Security_Report.txt";

a.click();

}