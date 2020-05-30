$(function(){
    document.getElementById("inputClauses").value = "aaa\nbbb\nccc";
    document.getElementById("submitClauses").onclick = resolutionStart;
});


function resolutionStart(){
    var inputClauses = document.getElementById("inputClauses");
    var rawClauses = inputClauses.value;
    var clausesArray = rawClauses.split("\n");

    console.log(clausesArray);
}