setInterval(function() {
    var date = new Date();

    document.getElementById("date").innerHTML = "Date: "+ date.getDate()+"/"+(date.getMonth()+1)+"/"+date.getFullYear();
    document.getElementById("time").innerHTML = "Time: "+ date.getHours()+":"+date.getMinutes()+":"+date.getSeconds();
},1000);

function page4() {
    document.getElementById("Contact").style.display = "block";
    document.getElementById("education").style.display = "none";
    document.getElementById("experience").style.display = "none";
    document.getElementById("home").style.display = "none";
}

function page3() {
    document.getElementById("experience").style.display = "block";
    document.getElementById("education").style.display = "none";
    document.getElementById("home").style.display = "none";
    document.getElementById("Contact").style.display = "none";
}

function page2() {
    document.getElementById("education").style.display = "block";
    document.getElementById("home").style.display = "none";
    document.getElementById("experience").style.display = "none";
    document.getElementById("Contact").style.display = "none";
}

function page1() {
    document.getElementById("home").style.display = "block";
    document.getElementById("education").style.display = "none";
    document.getElementById("experience").style.display = "none";
    document.getElementById("Contact").style.display = "none";
}