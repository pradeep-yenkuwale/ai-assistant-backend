function toggleChatbot() {
    const chatbotContainer = document.getElementById('chatbot-container');
    const openChatbotBtn = document.getElementById('open-chatbot');
    if (chatbotContainer.style.display === 'none' || chatbotContainer.style.display === '') {
        chatbotContainer.style.display = 'block';
        openChatbotBtn.style.display = 'none';
    } else {
        chatbotContainer.style.display = 'none';
        openChatbotBtn.style.display = 'block';
    }
}

function submitEnter(event) {
    var key = event.code;
    const userInput = $("#user-input").val()
    if(key == "Enter" && userInput) {
        sendMessage();
    }
}

async function sendMessage() {
    const userInput = document.getElementById('user-input');
    const userQuery = userInput.value.trim()
    if (userQuery === '') return;

    // User message
    createMessageElement(userQuery, 'sender');
    
    // Clear input
    document.getElementById('user-input').value = '';

    // Restrict inputs
    restrictInputs()

    const isValidUser = await validateUser(userQuery);
    if(!isValidUser) {
        return isValidUser;
    }
    const userEmail = localStorage.getItem("userEmail");
    let selectedLang = document.getElementById("toggle-label");
    selectedLang = selectedLang.textContent == "English"? 'en': 'ar'
    const selectedContext = $('.header-buttons .selected').val() || 'general';
    const queryPayload = {
        query: userQuery,
        language: selectedLang,
        email: userEmail,
        context: selectedContext,
        sent_at: new Date().toISOString()
    }
    sendUserQuery(queryPayload)

    function restrictInputs(){
        disableInputs(userInput)
    }
}

async function validateUser(userQuery) {
    isValidUser = true
    let userEmail = localStorage.getItem("userEmail");
    if(!userEmail){
        isValidUser = await performUserValidation(userQuery)
    }
    return isValidUser
}

async function validateUserEmail(email) {
    const ticketUrl = `/api/user/validate?email=${email}`
    return await $.ajax({
        method: "GET",
        url: ticketUrl,
        headers: {
            "content-type": "application/json"
        },
        success: function (response) {
            console.log("response", response)
        }, 
        error: function (error) {
            console.log("error", error.responseJSON)
            createMessageElement(error.responseJSON.message, "receiver")
        }
    })
}

async function performUserValidation(userEmail) {
    const validEmail = this.isValidEmail(userEmail);
    if(userEmail && validEmail) {
        if(validEmail) {
            localStorage.setItem("userEmail", userEmail);
            const isValidUser = await validateUserEmail(userEmail).catch(error => error)
            if(!isValidUser || !isValidUser.result || isValidUser.result == null) {
                createMessageElement("Oops! It looks like something went wrong with your credentials. Please enter your valid email and try again? I’m excited to help you once you're in!", 'receiver');
            } else {
                localStorage.setItem("userEmail", userEmail);
                createMessageElement("You're all set! You've been successfully authorized. Feel free to share any questions or concerns you have.", 'receiver');
            }
        } else {
            createMessageElement("Oops! It looks like something went wrong with your credentials. Please enter your valid email and try again? I’m excited to help you once you're in!", 'receiver');
        }
    } else {
        createMessageElement("Oops! It looks like something went wrong with your credentials. Please enter your valid email and try again? I’m excited to help you once you're in!", 'receiver');
    }
    releaseInputs();
    return false;
}


function releaseInputs() {
    const userInput = document.getElementById('user-input');
    enableInputs(userInput)
}

function isValidEmail(email) {
    return String(email)
      .toLowerCase()
      .match(
        /^(([^<>()[\]\\.,;:\s@"]+(\.[^<>()[\]\\.,;:\s@"]+)*)|.(".+"))@((\[[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\.[0-9]{1,3}\])|(([a-zA-Z\-0-9]+\.)+[a-zA-Z]{2,}))$/
      );
};

function disableInputs(userInput) {
    $("#send-btn").prop( "disabled", true );
    $("#start-recording-icon-btn").prop( "disabled", true );
    userInput.readOnly = true;
}

function enableInputs(userInput) {
    $("#send-btn").prop( "disabled", false );
    $("#start-recording-icon-btn").prop( "disabled", false );
    userInput.readOnly = false;
    userInput.focus()
}

function createMessageElement(text, userType) {
    const message = document.createElement('div');
    message.className = `message ${userType}`;

    // Add a user icon
    const userIcon = getUserIcon(userType)

    const messageContent = document.createElement('p');
    messageContent.className = 'message-content';
    messageContent.innerHTML = text;

    if(userType == "receiver") {
        message.appendChild(userIcon)
    }
    message.appendChild(messageContent);
    if(userType == "sender") {
        message.appendChild(userIcon)
    }

    const chatbotMessages = document.getElementById('chatbot-messages');

    chatbotMessages.appendChild(message);
    
    chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    return { messageContent, chatbotMessages }
}

