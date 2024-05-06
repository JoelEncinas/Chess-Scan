document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    var formData = new FormData();
    var imageFile = document.getElementById("imageInput").files[0];
    formData.append("image", imageFile);

    console.log("script working");

    fetch("/upload_image/", {
      method: "POST",
      body: formData,
    })
      .then((response) => response.json())
      .then((data) => {
        document.getElementById("result").innerText = data.message;
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

document.getElementById("imageInput").addEventListener("change", function () {
  document.getElementById("file-chosen").textContent = this.files[0].name;
});
