document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    var formData = new FormData();
    var imageFile = document.getElementById("imageInput").files[0];
    formData.append("image", imageFile);

    console.log("script working");

    const request = new Request(backendUploadImageUrl, {
      headers: { "X-CSRFToken": csrftoken },
    });

    fetch(request, {
      method: "POST",
      body: formData,
      mode: "same-origin",
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
