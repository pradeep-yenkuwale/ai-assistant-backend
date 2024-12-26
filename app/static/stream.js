$(document).ready(function () {
    let mediaRecorder;
    let audioChunks = [];

    // Mode switcher
    $("#text-mode").click(() => {
        $(".mode").addClass("hidden");
        $("#text-input").removeClass("hidden");
        $("#text-mode").addClass("active");
        $("#voice-mode").removeClass("active");
    });

    // voice mode
    $("#voice-mode").click(() => {
        $(".mode").addClass("hidden");
        $("#voice-input").removeClass("hidden");
        $("#voice-mode").addClass("active");
        $("#text-mode").removeClass("active");
    });

    // Text mode send
    $("#send-text").click(() => {
        const userText = $("#user-text").val();
        if (userText.trim() !== "") {
            appendMessage("user-message", userText);
            // Send text to backend
            $.ajax({
                url: "/api/user/stream/voice",
                method: "GET",
                data: { query: userText },
                success: (response) => {
                    appendMessage("ai-message", response.text);
                },
                error: (err) => console.error(err),
            });
            $("#user-text").val("");
        }
    });

    // Voice mode start recording
    $("#start-recording").click(async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorder = new MediaRecorder(stream);

        audioChunks = [];
        mediaRecorder.ondataavailable = (event) => {
            audioChunks.push(event.data);
        };

        $("#mic-animation").removeClass("hidden");
        $("#start-recording-icon").addClass("hidden");
        $("#stop-recording-icon").removeClass("hidden");

        mediaRecorder.start();
    });




    // Voice mode stop recording
    $("#stop-recording").click(() => {
        mediaRecorder.stop();

        $("#mic-animation").addClass("hidden");
        $("#stop-recording-icon").addClass("hidden");
        $("#audio-processing").removeClass("hidden");
        $("#start-recording-icon").removeClass("hidden");

        mediaRecorder.onstop = () => {
            const audioBlob = new Blob(audioChunks, { type: "audio/wav" });
            const formData = new FormData();
            formData.append("file", audioBlob);

            const userEmail = localStorage.getItem("userEmail");
            let selectedLang = document.getElementById("toggle-label");
            selectedLang = selectedLang.textContent == "English"? 'en': 'ar'
            const selectedContext = $('.header-buttons .selected').val() || 'general';
            console.log("selectedContext", selectedContext)
            const sent_at = new Date().toISOString()

            const url = `/api/user/stream/voice?email=${userEmail}&language=${selectedLang}&context=${selectedContext}&sent_at=${sent_at}`;
            // Send audio to backend
            $.ajax({
                url: url,
                method: "POST",
                data: formData,
                processData: false,
                contentType: false,
                xhrFields: {
                    responseType: 'blob'
                },
                success: function(data) {
                    console.log("data", data)
                    console.log('Blob:', data);
                    console.log('Blob type:', data.type);
                    console.log('Blob size:', data.size);

                    const audioBlob = new Blob([data], { type: 'audio/wav' });
                    const audioUrl = URL.createObjectURL(audioBlob);
                    const audioElement = new Audio(audioUrl);
                    const audioPlayer = document.getElementById("audio-player");
                    audioPlayer.src = audioUrl
                    audioPlayer.play()
                    $("#playing-audio").removeClass("hidden");
                    $("#start-recording-icon").addClass("hidden");
                    $("#pause-button").removeClass("hidden")
                    $("#stop-button").removeClass("hidden")
                },
                error: (err) => console.error(err),
            });
        };
    });


    // Helper: Append messages to chat history
    function appendMessage(className, text) {
        $("#chat-history").append(
            `<div class="message ${className}">${text}</div>`
        );
        $("#chat-window").scrollTop($("#chat-window")[0].scrollHeight);
    }
});


function pauseAudio() {
    console.log("I am here")
    $("#playing-audio").addClass('hidden')
    $("#pause-audio").removeClass('hidden')
    $("#play-button").removeClass('hidden')
    $("#pause-button").addClass('hidden')
    $("#stop-button").addClass('hidden')


}
function playAudio() {
    $("#playing-audio").removeClass('hidden')
    $("#pause-audio").addClass('hidden')
    $("#play-button").addClass('hidden')
    $("#pause-button").removeClass('hidden')
    $("#stop-button").removeClass('hidden')
}
function reInitializeControls() {
    $("#play-button").addClass('hidden')
    $("#pause-button").addClass('hidden')
    $("#start-recording-icon").removeClass("hidden");
    $("#playing-audio").addClass("hidden");
    $("#stop-button").addClass('hidden')

}

document.addEventListener("DOMContentLoaded", () => {
    const audioPlayer = document.getElementById("audio-player");
    const playButton = document.getElementById("play-button");
    const pauseButton = document.getElementById("pause-button");
    const stopButton = document.getElementById("stop-button");
    const statusMessage = document.getElementById("status-message");

    // Play button event listener
    playButton.addEventListener("click", () => {
        audioPlayer.play();
        playButton.disabled = true;
        pauseButton.disabled = false;
        // statusMessage.textContent = "Audio is playing...";
        playAudio()
    });

    // Play button event listener
    stopButton.addEventListener("click", () => {
        audioPlayer.pause()
        reInitializeControls()
    });

    // Pause button event listener
    pauseButton.addEventListener("click", () => {
        audioPlayer.pause();
        playButton.disabled = false;
        pauseButton.disabled = true;
        // statusMessage.textContent = "Audio is paused.";
        pauseAudio()
    });

    // Event listener for audio end
    audioPlayer.addEventListener("ended", () => {
        playButton.disabled = false;
        pauseButton.disabled = true;
        // statusMessage.textContent = "Audio finished playing.";
        reInitializeControls()
        // Perform additional actions after audio ends
        console.log("Audio has finished playing. Performing additional actions...");
        // Add your custom actions here
    });

    // Optional: Handle error events
    audioPlayer.addEventListener("error", (e) => {
        statusMessage.textContent = "Error loading or playing the audio.";
        console.error("Audio error:", e);
    });
});

