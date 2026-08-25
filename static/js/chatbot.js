/* KisanMitra AI Chatbot JavaScript Logic */

// Predefined Quick Actions by Language
const QUICK_ACTIONS = {
    en: [
        { label: "🌱 Check My Soil", query: "Can you analyze my soil metrics?" },
        { label: "💧 Irrigation", query: "Should I irrigate my crops today?" },
        { label: "🌿 Crop Health", query: "What is the health status of my crop?" },
        { label: "☀️ Farm Conditions", query: "Can you summarize my farm's current temperature and weather conditions?" },
        { label: "📋 Today's Plan", query: "Explain the current farm planning summary plan." },
        { label: "📊 Explain Recommendations", query: "Can you explain my active recommendations?" }
    ],
    te: [
        { label: "🌱 నా నేల ఆరోగ్యం", query: "నా మట్టి కొలతలను విశ్లేషించగలరా?" },
        { label: "💧 నీరు పెట్టాలా?", query: "నేను ఈ రోజు పంటకు నీరు పెట్టాలా?" },
        { label: "🌿 పంట ఆరోగ్యం", query: "నా పంట ఆరోగ్య పరిస్థితి ఏమిటి?" },
        { label: "☀️ వ్యవసాయ వాతావరణం", query: "నా పొలం యొక్క ప్రస్తుత ఉష్ణోగ్రత మరియు వాతావరణ పరిస్థితుల సారాంశం ఏమిటి?" },
        { label: "📋 నేటి ప్రణాళిక", query: "ప్రస్తుత వ్యవసాయ ప్రణాళికను వివరించండి." },
        { label: "📊 సిఫార్సుల వివరణ", query: "నా క్రియాశీల సిఫార్సులను వివరించగలరా?" }
    ],
    hi: [
        { label: "🌱 मिट्टी की जांच", query: "क्या आप मेरी मिट्टी के स्वास्थ्य का विश्लेषण कर सकते हैं?" },
        { label: "💧 क्या सिंचाई करें?", query: "क्या मुझे आज फसलों की सिंचाई करनी चाहिए?" },
        { label: "🌿 फसल का स्वास्थ्य", query: "मेरी फसल के स्वास्थ्य की क्या स्थिति है?" },
        { label: "☀️ मौसम की स्थिति", query: "मेरे खेत के वर्तमान तापमान और मौसम का सारांश बताएं।" },
        { label: "🧠 आज की योजना", query: "वर्तमान कृषि योजना सारांश स्पष्ट करें।" },
        { label: "📊 सिफारिशें समझाएं", query: "क्या आप मेरी सक्रिय सिफारिशों को समझा सकते हैं?" }
    ],
    ta: [
        { label: "🌱 என் மண் பரிசோதனை", query: "என் மண்ணின் அளவீடுகளை பகுப்பாய்வு செய்ய முடியுமா?" },
        { label: "💧 நீர் பாய்ச்ச வேண்டுமா?", query: "நான் இன்று பயிருக்கு நீர் பாய்ச்ச வேண்டுமா?" },
        { label: "🌿 பயிர் ஆரோக்கியம்", query: "என் பயிரின் ஆரோக்கிய நிலை என்ன?" },
        { label: "☀️ பண்ணை வானிலை", query: "என் பண்ணையின் தற்போதைய வெப்பநிலை மற்றும் வானிலை சுருக்கத்தை கூறுங்கள்." },
        { label: "📋 இன்றைய திட்டம்", query: "தற்போதைய பண்ணை திட்டமிடல் சுருக்கத்தை விளக்குங்கள்." },
        { label: "📊 பரிந்துரைகளின் விளக்கம்", query: "என் செயலில் உள்ள பரிந்துரைகளை விளக்க முடியுமா?" }
    ],
    kn: [
        { label: "🌱 ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ", query: "ನನ್ನ ಮಣ್ಣಿನ ಅಳತೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಬಹುದೇ?" },
        { label: "💧 ನೀರುಣಿಸಬೇಕೇ?", query: "ನಾನು ಇಂದು ಬೆಳೆಗೆ ನೀರುಣಿಸಬೇಕೇ?" },
        { label: "🌿 ಬೆಳೆ ಆರೋಗ್ಯ", query: "ನನ್ನ ಬೆಳೆಯ ಆರೋಗ್ಯ ಸ್ಥಿತಿ ಹೇಗಿದೆ?" },
        { label: "☀️ ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿ", query: "ನನ್ನ ತೋಟದ ಪ್ರಸ್ತುತ ತಾಪಮಾನ ಮತ್ತು ಹವಾಮಾನದ ಸಾರಾಂಶವೇನು?" },
        { label: "📋 ಇಂದಿನ ಕೃಷಿ ಯೋಜನೆ", query: "ಪ್ರಸ್ತುತ ಕೃಷಿ ಯೋಜನೆ ಸಾರಾಂಶವನ್ನು ವಿವರಿಸಿ." },
        { label: "📊 ಶಿಫಾರಸುಗಳನ್ನು ವಿವರಿಸಿ", query: "ನನ್ನ ಸಕ್ರಿಯ ಶಿಫಾರಸುಗಳನ್ನು ವಿವರಿಸಬಹುದೇ?" }
    ],
    ja: [
        { label: "🌱 土壌チェック", query: "私の土壌の状態を分析してもらえますか？" },
        { label: "💧 水やりは必要？", query: "今日、作物に灌漑する必要がありますか？" },
        { label: "🌿 作物の健康状態", query: "私の作物の健康状態はどうですか？" },
        { label: "☀️ 農場の気象状況", query: "農場の現在の気温と天候状況を教えてください。" },
        { label: "📋 今日の計画", query: "現在の農業計画の概要を説明してください。" },
        { label: "📊 推奨事項の説明", query: "現在のアクティブな推奨事項を説明してもらえますか？" }
    ],
    ko: [
        { label: "🌱 토양 확인", query: "제 토양 수치를 분석해 주실 수 있나요?" },
        { label: "💧 관개 필요?", query: "오늘 작물에 물을 줘야 하나요?" },
        { label: "🌿 작물 건강", query: "제 작물의 건강 상태는 어떤가요?" },
        { label: "☀️ 농장 기상 조건", query: "농장의 현재 기온과 기상 조건을 요약해 주세요." },
        { label: "📋 오늘의 계획", query: "현재 농업 계획 요약을 설명해 주세요." },
        { label: "📊 추천 설명", query: "현재 활성 추천 사항을 설명해 주실 수 있나요?" }
    ]
};

