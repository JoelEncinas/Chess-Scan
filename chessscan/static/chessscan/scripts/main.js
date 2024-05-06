document.addEventListener("DOMContentLoaded", function () {
  var alertSuccess = document.getElementById("success-alert");
  var alertDanger = document.getElementById("danger-alert");

  function showAlert(alert) {
    alert.classList.remove("d-none");
    setTimeout(function () {
      alert.classList.add("d-none");
    }, 2500);
  }

  const formClassic = document.getElementById("wood");
  const formWood = document.getElementById("classic");
  const woodLabel = document.getElementById("wood-label");
  const classicLabel = document.getElementById("classic-label");

  formWood.addEventListener("change", function () {
    if (this.checked) {
      woodLabel.style.backgroundColor = "red";
    } else {
      woodLabel.style.backgroundColor = "";
    }
  });

  formClassic.addEventListener("change", function () {
    if (this.checked) {
      classicLabel.style.backgroundColor = "red";
    } else {
      classicLabel.style.backgroundColor = "";
    }
  });

  clipboard = document.getElementById("copy-to-clipboard");
  scanData = document.getElementById("scan");

  document
    .getElementById("uploadForm")
    .addEventListener("submit", function (event) {
      event.preventDefault();
      var formData = new FormData();
      var imageFile = document.getElementById("imageInput").files[0];
      formData.append("image", imageFile);

      var selectedRadioButton = document.querySelector(
        'input[name="piece"]:checked'
      );

      formData.append("piece_material", selectedRadioButton.id);

      const request = new Request(backendUploadImageUrl, {
        headers: { "X-CSRFToken": csrftoken },
      });

      fetch(request, {
        method: "POST",
        body: formData,
        mode: "same-origin",
      })
        .then((response) => {
          if (response.status === 418) {
            throw new Error("board not detected");
          } else if (response.status === 400) {
            throw new Error("no image uploaded");
          }
          return response.json();
        })
        .then((data) => {
          document.getElementById("imageContainer").src =
            "data:image/jpg;base64," + data.image;
          document.getElementById("result").value = data.fen;
          scanData.classList.remove("d-none");
          document.getElementById("lichess-link").href = data.lichess;

          clipboard.addEventListener("click", function () {
            navigator.clipboard.writeText(data.fen);
            showAlert(alertSuccess);
          });
        })
        .catch((error) => {
          if (error.message === "board not detected") {
            alertDanger.innerText = "Chessboard not found in the image!";
            showAlert(alertDanger);
          }

          if (error.message === "no image uploaded") {
            alertDanger.innerText = "Need to upload an image first!";
            showAlert(alertDanger);
          }
        });
    });

  document.getElementById("imageInput").addEventListener("change", function () {
    document.getElementById("file-chosen").textContent = this.files[0].name;
  });
});