function getUserIcon(userType) {
    const userIcon = document.createElement("div");
    userIcon.classList.add("user-icon");
    const img = document.createElement("img");
    if(userType == "receiver"){
        img.setAttribute("src", "static/media/reciever.png");
        img.alt = "Receiver Icon";
    } else {
        img.setAttribute("src", "static/media/sender.png");
        img.alt = "Sender Icon";
    }
    userIcon.appendChild(img);
    return userIcon
}

function toggleLanguage() {
    const toggleLabel = document.getElementById("toggle-label");
    const chatbotMessages = $('#chatbot-messages .message');
    const userInput = document.getElementById('user-input');
    if(chatbotMessages.length > 1) {
        if(confirm("You are about to loose the conversation, are you sure?")) {
            resetChatBox(toggleLabel)
        }
    } else {
        resetChatBox(toggleLabel)
    }
    enableInputs(userInput)
}
async function resetChatBox(toggleLabel){
    const userInput = document.getElementById("user-input");
    const sendBtn = document.getElementById("send-btn");
    const chatbotMessages = document.getElementById('chatbot-messages');
    const openChatBot = document.getElementById('open-chatbot');

    const titleInput = document.getElementById('titleInput');
    const detailsInput = document.getElementById('detailsInput');
    // const contactInput = document.getElementById('contactInput');

    const titleInputLabel = document.getElementById('titleInputLabel');
    const detailsInputLabel = document.getElementById('detailsInputLabel');
    // const contactInputLabel = document.getElementById('contactInputLabel');

    const headerTitle = document.getElementById('header-title');
    const closeBtn = document.getElementById('close-button');
    const createBtn = document.getElementById('create-button')

    chatbotMessages.innerHTML = ""
    if (toggleLabel.textContent === "English") {
        
        toggleLabel.textContent = "Arabic";
        
        userInput.placeholder = "اكتب رسالتك...";
        
        sendBtn.textContent = "يرسل"
        
        openChatBot.textContent = "مهلا، أنا هنا!🙋‍♂️"

        // Reset background image based on language
        $('body').css('background-image', "url('static/media/background_ar.png')");

        headerTitle.textContent = "إثارة القلق"

        titleInputLabel.textContent = "عنوان:";
        detailsInputLabel.textContent = "تفاصيل:";
        // contactInputLabel.textContent = "هل ترغب في مشاركة تفاصيل الاتصال الخاصة بك (اختياري)؟:";

        titleInput.placeholder = "أدخل العنوان";
        detailsInput.placeholder = "قم بوصف استفسارك"
        // contactInput.placeholder = "البريد الإلكتروني أو رقم الهاتف"

        closeBtn.textContent = "يغلق"
        createBtn.textContent = "يرفع"

        // Set direction to right-to-left for Arabic
        document.body.dir = "rtl";

    } else {

        toggleLabel.textContent = "English";

        userInput.placeholder = "Type your message...";

        sendBtn.textContent = "Send"

        openChatBot.textContent = "Hey, I am here!🙋‍♂️"

        // Reset background image based on language
        $('body').css('background-image', "url('static/media/background_en.png')");

        headerTitle.textContent = "Raise a Concern"

        titleInputLabel.textContent = "Title:"
        detailsInputLabel.textContent = "Details:"
        // contactInputLabel.textContent = "You want to share your contact details (optional)?:"

        titleInput.placeholder = "Enter title";
        detailsInput.placeholder = "Describe your query"
        // contactInput.placeholder = "You want to share your contact details (optional)?:"

        closeBtn.textContent = "Close"
        createBtn.textContent = "Raise"

        // Set direction to left-to-right for English
        document.body.dir = "ltr";
    }
    const userEmail = localStorage.getItem("userEmail")
    const isValidUser = await validateUserEmail(userEmail).catch(error => error)
    let text = toggleLabel.textContent == "Arabic"? "مرحبًا، كيف يمكنني مساعدتك اليوم؟": "Hi!, How i can assist you today?"
    if(!isValidUser || !isValidUser.result || isValidUser.result == null) {
        text = toggleLabel.textContent == "Arabic"? "مرحبًا! يبدو أننا نبدأ جلسة جديدة، أو قد تحتاج إلى السماح بالوصول. يرجى تقديم بريدك الإلكتروني الصحيح للمتابعة، وأنا متحمس لمساعدتك!": "Hey, Welcome! It looks like we're starting a new session, or you might need to authorize access. Please provide your valid email to continue—I’m excited to assist you!"
    }
    createMessageElement(text, 'receiver')
}

