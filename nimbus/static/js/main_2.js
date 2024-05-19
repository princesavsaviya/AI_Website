// Function To Disable The Generate Button During Processing
function disableGenerateButton() {
    document.getElementById("generate").disabled = true;
    document.getElementById("show-previous").disabled = true;
}

// Function To Anable The Generate Button After Process
function enableGenerateButton() {
    document.getElementById("generate").disabled = false;
    document.getElementById("show-previous").disabled = false;
}

// Function To Clear Image Grid
function clearImageGrid() {
    const imageGrid = document.getElementById("image-grid");
    imageGrid.innerHTML = "";
}

// Function To Generate Images (with local tensor data)
/*async function generateImages() {
    disableGenerateButton();
    clearImageGrid();

    const loading = document.getElementById("loading");
    loading.style.display = "block";

    // Fetch tensor data from local file
    const tensorDataResponse = await fetch("/generate-image/");
    const tensorData = await tensorDataResponse.json();
    console.log(tensorDataResponse);
    // Process tensor data to generate images
    const maxImage = 1;
    const imageUrls = [];

    for (let i = 0; i < maxImage && i < tensorData.length; i++) {
        // Process tensor data and generate image URLs
        const imageArray = tensorData[i]; // Assuming tensorData is a 3D array (height x width x 3)
        const imgUrl = arrayToDataURL(imageArray);
        imageUrls.push(imgUrl);

        const img = document.createElement("img");
        img.src = imgUrl;
        img.alt = `art-${i + 1}`;
        img.onclick = () => downloadImage(imgUrl, i);
        document.getElementById("image-grid").appendChild(img);
    }

    loading.style.display = "none";
    enableGenerateButton();
}*/

async function generateImages() {
    disableGenerateButton();
    clearImageGrid();

    const loading = document.getElementById("loading");
    loading.style.display = "block";

    const imageType = document.getElementById("image-type").value;

    const response = await fetch(`/generate-image/${imageType}`); // Adjust the endpoint URL accordingly
    const imageBinaryData = await response.blob(); // Get the binary data
    console.log(imageBinaryData);
    console.log(response);
    // Convert binary data to an image URL
    const imgUrl = URL.createObjectURL(imageBinaryData);
    
    // Create an image element and display the image on the webpage
    const img = document.createElement("img");
    img.src = imgUrl;
    img.alt = "Generated Image";
    img.style.width = "350px"; // Adjust the width as needed
    img.style.height = "350px";
    document.getElementById("image-grid").appendChild(img);
    document.getElementById("image-grid").style.display = "block";
    console.log("Img added to image grid")
    loading.style.display = "none";
    enableGenerateButton();
}

// Function To Download Images
function downloadImage(imgUrl, imageNumber) {
    const link = document.createElement("a");
    link.href = imgUrl;
    link.download = `image-${imageNumber + 1}.jpg`;
    link.click();
}

// Remove Loading Page After Document Loaded
document.addEventListener("DOMContentLoaded", () => {
    document.getElementById("splash").classList.add("loaded");
});
