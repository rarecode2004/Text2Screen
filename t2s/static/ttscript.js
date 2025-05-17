document.getElementById('promptForm').addEventListener('submit', async function (e) {
    e.preventDefault();
    
    const prompt = document.getElementById('prompt').value;
    const loadingDiv = document.getElementById('loading');
    const videoContainer = document.getElementById('videoContainer');
    const generatedVideo = document.getElementById('generatedVideo');
    const downloadLink = document.getElementById('downloadLink');

    loadingDiv.style.display = 'block';
    videoContainer.style.display = 'none';

    try {
        const response = await fetch('/generate-video', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ prompt }),
        });

        if (!response.ok) {
            throw new Error('Network response was not ok');
        }

        const result = await response.json();

        loadingDiv.style.display = 'none';
        videoContainer.style.display = 'block';
        generatedVideo.src = result.video_url;
        downloadLink.href = result.video_url;
    } catch (error) {
        console.error('Error:', error);
        loadingDiv.style.display = 'none';
        videoContainer.style.display = 'block';
        generatedVideo.innerText = 'Failed to load video.';
    }
});