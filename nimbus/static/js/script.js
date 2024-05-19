document.getElementById('generateButton').addEventListener('click', generateImage);

function generateImage() {
    const imageUrl = 'https://example.com/api/generate'; // Replace with your actual API endpoint
    const loader = document.getElementById('loader');
    const imageElement = document.getElementById('generatedImage');

    loader.style.display = 'block';
    imageElement.hidden = true;

    fetch(imageUrl)
        .then(response => response.blob())
        .then(blob => {
            loader.style.display = 'none';
            imageElement.src = URL.createObjectURL(blob);
            imageElement.hidden = false;
        })
        .catch(error => {
            console.error('Error generating image:', error);
            loader.style.display = 'none';
            alert('Failed to generate image. Please try again.');
        });
}
