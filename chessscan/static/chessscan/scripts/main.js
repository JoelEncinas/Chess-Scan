var alert = document.getElementById("myAlert");

function showAlert() {
  alert.classList.remove("d-none");
  setTimeout(function () {
    alert.classList.add("d-none");
  }, 3500);
}

document
  .getElementById("uploadForm")
  .addEventListener("submit", function (event) {
    event.preventDefault();
    var formData = new FormData();
    var imageFile = document.getElementById("imageInput").files[0];
    formData.append("image", imageFile);

    const request = new Request(backendUploadImageUrl, {
      headers: { "X-CSRFToken": csrftoken },
    });

    fetch(request, {
      method: "POST",
      body: formData,
      mode: "same-origin",
    })
      .then((response) => {
        console.log(response.status);
        if (response.status === 204) {
          throw new Error("Board not found!");
        }
        return response.json();
      })
      .then((data) => {
        console.log(data);

        document.getElementById("imageContainer").src =
          "data:image/jpg;base64," + data.image;
        document.getElementById("result").value = data.fen;
        document.getElementById("lichess-link").classList.remove("d-none");
        document.getElementById("lichess-link").href = data.lichess;

        document
          .getElementById("copy-to-clipboard")
          .addEventListener("click", function () {
            navigator.clipboard.writeText(data.fen);
            showAlert();
          });
      })
      .catch((error) => {
        console.error("Error:", error);
      });
  });

document.getElementById("imageInput").addEventListener("change", function () {
  document.getElementById("file-chosen").textContent = this.files[0].name;
});
