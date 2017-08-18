// console.log("AM i WORKING?");

// document.ready = function(){
//      var canvas = document.getElementById("#myCanvas");
//      var context = canvas.getContext("2d");
//      // var img = document.getElementById("#photo");
//      // var text = document.getElementById("#text")

//      var imageObj = new Image();
//      imageObj.onload = function(){
//          context.drawImage(imageObj, 10, 10);
//          context.font = "40pt Calibri";
//          context.fillText('#text');
//      };
//      imageObj.src = $('#photo'); 
// };
window.onload = function(){
     var canvas = document.getElementById("myCanvas");
     var context = canvas.getContext("2d");
     var imageObj = new Image();
     imageObj.onload = function(){
         context.drawImage(imageObj, 10, 10);
         context.fillStyle = "#FF0000"
         context.fillRect(10,623,768,60)
         context.font = "18pt Calibri";
         text = document.getElementById("text").innerHTML;
         context.fillText(text, 5, 600);
     };
    imageObj.src = document.getElementById('photo').getAttribute("src"); 
};