// Localized Welcome Message
const WELCOME_MESSAGES = {
    en: "Hello, I'm KisanMitra AI. Your intelligent farm companion. I can help you understand:\n\n• Your soil\n• Crop health\n• Irrigation\n• Fertilizer needs\n• Farm recommendations\n• AI agent results\n• Farm planning\n\nAsk me anything about your farm.",
    te: "నమస్కారం, నేను కిసాన్ మిత్ర AI. మీ తెలివైన వ్యవసాయ సహచరుడిని. వీటిని అర్థం చేసుకోవడంలో నేను మీకు సహాయపడగలను:\n\n• మీ మట్టి\n• పంట ఆరోగ్యం\n• నీటి పారుదల\n• ఎరువుల అవసరాలు\n• వ్యవసాయ సిఫార్సులు\n• AI ఏజెంట్ ఫలితాలు\n• వ్యవసాయ ప్రణాళిక\n\nమీ వ్యవసాయం గురించి నన్ను ఏదైనా అడగండి.",
    hi: "नमस्ते, मैं किसानमित्र AI हूँ। आपका बुद्धिमान कृषि साथी। मैं आपको समझने में मदद कर सकता हूँ:\n\n• आपकी मिट्टी\n• फसल का स्वास्थ्य\n• सिंचाई की आवश्यकताएं\n• उर्वरक की आवश्यकता\n• खेत की सिफारिशें\n• एआई एजेंट के परिणाम\n• कृषि योजना\n\nअपने खेत के बारे में मुझसे कुछ भी पूछें।",
    ta: "வணக்கம், நான் கிசான்மித்ரா AI. உங்கள் புத்திசாலித்தனமான பண்ணை கூட்டாளி. இவற்றை நீங்கள் புரிந்து கொள்ள நான் உதவ முடியும்:\n\n• உங்கள் மண்\n• பயிர் ஆரோக்கியம்\n• நீர் பாசனம்\n• உரத் தேவைகள்\n• பண்ணை பரிந்துரைகள்\n• AI ஏஜென்ட் முடிவுகள்\n• பண்ணை திட்டமிடல்\n\nஉங்கள் பண்ணை பற்றி என்னிடம் எது வேண்டுமானாலும் கேளுங்கள்.",
    kn: "ನಮಸ್ಕಾರ, ನಾನು ಕಿಸಾನ್ ಮಿತ್ರ AI. ನಿಮ್ಮ ಬುದ್ಧಿವಂತ ಕೃಷಿ ಸಂಗಾತಿ. ಈ ಕೆಳಗಿನವುಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ:\n\n• ನಿಮ್ಮ ಮಣ್ಣು\n• ಬೆಳೆ ಆರೋಗ್ಯ\n• ನೀರಾವರಿ\n• ರಸಗೊಬ್ಬರ ಅಗತ್ಯಗಳು\n• ತೋಟದ ಶಿಫಾರಸುಗಳು\n• ಎಐ ಏಜೆಂಟ್ ಫಲಿತಾಂಶಗಳು\n• ಕೃಷಿ ಯೋಜನೆ\n\nನಿಮ್ಮ ತೋಟದ ಬಗ್ಗೆ ನನ್ನನ್ನು ಏನಾದರೂ ಕೇಳಿ.",
    ja: "こんにちは、KisanMitra AIです。あなたのインテリジェントな農場アシスタント。以下についてお手伝いできます:\n\n• 土壌分析\n• 作物の健康\n• 灌漑\n• 肥料のニーズ\n• 農場の推奨事項\n• AIエージェントの結果\n• 農場計画\n\n農場について何でも聞いてください。",
    ko: "안녕하세요, 저는 KisanMitra AI입니다. 당신의 지능형 농장 도우미입니다. 다음 사항에 도움을 드릴 수 있습니다:\n\n• 토양 분석\n• 작물 건강\n• 관개\n• 비료 필요량\n• 농장 추천 사항\n• AI 에이전트 결과\n• 농장 계획\n\n농장에 대해 무엇이든 물어보세요."
};

