function myFunction() {
  var loaded = document.getElementById("load_info").text;
  if(loaded = 'False') {
    document.getElementById("alert_text").style.display = "inline-block";
    document.getElementById("loader").style.display = "block";
    document.getElementById("myDiv").style.display = "none";
    myVar = setTimeout(2000);
    myFunction();
  }
  else {
    showPage()
  }

}

function showPage() {
  var table = document.getElementById("table").text;
  document.getElementById("alert_text").style.display = "none";
  document.getElementById("loader").style.display = "none";
  document.getElementById("myDiv").style.display = "block";
  document.getElementById("load_table").innerHTML = table;
}