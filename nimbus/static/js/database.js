// Function To Clear Image Grid
function clearImageGrid() {
    const imageGrid = document.getElementById("image-grid");
    imageGrid.innerHTML = "";
}
async function DisplayImages() {
    clearImageGrid();

    const loading = document.getElementById("loading");
    loading.style.display = "block";

    // Fetch image data from backend endpoint
    const response = await fetch("/display-image/"); // Adjust the endpoint URL accordingly
    const imageData = await response.json(); // Get the JSON data containing images
    // Check if images are present in the response
    if (imageData && imageData.images && imageData.images.length > 0) {
        // Loop through each image data
        const images = JSON.parse(imageData.images); // Assuming imageData is your JSON data object
        for (let i = 0; i < images.length; i++) {
            const image = images[i];
            const binaryString = atob(image)

            const uint8Array = new Uint8Array(binaryString.length);
            for (let i = 0; i < binaryString.length; i++) {
                uint8Array[i] = binaryString.charCodeAt(i);
            }
            //console.log(binaryString);
            const blob = new Blob([uint8Array], { type: "image/jpeg" })
            const imgURL = URL.createObjectURL(blob)

            // Create an image element and display the image on the webpage
            const img = document.createElement("img");
            img.src = imgURL;
            img.alt = "Previous Image"; // Use filename if available, else use a default alt text
            img.style.width = "250px"; // Adjust the width as needed
            img.style.height = "250px";
            img.style.padding = "5px";

            document.getElementById("image-grid").appendChild(img);
        }

        // Show the image grid
        document.getElementById("image-grid").style.display = "grid";
        console.log("Images added to image grid");
    } else {
        console.log("No images found in the response");
    }

    // Hide loading indicator and enable generate button
    loading.style.display = "none";
}

document.addEventListener('DOMContentLoaded', function () {
    DisplayImages();
    document.getElementById("splash").classList.add("loaded");
})
