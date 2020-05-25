window.addEventListener("load", function() {
  document.getElementById("file-upload").onchange = function(event) {
    var reader = new FileReader();
    reader.readAsDataURL(event.srcElement.files[0]);
    var me = this;
    debugger
    var fileContent
    reader.onload = function () {
      fileContent = reader.result;
    localStorage.setItem("imgcontent", fileContent);
    console.log(fileContent);
    }
}});