function openDialog() {
    document.getElementById("dialogOverlay").style.display = 'flex'
}

function closeDialog() {
    resetInputs()
    document.getElementById("dialogOverlay").style.display = 'none'
}

function onPageLoad() {
    const toggleLabel = document.getElementById("toggle-label");
    const userInput = document.getElementById('user-input');
    toggleLabel.textContent = "English"
    console.log("Loading")
    resetChatBox(toggleLabel)
    enableInputs(userInput)
}

function createTicket(){
    const title = $("#titleInput").val().trim();
    const details =  $("#detailsInput").val().trim();
    const contact = localStorage.getItem('userEmail')
    if(!title || !details){
        document.getElementById("erroreMessage").innerHTML = "Title and Details of ticket are required";
        return;
    }
    const payload = {
        title: title,
        details: details,
        contact: contact
    }
    console.log("Ticket Payload", payload)
    const ticketUrl = "/api/ticket"
    $.ajax({
        method: "POST",
        url: ticketUrl,
        data: JSON.stringify(payload),
        headers: {
            "content-type": "application/json"
        },
        success: function (response) {
            document.getElementById("successMessage").innerHTML = response.message
            setTimeout(
                function() {
                    closeDialog();
            }, 5000);
        }, error: function (error) {
            const errorObj = JSON.parse(error.responseText).detail[0]
            const message = errorObj.msg + " " + errorObj.type + " " + errorObj.loc.join(" -> ")
            document.getElementById("erroreMessage").innerHTML = message  
        }
    })
}

function resetInputs() {
    $("#titleInput").val('')
    $("#detailsInput").val('')
    $("#contactInput").val('')
    document.getElementById("erroreMessage").innerHTML = ""  
    document.getElementById("successMessage").innerHTML = ""
}

function selectButton(button) {
    // Deselect all buttons
    const buttons = document.querySelectorAll('.header-buttons button');
    buttons.forEach(btn => btn.classList.remove('selected'));

    // Select the clicked button
    button.classList.add('selected');
}

function sendUserQuery(payload) {
    const url = '/api/user/stream/text'
    let { messageContent, chatbotMessages } = createMessageElement("...", "receiver")
    const eventSource = new EventSource(`${url}?query=${encodeURIComponent(payload.query)}&email=${payload.email}&language=${payload.language}&sent_at=${payload.sent_at}&context=${payload.context}`)
    eventSource.onmessage = function (event) {
        const elementText = messageContent.innerHTML
        let formattedText = formatText(elementText.replace("...", "") + event.data);
        messageContent.innerHTML = formattedText;
        chatbotMessages.scrollTop = chatbotMessages.scrollHeight;
    };
    eventSource.onerror = function (error) {
        console.log("error", error)
        releaseInputs()
        eventSource.close();
    };
    function formatText(text){
        return text.replace(/\*\*(.*?)\*\*/g, "<b>$1</b>");
    }
}

$(document).ready(function () {

    let audioChunksText = [];
    let mediaRecorderText;
    $("#stop-recording-btn").click(() => {
        mediaRecorderText.stop();
        $("#stop-recording-icon-btn").addClass("hidden");
        $("#start-recording-icon-btn").removeClass("hidden");
        // Send audio to backend
        mediaRecorderText.onstop = async () => {
            const audioBlob = new Blob(audioChunksText, { type: "audio/wav" });
            console.log("audioBlob", audioBlob.type, audioBlob.size)
            const formData = new FormData();
            formData.append("file", audioBlob);
            const response = await fetch("/api/user/text", {
                method: "POST",
                body: formData,
            })
            const responseData = await response.json(); // If your API responds with JSON
            createMessageElement(responseData, "sender")
            const userEmail = localStorage.getItem("userEmail");
            let selectedLang = document.getElementById("toggle-label");
            selectedLang = selectedLang.textContent == "English"? 'en': 'ar'
            const selectedContext = $('.header-buttons .selected').val() || 'general';
            console.log("selectedContext", selectedContext)
            const queryPayload = {
                query: responseData,
                language: selectedLang,
                email: userEmail,
                context: selectedContext,
                sent_at: new Date().toISOString()
            }
            sendUserQuery(queryPayload)
        }
    })

    // Voice mode start recording
    $("#start-recording-btn").click(async () => {
        const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
        mediaRecorderText = new MediaRecorder(stream);

        audioChunksText = [];
        mediaRecorderText.ondataavailable = (event) => {
            audioChunksText.push(event.data);
        };

        $("#mic-animation").removeClass("hidden");
        $("#start-recording-icon-btn").addClass("hidden");
        $("#stop-recording-icon-btn").removeClass("hidden");

        mediaRecorderText.start();
    });
})