// Play button localized labels
const PLAY_LABELS = {
    en: "🔊 Play Voice",
    te: "🔊 వినిపించు",
    hi: "🔊 आवाज सुनाएं",
    ta: "🔊 ஒலிபரப்பு",
    kn: "🔊 ಧ್ವನಿ ಪ್ಲೇ",
    ja: "🔊 音声再生",
    ko: "🔊 음성 재생"
};

document.addEventListener("DOMContentLoaded", () => {
    const bubble = document.getElementById("kisanmitra-bubble");
    const windowEl = document.getElementById("kisanmitra-window");
    const closeBtn = document.getElementById("kisanmitra-close-btn");
    const sendBtn = document.getElementById("kisanmitra-send-btn");
    const inputField = document.getElementById("kisanmitra-input-field");
    const messagesBody = document.getElementById("kisanmitra-body");
    const langSelect = document.getElementById("kisanmitra-lang-select");
    const clearBtn = document.getElementById("kisanmitra-clear-btn");
    const micBtn = document.getElementById("kisanmitra-mic-btn");
    const autoSpeakCheckbox = document.getElementById("kisanmitra-autospeak");

    let activeLang = langSelect ? langSelect.value : "en";

    // Restore auto-speak preference from localStorage
    const AUTOSPEAK_KEY = "kisanmitra_autospeak";
    if (autoSpeakCheckbox) {
        autoSpeakCheckbox.checked = localStorage.getItem(AUTOSPEAK_KEY) === "1";
        autoSpeakCheckbox.addEventListener("change", () => {
            localStorage.setItem(AUTOSPEAK_KEY, autoSpeakCheckbox.checked ? "1" : "0");
        });
    }

    async function syncSettingsWithStatus() {
        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/api/chat/status`);
            const statusData = await resp.json();
            if (statusData && autoSpeakCheckbox) {
                // If localstorage has not been set yet, use the DB settings
                if (localStorage.getItem(AUTOSPEAK_KEY) === null) {
                    autoSpeakCheckbox.checked = statusData.auto_play_voice;
                    localStorage.setItem(AUTOSPEAK_KEY, statusData.auto_play_voice ? "1" : "0");
                }
            }
        } catch (err) {
            console.error("Failed to sync chatbot status configs:", err);
        }
    }
    syncSettingsWithStatus();

    function isAutoSpeakEnabled() {
        return autoSpeakCheckbox ? autoSpeakCheckbox.checked : false;
    }

    // ── Voice Status Bar (injected dynamically into footer) ──────────────────
    let voiceStatusBar = null;
    if (micBtn) {
        voiceStatusBar = document.createElement("div");
        voiceStatusBar.className = "voice-status-bar";
        voiceStatusBar.innerHTML = `<span class="voice-dot"></span><span id="voice-status-text">Listening…</span>`;
        // Insert above the input row
        micBtn.closest(".kisanmitra-input-row").parentNode
              .insertBefore(voiceStatusBar, micBtn.closest(".kisanmitra-input-row"));
    }

    // Helper functions to open and close chat window
    function openChatWindow() {
        if (windowEl) {
            windowEl.classList.add("active");
            messagesBody.scrollTop = messagesBody.scrollHeight;
            inputField.focus();
        }
    }

    function closeChatWindow() {
        if (windowEl) {
            windowEl.classList.remove("active");
        }
    }

    // Toggle Chat Window via floating bubble
    if (bubble) {
        bubble.addEventListener("click", () => {
            if (windowEl.classList.contains("active")) {
                closeChatWindow();
            } else {
                openChatWindow();
            }
        });
    }

    // Floating bubble event listener is sufficient to toggle the floating chat box

    if (closeBtn) {
        closeBtn.addEventListener("click", closeChatWindow);
    }

    // Language selector change
    if (langSelect) {
        langSelect.addEventListener("change", async (e) => {
            activeLang = e.target.value;
            
            // Update user settings on language preference via POST request
            try {
                const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
                await fetch(`${apiBase}/settings`, {
                    method: "POST",
                    headers: {
                        "Content-Type": "application/x-www-form-urlencoded"
                    },
                    body: `language=${activeLang}`
                });
            } catch (err) {
                console.error("Error setting session language:", err);
            }

            // Refresh chat logs history using new language format context
            loadChatHistory();
        });
    }

    // Clear history logs trigger
    if (clearBtn) {
        clearBtn.addEventListener("click", async () => {
            if (!confirm("Are you sure you want to clear your conversation with KisanMitra AI?")) {
                return;
            }
            
            try {
                const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
                const resp = await fetch(`${apiBase}/api/chat/clear`, { method: "POST" });
                const data = await resp.json();
                if (data.success) {
                    messagesBody.innerHTML = "";
                    appendWelcomeCard();
                }
            } catch (err) {
                console.error("Error clearing chat log:", err);
            }
        });
    }

    // Message submit trigger
    if (sendBtn) {
        sendBtn.addEventListener("click", handleSendMessage);
    }
    if (inputField) {
        inputField.addEventListener("keydown", (e) => {
            if (e.key === "Enter") {
                handleSendMessage();
            }
        });
    }

    // ── Voice Input (SpeechRecognition) ──────────────────────────────────────
    const voiceLangMap = { en: "en-US", te: "te-IN", hi: "hi-IN", ta: "ta-IN", kn: "kn-IN", ja: "ja-JP", ko: "ko-KR" };
    const listeningLabels = { en: "Listening…", te: "వింటోంది…", hi: "सुन रहा है…", ta: "கேட்கிறது…", kn: "ಕೇಳುತ್ತಿದೆ…", ja: "聞いています…", ko: "듣는 중…" };

    let recognition = null;
    let isListening = false;
    let finalTranscript = "";  // accumulates confirmed speech across interim results

    function startVoiceInput() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Voice input is not supported in this browser. Please use Google Chrome.");
            return;
        }

        finalTranscript = "";          // reset on each new session
        if (inputField) inputField.value = "";

        recognition = new SpeechRecognition();
        recognition.lang = voiceLangMap[activeLang] || "en-US";
        recognition.interimResults = true;   // words appear live as you speak
        recognition.maxAlternatives = 1;
        recognition.continuous = false;

        recognition.onstart = () => {
            isListening = true;
            if (micBtn) micBtn.classList.add("mic-active");
            if (voiceStatusBar) {
                document.getElementById("voice-status-text").textContent = listeningLabels[activeLang] || "Listening…";
                voiceStatusBar.classList.add("visible");
            }
            if (inputField) inputField.placeholder = listeningLabels[activeLang] || "Listening…";
        };

        recognition.onresult = (event) => {
            // Accumulate final results + show interim in real time
            let interimTranscript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const res = event.results[i];
                if (res.isFinal) {
                    finalTranscript += res[0].transcript;
                } else {
                    interimTranscript += res[0].transcript;
                }
            }
            // Live update: user sees every word as they speak
            if (inputField) inputField.value = finalTranscript + interimTranscript;
        };

        recognition.onend = () => {
            isListening = false;
            if (micBtn) micBtn.classList.remove("mic-active");
            if (voiceStatusBar) voiceStatusBar.classList.remove("visible");
            if (inputField) inputField.placeholder = "Ask KisanMitra about your farm...";
            // Auto-send only if something was captured
            if (inputField && inputField.value.trim()) {
                handleSendMessage();
            }
        };

        recognition.onerror = (event) => {
            isListening = false;
            if (micBtn) micBtn.classList.remove("mic-active");
            if (voiceStatusBar) voiceStatusBar.classList.remove("visible");
            if (inputField) inputField.placeholder = "Ask KisanMitra about your farm...";
            console.warn("Voice recognition error:", event.error);
        };

        recognition.start();
    }

    function stopVoiceInput() {
        if (recognition) recognition.stop();
    }

    if (micBtn) {
        micBtn.addEventListener("click", () => {
            if (isListening) {
                stopVoiceInput();
            } else {
                startVoiceInput();
            }
        });
    }

    // Load Chat history from SQLite logs on setup
    async function loadChatHistory() {
        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/api/chat/history?limit=20`);
            const data = await resp.json();
            
            messagesBody.innerHTML = "";
            appendWelcomeCard();

            if (data.success && data.history && data.history.length > 0) {
                data.history.forEach(msg => {
                    appendMessageBubble(msg.role, msg.message);
                });
            }
        } catch (err) {
            console.error("Error loading chat history:", err);
        }
    }

    // Helper: append system welcome card with quick-actions chips
    function appendWelcomeCard() {
        const welcomeCard = document.createElement("div");
        welcomeCard.className = "kisanmitra-welcome-card";
        
        const welcomeText = WELCOME_MESSAGES[activeLang] || WELCOME_MESSAGES["en"];
        welcomeCard.innerHTML = `<div style="font-size: 13.5px; line-height: 1.6; color: #333; white-space: pre-line;">🌱 ${formatWelcomeMarkdown(welcomeText)}</div>`;
        
        // Append quick action chips container
        const chipsGrid = document.createElement("div");
        chipsGrid.className = "quick-actions-grid";
        chipsGrid.id = "quick-actions-container-inner";
        welcomeCard.appendChild(chipsGrid);

        messagesBody.appendChild(welcomeCard);
        renderQuickActions();
    }

    // Parse bullet formatting for welcome card
    function formatWelcomeMarkdown(text) {
        return text.replace(/• /g, " • ");
    }

    // Helper: Render quick action chips matching active language
    function renderQuickActions() {
        const container = document.getElementById("quick-actions-container-inner");
        if (!container) return;

        container.innerHTML = "";
        const chips = QUICK_ACTIONS[activeLang] || QUICK_ACTIONS["en"];

        chips.forEach(chip => {
            const el = document.createElement("div");
            el.className = "quick-action-chip";
            el.textContent = chip.label;
            el.addEventListener("click", () => {
                inputField.value = chip.query;
                handleSendMessage();
            });
            container.appendChild(el);
        });
    }

    // Helper: Append a message bubble to the chat logs area
    function appendMessageBubble(role, text) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `chat-msg ${role === 'user' ? 'user' : 'assistant'}`;

        const avatar = document.createElement("div");
        avatar.className = "chat-msg-avatar";
        avatar.textContent = role === 'user' ? "👨‍🌾" : "🌱";

        const bubble = document.createElement("div");
        bubble.className = "chat-msg-bubble";
        
        // Clean text content
        let formattedText = formatMarkdown(text);
        bubble.innerHTML = formattedText;

        // Append play button for assistant voice outputs
        let playBtn = null;
        if (role === 'assistant' && !text.includes("AI service is not configured")) {
            playBtn = document.createElement("button");
            playBtn.className = "tts-play-btn";
            const btnLabel = PLAY_LABELS[activeLang] || PLAY_LABELS["en"];
            playBtn.innerHTML = btnLabel;
            playBtn.addEventListener("click", () => playVoiceTTS(text, playBtn));
            bubble.appendChild(playBtn);
        }

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(bubble);
        messagesBody.appendChild(msgDiv);
        messagesBody.scrollTop = messagesBody.scrollHeight;

        // Auto-speak every new assistant reply — only if user opted in
        if (role === 'assistant' && !text.includes("AI service is not configured") && isAutoSpeakEnabled()) {
            autoSpeak(text, playBtn);
        }
    }

    // Global tracking of speaking voice to allow "Stop speaking" interaction
    let currentSpeechButton = null;
    let currentSpeechOriginalLabel = "";
    let currentSpeechAudio = null;

    const STOP_LABELS = {
        en: "🛑 Stop",
        te: "🛑 ఆపు",
        hi: "🛑 रोकें",
        ta: "🛑 நிறுத்து",
        kn: "🛑 ನಿಲ್ಲಿಸು",
        ja: "🛑 停止",
        ko: "🛑 정지"
    };

    function stopVoiceTTS() {
        if (currentSpeechAudio) {
            try {
                currentSpeechAudio.pause();
                currentSpeechAudio.currentTime = 0;
            } catch (e) {}
            currentSpeechAudio = null;
        }
        if (window.speechSynthesis) {
            window.speechSynthesis.cancel();
        }
        if (currentSpeechButton) {
            currentSpeechButton.innerHTML = currentSpeechOriginalLabel;
            currentSpeechButton.classList.remove("speaking");
            currentSpeechButton.disabled = false;
            currentSpeechButton = null;
        }
    }

    // Auto-speak — fires silently after each AI reply (no UI button interaction needed)
    function autoSpeak(text, buttonElement) {
        if (!('speechSynthesis' in window)) return;
        stopVoiceTTS();

        const originalLabel = buttonElement ? buttonElement.innerHTML : (PLAY_LABELS[activeLang] || "🔊 Play Voice");
        if (buttonElement) {
            currentSpeechButton = buttonElement;
            currentSpeechOriginalLabel = originalLabel;
            buttonElement.innerHTML = STOP_LABELS[activeLang] || "🛑 Stop";
            buttonElement.classList.add("speaking");
            buttonElement.disabled = false;
        }

        const cleanText = text.replace(/\*\*/g, '').replace(/\*/g, '').replace(/•/g, '').replace(/<[^>]+>/g, '');
        const utterance = new SpeechSynthesisUtterance(cleanText);
        const vMap = { en: "en-US", te: "te-IN", hi: "hi-IN", ta: "ta-IN", kn: "kn-IN", ja: "ja-JP", ko: "ko-KR" };
        const targetLang = vMap[activeLang] || "en-US";
        utterance.lang = targetLang;
        utterance.rate = 0.95;
        const voice = _pickVoice(targetLang);
        if (voice) utterance.voice = voice;

        utterance.onend = () => {
            if (currentSpeechButton === buttonElement) {
                stopVoiceTTS();
            }
        };
        utterance.onerror = () => {
            if (currentSpeechButton === buttonElement) {
                stopVoiceTTS();
            }
        };
        window.speechSynthesis.speak(utterance);
    }

    // ElevenLabs Speech synthesis API play control with Web Speech fallback
    async function playVoiceTTS(text, buttonElement) {
        if (currentSpeechButton === buttonElement) {
            stopVoiceTTS();
            return;
        }

        stopVoiceTTS();

        const originalLabel = buttonElement.innerHTML;
        currentSpeechButton = buttonElement;
        currentSpeechOriginalLabel = originalLabel;

        buttonElement.innerHTML = STOP_LABELS[activeLang] || "🛑 Stop";
        buttonElement.classList.add("speaking");
        buttonElement.disabled = false;

        const browserOnlyLangs = new Set(["te", "ta", "kn"]);
        if (browserOnlyLangs.has(activeLang)) {
            speakBrowserTTS(text, buttonElement, originalLabel);
            return;
        }

        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/api/chat/tts`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({ text: text, language: activeLang })
            });

            if (resp.ok) {
                const blob = await resp.blob();
                const audioUrl = URL.createObjectURL(blob);
                const audio = new Audio(audioUrl);
                currentSpeechAudio = audio;
                audio.play().catch(e => {
                    speakBrowserTTS(text, buttonElement, originalLabel);
                });
                audio.onended = () => {
                    if (currentSpeechButton === buttonElement) {
                        stopVoiceTTS();
                    }
                };
            } else {
                speakBrowserTTS(text, buttonElement, originalLabel);
            }
        } catch (err) {
            speakBrowserTTS(text, buttonElement, originalLabel);
        }
    }

    // Preload the browser voice list once (it loads asynchronously in most browsers)
    let _cachedVoices = [];
    function _loadVoices() {
        _cachedVoices = window.speechSynthesis.getVoices();
    }
    _loadVoices();
    if (window.speechSynthesis.onvoiceschanged !== undefined) {
        window.speechSynthesis.onvoiceschanged = _loadVoices;
    }

    // Pick the best matching SpeechSynthesisVoice for a BCP-47 locale string
    function _pickVoice(bcp47) {
        const voices = _cachedVoices.length ? _cachedVoices : window.speechSynthesis.getVoices();
        const lang   = bcp47.toLowerCase();
        const prefix = lang.split("-")[0];          // e.g. "te" from "te-in"

        // 1. Exact locale match (te-IN)
        let match = voices.find(v => v.lang.toLowerCase() === lang);
        // 2. Any voice whose lang starts with the same prefix (te-*)
        if (!match) match = voices.find(v => v.lang.toLowerCase().startsWith(prefix));
        // 3. Any voice with the prefix anywhere in lang
        if (!match) match = voices.find(v => v.lang.toLowerCase().includes(prefix));
        return match || null;
    }

    // Browser Speech Synthesis with proper voice selection
    function speakBrowserTTS(text, buttonElement, originalLabel) {
        if (!("speechSynthesis" in window)) {
            if (currentSpeechButton === buttonElement) {
                stopVoiceTTS();
            }
            return;
        }

        window.speechSynthesis.cancel();

        const cleanText = text.replace(/\*\*/g, "").replace(/\*/g, "").replace(/•/g, "");

        const voiceLangMap = {
            en: "en-US",
            te: "te-IN",
            hi: "hi-IN",
            ta: "ta-IN",
            kn: "kn-IN",
            ja: "ja-JP",
            ko: "ko-KR"
        };
        const targetLang = voiceLangMap[activeLang] || "en-US";

        function _doSpeak() {
            const utterance = new SpeechSynthesisUtterance(cleanText);
            utterance.lang  = targetLang;

            const voice = _pickVoice(targetLang);
            if (voice) utterance.voice = voice;

            utterance.onend = () => {
                if (currentSpeechButton === buttonElement) {
                    stopVoiceTTS();
                }
            };
            utterance.onerror = () => {
                if (currentSpeechButton === buttonElement) {
                    stopVoiceTTS();
                }
            };
            window.speechSynthesis.speak(utterance);
        }

        // Voices may not be loaded yet — wait up to 1 s for them
        const voices = window.speechSynthesis.getVoices();
        if (voices.length > 0) {
            _cachedVoices = voices;
            _doSpeak();
        } else {
            let waited = 0;
            const poll = setInterval(() => {
                const v = window.speechSynthesis.getVoices();
                waited += 50;
                if (v.length > 0 || waited >= 1000) {
                    clearInterval(poll);
                    if (v.length > 0) _cachedVoices = v;
                    _doSpeak();
                }
            }, 50);
        }
    }

    // Helper: Add thinking animated indicator loader
    let thinkingElement = null;
    function showThinkingIndicator() {
        removeThinkingIndicator();
        
        const loader = document.createElement("div");
        loader.className = "chat-msg assistant";
        loader.id = "kisanmitra-loader-bubble";

        const avatar = document.createElement("div");
        avatar.className = "chat-msg-avatar";
        avatar.textContent = "🌱";

        const bubble = document.createElement("div");
        bubble.className = "chat-msg-bubble kisanmitra-thinking";
        
        let label = "KisanMitra is thinking";
        if (activeLang === 'te') label = "కిసాన్ మిత్ర ఆలోచిస్తోంది";
        if (activeLang === 'hi') label = "किसानमित्र सोच रहा है";
        if (activeLang === 'ta') label = "கிசான்மித்ரா யோசிக்கிறது";
        if (activeLang === 'kn') label = "ಕಿಸಾನ್ ಮಿತ್ರ ಯೋಚಿಸುತ್ತಿದೆ";

        bubble.innerHTML = `
            <span>${label}</span>
            <div class="thinking-dots">
                <span></span>
                <span></span>
                <span></span>
            </div>
        `;

        loader.appendChild(avatar);
        loader.appendChild(bubble);
        messagesBody.appendChild(loader);
        messagesBody.scrollTop = messagesBody.scrollHeight;
        thinkingElement = loader;
    }

    function removeThinkingIndicator() {
        if (thinkingElement) {
            thinkingElement.remove();
            thinkingElement = null;
        }
        const oldLoader = document.getElementById("kisanmitra-loader-bubble");
        if (oldLoader) oldLoader.remove();
    }

    // Submit handler
    async function handleSendMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        // Clear input field immediately
        inputField.value = "";

        // Append user bubble to UI
        appendMessageBubble("user", text);

        // Display thinking loader
        showThinkingIndicator();

        try {
            const apiBase = window.KISANMITRA_CONFIG?.apiBase || "";
            const resp = await fetch(`${apiBase}/api/chat`, {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                    "X-Requested-With": "XMLHttpRequest"
                },
                body: JSON.stringify({
                    message: text,
                    language: activeLang
                })
            });
            const data = await resp.json();
            
            removeThinkingIndicator();

            if (data.success && data.message) {
                appendMessageBubble("assistant", data.message);
            } else {
                appendMessageBubble("assistant", data.error || "Sorry, I encountered an error. Please try again.");
            }
        } catch (err) {
            removeThinkingIndicator();
            appendMessageBubble("assistant", "Sorry, I couldn't connect to the server. Please check your internet connection.");
        }
    }

    // Simple Safe Markdown formatter parser (Converts bullets, headers, bold, line breaks)
    function formatMarkdown(text) {
        if (!text) return "";
        // Sanitize html tags to prevent XSS injection
        let escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        // Bold tags formatting
        escaped = escaped.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

        // Bullet list parsing (lines starting with - or *)
        let lines = escaped.split("\n");
        let inList = false;
        for (let i = 0; i < lines.length; i++) {
            let line = lines[i].trim();
            if (line.startsWith("- ") || line.startsWith("* ") || line.startsWith("• ")) {
                let content = line.substring(2);
                if (!inList) {
                    lines[i] = "<ul><li>" + content + "</li>";
                    inList = true;
                } else {
                    lines[i] = "<li>" + content + "</li>";
                }
            } else {
                if (inList) {
                    lines[i - 1] += "</ul>";
                    inList = false;
                }
                // Paragraph wrapper if not empty line
                if (line) {
                    lines[i] = "<p>" + line + "</p>";
                }
            }
        }
        if (inList) {
            lines[lines.length - 1] += "</ul>";
        }

        return lines.join("");
    }

    // Initial trigger
    loadChatHistory();
});
