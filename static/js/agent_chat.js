/* Reusable Agent Chat JavaScript Logic */

const AGENTS_CONFIG = {
    'weather': {
        name: 'Weather Agent',
        emoji: '🌦️',
        icon: 'agent-weather.png',
        color: '#8CC8F2',
        description: 'Monitors weather hazards and advises crop-climate decisions.',
        accentColor: '#1a6693',
        bgLight: '#e8f4fd',
        bgDark: '#d1eaf7',
        quickQuestions: {
            en: [
                "Will rain affect my crop?",
                "Is the current temperature safe for my crop?",
                "Should I irrigate if rainfall is expected?",
                "What is my current weather risk?"
            ],
            te: [
                "నా పంటపై వర్షం ప్రభావం చూపుతుందా?",
                "ప్రస్తుత ఉష్ణోగ్రత నా పంటకు సురక్షితమేనా?",
                "వర్షం పడే అవకాశం ఉంటే నేను నీరు పెట్టాలా?",
                "నా ప్రస్తుత వాతావరణ ప్రమాదం ఏమిటి?"
            ],
            hi: [
                "क्या बारिश मेरी फसल को प्रभावित करेगी?",
                "क्या वर्तमान तापमान मेरी फसल के लिए सुरक्षित है?",
                "यदि बारिश की उम्मीद है तो क्या मुझे सिंचाई करनी चाहिए?",
                "मेरा वर्तमान मौसम जोखिम क्या है?"
            ],
            ta: [
                "மழை என் பயிரை பாதிக்குமா?",
                "தற்போதைய வெப்பநிலை என் பயிருக்கு பாதுகாப்பானதா?",
                "மழை பெய்யும் என எதிர்பார்க்கப்பட்டால் நான் நீர் பாய்ச்ச வேண்டுமா?",
                "எனது தற்போதைய வானிலை ஆபத்து என்ன?"
            ],
            kn: [
                "ಮಳೆ ನನ್ನ ಬೆಳೆಯ ಮೇಲೆ ಪರಿಣಾಮ ಬೀರುತ್ತದೆಯೇ?",
                "ಪ್ರಸ್ತುತ ತಾಪಮಾನ ನನ್ನ ಬೆಳೆಗೆ ಸುರಕ್ಷಿತವೇ?",
                "ಮಳೆ ಬರುವ ನಿರೀಕ್ಷೆ ಇದ್ದರೆ ನಾನು ನೀರುಣಿಸಬೇಕೇ?",
                "ನನ್ನ ಪ್ರಸ್ತುತ ಹವಾಮಾನ ಅಪಾಯ ಏನು?"
            ]
        }
    },
    'soil': {
        name: 'Soil Agent',
        emoji: '🌱',
        icon: 'agent-soil.png',
        color: '#6FAF7B',
        description: 'Analyzes soil health, hydration, and nutrient levels.',
        accentColor: '#285943',
        bgLight: '#EAF7EC',
        bgDark: '#DDF3E2',
        quickQuestions: {
            en: [
                "Why is my soil health low?",
                "Is my soil moisture sufficient?",
                "Which nutrient needs attention?",
                "How does my soil affect my crop?"
            ],
            te: [
                "నా నేల ఆరోగ్యం ఎందుకు తక్కువగా ఉంది?",
                "నా నేల తేమ సరిపోతుందా?",
                "ఏ పోషకంపై శ్రద్ధ వహించాలి?",
                "నా నేల నా పంటను ఎలా ప్రభావితం చేస్తుంది?"
            ],
            hi: [
                "मेरी मिट्टी का स्वास्थ्य कम क्यों है?",
                "क्या मेरी मिट्टी की नमी पर्याप्त है?",
                "किस पोषक तत्व पर ध्यान देने की आवश्यकता है?",
                "मेरी मिट्टी मेरी फसल को कैसे प्रभावित करती है?"
            ],
            ta: [
                "என் மண்ணின் ஆரோக்கியம் ஏன் குறைவாக உள்ளது?",
                "என் மண்ணின் ஈரப்பதம் போதுமானதா?",
                "எந்த ஊட்டச்சத்துக்கு கவனம் தேவை?",
                "என் மண் என் பயிரை எவ்வாறு பாதிக்கிறது?"
            ],
            kn: [
                "ನನ್ನ ಮಣ್ಣಿನ ಆರೋಗ್ಯ ಏಕೆ ಕಡಿಮೆಯಾಗಿದೆ?",
                "ನನ್ನ ಮಣ್ಣಿನ ತೇವಾಂಶ ಸಾಕಾಗಿದೆಯೇ?",
                "ಯಾವ ಪೋಷಕಾಂಶಕ್ಕೆ ಗಮನ ನೀಡಬೇಕು?",
                "ನನ್ನ ಮಣ್ಣು ನನ್ನ ಬೆಳೆಯ ಮೇಲೆ ಹೇಗೆ ಪರಿಣಾಮ ಬೀರುತ್ತದೆ?"
            ]
        }
    },
    'crop-disease': {
        name: 'Crop Disease Agent',
        emoji: '🌿',
        icon: 'agent-crop-disease.png',
        color: '#D97D7D',
        description: 'Monitors crop health and detects diseases early.',
        accentColor: '#802626',
        bgLight: '#FDF2F2',
        bgDark: '#FDE8E8',
        quickQuestions: {
            en: [
                "Why is my crop showing yellow leaves?",
                "Is this disease serious?",
                "What should I monitor?",
                "What could be causing crop symptoms?"
            ],
            te: [
                "నా పంట ఆకులు పసుపు రంగులోకి ఎందుకు మారుతున్నాయి?",
                "ఈ వ్యాధి తీవ్రమైనదా?",
                "నేను దేనిని పర్యవేక్షించాలి?",
                "పంట లక్షణాలకు కారణం ఏమిటి?"
            ],
            hi: [
                "मेरी फसल में पीले पत्ते क्यों दिखाई दे रहे हैं?",
                "क्या यह बीमारी गंभीर है?",
                "मुझे क्या निगरानी करनी चाहिए?",
                "फसल के लक्षणों का क्या कारण हो सकता है?"
            ],
            ta: [
                "என் பயிரில் ஏன் மஞ்சள் இலைகள் தோன்றுகின்றன?",
                "இந்த நோய் தீவிரமானதா?",
                "நான் எதை கண்காணிக்க வேண்டும்?",
                "பயிர் அறிகுறிகளுக்கு என்ன காரணம்?"
            ],
            kn: [
                "ನನ್ನ ಬೆಳೆ ಏಕೆ ಹಳದಿ ಎಲೆಗಳನ್ನು ತೋರಿಸುತ್ತಿದೆ?",
                "ಈ ರೋಗವು ಗಂಭೀರವಾಗಿದೆಯೇ?",
                "ನಾನು ಏನನ್ನು ಮೇಲ್ವಿಚಾರಣೆ ಮಾಡಬೇಕು?",
                "ಬೆಳೆಯ ರೋಗಲಕ್ಷಣಗಳಿಗೆ ಕಾರಣವೇನು?"
            ]
        }
    },
    'irrigation': {
        name: 'Irrigation Agent',
        emoji: '💧',
        icon: 'agent-irrigation.png',
        color: '#59B8E8',
        description: 'Optimizes water distribution and valve schedules.',
        accentColor: '#1d5573',
        bgLight: '#eef8fd',
        bgDark: '#daf0fc',
        quickQuestions: {
            en: [
                "Why do I need irrigation?",
                "When should I irrigate?",
                "Is my soil moisture enough?",
                "Can I skip irrigation if it rains?"
            ],
            te: [
                "నాకు నీటి పారుదల ఎందుకు అవసరం?",
                "నేను ఎప్పుడు నీరు పెట్టాలి?",
                "నా నేల తేమ సరిపోతుందా?",
                "వర్షం పడితే నీరు పెట్టడం ఆపవచ్చా?"
            ],
            hi: [
                "मुझे सिंचाई की आवश्यकता क्यों है?",
                "मुझे कब सिंचाई करनी चाहिए?",
                "क्या मेरी मिट्टी की नमी पर्याप्त है?",
                "क्या बारिश होने पर मैं सिंचाई छोड़ सकता हूँ?"
            ],
            ta: [
                "எனக்கு ஏன் நீர் பாசனம் தேவை?",
                "நான் எப்போது நீர் பாய்ச்ச வேண்டும்?",
                "என் மண்ணின் ஈரப்பதம் போதுமானதா?",
                "மழை பெய்தால் நீர் பாசனத்தை தவிர்க்கலாமா?"
            ],
            kn: [
                "ನನಗೆ ನೀರಾವರಿ ಏಕೆ ಬೇಕು?",
                "ನಾನು ಯಾವಾಗ ನೀರುಣಿಸಬೇಕು?",
                "ನನ್ನ ಮಣ್ಣಿನ ತೇವಾಂಶ ಸಾಕಾಗಿದೆಯೇ?",
                "ಮಳೆ ಬಂದರೆ ನೀರಾವರಿಯನ್ನು ಬಿಡಬಹುದೇ?"
            ]
        }
    },
    'fertilizer': {
        name: 'Fertilizer Agent',
        emoji: '🧪',
        icon: 'agent-fertilizer.png',
        color: '#E8B85C',
        description: 'Generates crop-specific nutrient application plans.',
        accentColor: '#75561a',
        bgLight: '#fefcf6',
        bgDark: '#fbf0d8',
        quickQuestions: {
            en: [
                "Which nutrient is low?",
                "Why are you recommending fertilizer?",
                "What does my NPK indicate?",
                "Should I apply fertilizer now?"
            ],
            te: [
                "ఏ పోషకం తక్కువగా ఉంది?",
                "మీరు ఎరువును ఎందుకు సిఫార్సు చేస్తున్నారు?",
                "నా NPK దేనిని సూచిస్తుంది?",
                "నేను ఇప్పుడు ఎరువులు వేయాలా?"
            ],
            hi: [
                "कौन सा पोषक तत्व कम है?",
                "आप उर्वरक की सिफारिश क्यों कर रहे हैं?",
                "मेरा NPK क्या दर्शाता है?",
                "क्या मुझे अभी उर्वरक डालना चाहिए?"
            ],
            ta: [
                "எந்த ஊட்டச்சத்து குறைவாக உள்ளது?",
                "நீங்கள் ஏன் உரத்தை பரிந்துரைக்கிறீர்கள்?",
                "என் NPK எதை குறிக்கிறது?",
                "நான் இப்போது உரம் போட வேண்டுமா?"
            ],
            kn: [
                "ಯಾವ ಪೋಷಕಾಂಶ ಕಡಿಮೆಯಾಗಿದೆ?",
                "ನೀವು ರಸಗೊಬ್ಬರವನ್ನು ಏಕೆ ಶಿಫಾರಸು ಮಾಡುತ್ತಿದ್ದೀರಿ?",
                "ನನ್ನ NPK ಏನನ್ನು ಸೂಚಿಸುತ್ತದೆ?",
                "ನಾನು ಈಗ ರಸಗೊಬ್ಬರವನ್ನು ಹಾಕಬೇಕೇ?"
            ]
        }
    },
    'market': {
        name: 'Market Agent',
        emoji: '📈',
        icon: 'agent-market.png',
        color: '#B38CD9',
        description: 'Tracks commodity prices and optimal selling windows.',
        accentColor: '#533475',
        bgLight: '#faf6fe',
        bgDark: '#eeddf5',
        quickQuestions: {
            en: [
                "Is the current market trend good?",
                "Should I consider selling now?",
                "Why is the market risk high?",
                "What is my current market trend?"
            ],
            te: [
                "ప్రస్తుత మార్కెట్ ధోరణి బాగుందా?",
                "నేను ఇప్పుడు విక్రయించాలా?",
                "మార్కెట్ ప్రమాదం ఎందుకు ఎక్కువగా ఉంది?",
                "నా ప్రస్తుత మార్కెట్ ధోరణి ఏమిటి?"
            ],
            hi: [
                "क्या वर्तमान बाजार का रुझान अच्छा है?",
                "क्या मुझे अभी बेचने पर विचार करना चाहिए?",
                "बाजार का जोखिम अधिक क्यों है?",
                "मेरा वर्तमान बाजार रुझान क्या है?"
            ],
            ta: [
                "தற்போதைய சந்தை போக்கு நன்றாக உள்ளதா?",
                "நான் இப்போது விற்பதை கருத்தில் கொள்ள வேண்டுமா?",
                "சந்தை ஆபத்து ஏன் அதிகமாக உள்ளது?",
                "எனது தற்போதைய சந்தை போக்கு என்ன?"
            ],
            kn: [
                "ಪ್ರಸ್ತುತ ಮಾರುಕಟ್ಟೆ ಪ್ರವೃತ್ತಿ ಚೆನ್ನಾಗಿದೆಯೇ?",
                "ನಾನು ಈಗ ಮಾರಾಟ ಮಾಡಲು ಯೋಚಿಸಬೇಕೇ?",
                "ಮಾರುಕಟ್ಟೆ ಅಪಾಯ ಏಕೆ ಹೆಚ್ಚಾಗಿದೆ?",
                "ನನ್ನ ಪ್ರಸ್ತುತ ಮಾರುಕಟ್ಟೆ ಪ್ರವೃತ್ತಿ ಏನು?"
            ]
        }
    },
    'farm-planning': {
        name: 'Farm Planning Agent',
        emoji: '🧠',
        icon: 'agent-farm-planning.png',
        color: '#285943',
        description: 'Coordinates data from all agents to synthesize farm strategy.',
        accentColor: '#173628',
        bgLight: '#edf5f1',
        bgDark: '#d4e6dd',
        quickQuestions: {
            en: [
                "What should I do today?",
                "What is the most important problem on my farm?",
                "Why is my farm risk high?",
                "Explain the recommendations from all agents.",
                "Are the Disease and Weather Agents indicating the same risk?"
            ],
            te: [
                "నేను ఈ రోజు ఏమి చేయాలి?",
                "నా పొలంలో అత్యంత ముఖ్యమైన సమస్య ఏమిటి?",
                "నా వ్యవసాయ ప్రమాదం ఎందుకు ఎక్కువగా ఉంది?",
                "అన్ని ఏజెంట్ల నుండి వచ్చిన సిఫార్సులను వివరించండి.",
                "వ్యాధి మరియు వాతావరణ ఏజెంట్లు ఒకే విధమైన ప్రమాదాన్ని సూచిస్తున్నారా?"
            ],
            hi: [
                "मुझे आज क्या करना चाहिए?",
                "मेरे खेत की सबसे बड़ी समस्या क्या है?",
                "मेरे खेत का जोखिम अधिक क्यों है?",
                "सभी एजेंटों की सिफारिशों को समझाएं।",
                "क्या रोग और मौसम एजेंट एक ही जोखिम का संकेत दे रहे हैं?"
            ],
            ta: [
                "நான் இன்று என்ன செய்ய வேண்டும்?",
                "என் பண்ணையில் மிக முக்கியமான பிரச்சனை என்ன?",
                "என் பண்ணை ஆபத்து ஏன் அதிகமாக உள்ளது?",
                "அனைத்து ஏஜென்ட்களின் பரிந்துரைகளையும் விளக்குங்கள்.",
                "நோய் மற்றும் வானிலை ஏஜென்ட்கள் ஒரே ஆபத்தை குறிக்கின்றனவா?"
            ],
            kn: [
                "ನಾನು ಇಂದು ಏನು ಮಾಡಬೇಕು?",
                "ನನ್ನ ತೋಟದಲ್ಲಿನ ಪ್ರಮುಖ ಸಮಸ್ಯೆ ಏನು?",
                "ನನ್ನ ತೋಟದ ಅಪಾಯ ಏಕೆ ಹೆಚ್ಚಾಗಿದೆ?",
                "ಎಲ್ಲಾ ಏಜೆಂಟರ ಶಿಫಾರಸುಗಳನ್ನು ವಿವರಿಸಿ.",
                "ರೋಗ ಮತ್ತು ಹವಾಮಾನ ಏಜೆಂಟರು ಒಂದೇ ಅಪಾಯವನ್ನು ಸೂಚಿಸುತ್ತಿದ್ದಾರೆಯೇ?"
            ]
        }
    }
};

const AGENT_WELCOME_MESSAGES = {
    en: "Hello! I am your {emoji} {name}. I am a specialist farming assistant focused on {desc}.\n\nAsk me anything within my domain.",
    te: "నమస్కారం! నేను మీ {emoji} {name}. నేను {desc} పై దృష్టి కేంద్రీకరించిన ప్రత్యేక వ్యవసాయ సహాయకుడిని.\n\nనా పరిధిలోని ఏదైనా నన్ను అడగండి.",
    hi: "नमस्ते! मैं आपका {emoji} {name} हूँ। मैं {desc} पर केंद्रित एक विशेषज्ञ कृषि सहायक हूँ।\n\nअपने अधिकार क्षेत्र के अंतर्गत मुझसे कुछ भी पूछें।",
    ta: "வணக்கம்! நான் உங்கள் {emoji} {name}. நான் {desc} என்பதில் கவனம் செலுத்தும் ஒரு சிறப்பு விவசாய உதவியாளர்.\n\nஎன் எல்லைக்குள் எது வேண்டுமானாலும் கேளுங்கள்.",
    kn: "ನಮಸ್ಕಾರ! ನಾನು ನಿಮ್ಮ {emoji} {name}. ನಾನು {desc} ಮೇಲೆ ಕೇಂದ್ರೀಕರಿಸಿದ ತಜ್ಞ ಕೃಷಿ ಸಹಾಯಕ.\n\nನನ್ನ ವ್ಯಾಪ್ತಿಯಲ್ಲಿ ಏನನ್ನಾದರೂ ಕೇಳಿ."
};

const AGENT_PLAY_LABELS = {
    en: "🔊 Play Voice",
    te: "🔊 వినిపించు",
    hi: "🔊 आवाज सुनाएं",
    ta: "🔊 ஒலிபரப்பு",
    kn: "🔊 ధ್ವನಿ ప್ಲೇ"
};

const AGENT_STOP_LABELS = {
    en: "🛑 Stop",
    te: "🛑 ఆపు",
    hi: "🛑 रोकें",
    ta: "🛑 நிறுத்து",
    kn: "🛑 ನಿಲ್ಲಿಸು"
};

const AGENT_THINKING_LABELS = {
    en: "Thinking…",
    te: "ఆలోచిస్తోంది…",
    hi: "सोच रहा है…",
    ta: "யோசிக்கிறது…",
    kn: "ಯೋಚಿಸುತ್ತಿದೆ…"
};

document.addEventListener("DOMContentLoaded", () => {
    const container = document.getElementById("agent-chat-container");
    const windowEl = document.getElementById("agent-chat-window");
    const bubble = document.getElementById("agent-chat-bubble");
    const bubbleIcon = document.getElementById("agent-chat-bubble-icon");
    const bubbleLabel = document.getElementById("agent-chat-bubble-label");
    const closeBtn = document.getElementById("agent-chat-close-btn");
    const sendBtn = document.getElementById("agent-chat-send-btn");
    const inputField = document.getElementById("agent-chat-input-field");
    const messagesBody = document.getElementById("agent-chat-body");
    const langSelect = document.getElementById("agent-chat-lang-select");
    const clearBtn = document.getElementById("agent-chat-clear-btn");
    const micBtn = document.getElementById("agent-chat-mic-btn");
    const autoSpeakCheckbox = document.getElementById("agent-chat-autospeak");

    let activeAgent = null; // slug like 'soil', 'weather'
    let activeLang = "en";

    // Setup LocalStorage autospeak key
    const AGENT_AUTOSPEAK_KEY = "agent_chat_autospeak";
    if (autoSpeakCheckbox) {
        autoSpeakCheckbox.checked = localStorage.getItem(AGENT_AUTOSPEAK_KEY) === "1";
        autoSpeakCheckbox.addEventListener("change", () => {
            localStorage.setItem(AGENT_AUTOSPEAK_KEY, autoSpeakCheckbox.checked ? "1" : "0");
        });
    }

    function isAutoSpeakEnabled() {
        return autoSpeakCheckbox ? autoSpeakCheckbox.checked : false;
    }

    // Voice Status Bar setup
    let voiceStatusBar = null;
    if (micBtn) {
        voiceStatusBar = document.createElement("div");
        voiceStatusBar.className = "voice-status-bar";
        voiceStatusBar.innerHTML = `<span class="voice-dot"></span><span id="agent-voice-status-text">Listening…</span>`;
        micBtn.closest(".kisanmitra-input-row").parentNode
              .insertBefore(voiceStatusBar, micBtn.closest(".kisanmitra-input-row"));
    }

    // Minimize and toggle buttons
    function openChatWindow() {
        if (windowEl) {
            windowEl.classList.add("active");
            bubble.style.display = "none";
            messagesBody.scrollTop = messagesBody.scrollHeight;
            inputField.focus();
        }
    }

    function closeChatWindow() {
        if (windowEl) {
            windowEl.classList.remove("active");
            bubble.style.display = "flex";
        }
    }

    if (closeBtn) closeBtn.addEventListener("click", closeChatWindow);
    if (bubble) bubble.addEventListener("click", openChatWindow);

    // Global initializer function called from buttons [ Ask Weather Agent ] etc
    window.askAgentChat = async function(agentSlug) {
        const config = AGENTS_CONFIG[agentSlug];
        if (!config) return;

        stopVoiceTTS();

        // 1. Hide KisanMitra general chatbot window and bubble to prevent overlay
        const kmWindow = document.getElementById("kisanmitra-window");
        const kmBubble = document.getElementById("kisanmitra-bubble");
        if (kmWindow) kmWindow.classList.remove("active");
        if (kmBubble) kmBubble.style.opacity = "0.3"; // Dim it or hide it

        // 2. Set active agent properties
        activeAgent = agentSlug;
        
        // Load active language preference
        const appLang = document.documentElement.lang || "en";
        activeLang = ['en','te','hi','ta','kn'].includes(appLang) ? appLang : 'en';
        if (langSelect) langSelect.value = activeLang;

        // 3. Apply custom colors to CSS variables
        container.style.setProperty('--agent-accent', config.color);
        container.style.setProperty('--agent-accent-alpha', config.color + '33');
        container.style.setProperty('--agent-accent-alpha-light', config.color + '20');
        container.style.setProperty('--agent-bg-light', config.bgLight);
        container.style.setProperty('--agent-bg-dark', config.bgDark);
        container.style.setProperty('--agent-text-color', config.accentColor);
        container.style.setProperty('--agent-bg-track', config.bgDark);

        // 4. Update Header Elements
        document.getElementById("agent-chat-title").innerHTML = `${config.emoji} ${config.name}`;
        document.getElementById("agent-chat-subtitle").textContent = config.description;

        // 5. Update Bubble details
        if (bubbleIcon) bubbleIcon.textContent = config.emoji;
        if (bubbleLabel) bubbleLabel.textContent = config.name;

        // Display container
        container.style.display = "block";
        openChatWindow();

        // 6. Fetch history and render welcome
        await loadAgentChatHistory();
    };

    if (langSelect) {
        langSelect.addEventListener("change", async (e) => {
            activeLang = e.target.value;
            await loadAgentChatHistory();
        });
    }

    if (clearBtn) {
        clearBtn.addEventListener("click", async () => {
            if (!confirm(`Are you sure you want to clear your conversation with the ${AGENTS_CONFIG[activeAgent].name}?`)) {
                return;
            }
            try {
                const resp = await fetch("/api/agent-chat/clear", {
                    method: "POST",
                    headers: { "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest" },
                    body: JSON.stringify({ agent: activeAgent })
                });
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

    if (sendBtn) sendBtn.addEventListener("click", handleSendMessage);
    if (inputField) {
        inputField.addEventListener("keydown", (e) => {
            if (e.key === "Enter") handleSendMessage();
        });
    }

    // Load Chat history from SQLite
    async function loadAgentChatHistory() {
        if (!activeAgent) return;
        try {
            messagesBody.innerHTML = `
                <div style="text-align:center;padding:24px;color:var(--text-secondary);">
                    <span class="spinner" style="display:inline-block;width:18px;height:18px;
                         border:3px solid rgba(0,0,0,.1);border-top-color:var(--agent-accent, var(--primary));
                         border-radius:50%;animation:spin 0.8s linear infinite;margin-right:8px;"></span>
                    Loading history…
                </div>`;
                
            const resp = await fetch(`/api/agent-chat/history?agent=${activeAgent}&limit=20`);
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

    function appendWelcomeCard() {
        const config = AGENTS_CONFIG[activeAgent];
        const welcomeCard = document.createElement("div");
        welcomeCard.className = "kisanmitra-welcome-card";
        welcomeCard.style.borderColor = "var(--agent-accent-alpha)";
        
        let tpl = AGENT_WELCOME_MESSAGES[activeLang] || AGENT_WELCOME_MESSAGES["en"];
        let msg = tpl.replace("{emoji}", config.emoji)
                     .replace("{name}", config.name)
                     .replace("{desc}", config.description.toLowerCase());

        welcomeCard.innerHTML = `<div style="font-size: 13.5px; line-height: 1.6; color: #333; white-space: pre-line;">${msg}</div>`;
        
        // Append quick actions chips matching selected language
        const chipsGrid = document.createElement("div");
        chipsGrid.className = "quick-actions-grid";
        
        const chips = config.quickQuestions[activeLang] || config.quickQuestions["en"] || [];
        chips.forEach(q => {
            const chip = document.createElement("div");
            chip.className = "quick-action-chip";
            chip.style.background = "var(--agent-bg-light)";
            chip.style.borderColor = "var(--agent-accent-alpha)";
            chip.style.color = "var(--agent-text-color)";
            chip.textContent = q;
            chip.addEventListener("click", () => {
                inputField.value = q;
                handleSendMessage();
            });
            chipsGrid.appendChild(chip);
        });

        welcomeCard.appendChild(chipsGrid);
        messagesBody.appendChild(welcomeCard);
        messagesBody.scrollTop = messagesBody.scrollHeight;
    }

    function appendMessageBubble(role, text) {
        const msgDiv = document.createElement("div");
        msgDiv.className = `chat-msg ${role === 'user' ? 'user' : 'assistant'}`;

        const avatar = document.createElement("div");
        avatar.className = "chat-msg-avatar";
        avatar.style.borderColor = "var(--agent-accent-alpha)";
        if (role === 'user') {
            avatar.textContent = "👨‍🌾";
            avatar.style.background = "var(--agent-text-color)";
        } else {
            avatar.textContent = AGENTS_CONFIG[activeAgent].emoji;
            avatar.style.background = "var(--agent-bg-light)";
        }

        const bubble = document.createElement("div");
        bubble.className = "chat-msg-bubble";
        bubble.style.borderColor = "var(--agent-accent-alpha)";
        if (role === 'user') {
            bubble.style.background = "var(--agent-bg-light)";
            bubble.style.color = "var(--agent-text-color)";
        }
        
        let formattedText = formatMarkdown(text);
        bubble.innerHTML = formattedText;

        // TTS button
        let playBtn = null;
        if (role === 'assistant' && !text.includes("is not configured")) {
            playBtn = document.createElement("button");
            playBtn.className = "tts-play-btn";
            playBtn.style.background = "var(--agent-bg-light)";
            playBtn.style.color = "var(--agent-text-color)";
            playBtn.style.borderColor = "var(--agent-accent-alpha)";
            
            const btnLabel = AGENT_PLAY_LABELS[activeLang] || AGENT_PLAY_LABELS["en"];
            playBtn.innerHTML = btnLabel;
            playBtn.addEventListener("click", () => playVoiceTTS(text, playBtn));
            bubble.appendChild(playBtn);
        }

        msgDiv.appendChild(avatar);
        msgDiv.appendChild(bubble);
        messagesBody.appendChild(msgDiv);
        messagesBody.scrollTop = messagesBody.scrollHeight;

        if (role === 'assistant' && !text.includes("is not configured") && isAutoSpeakEnabled()) {
            autoSpeak(text, playBtn);
        }
    }

    // Speaking variables
    let currentSpeechButton = null;
    let currentSpeechOriginalLabel = "";
    let currentSpeechAudio = null;

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

    function autoSpeak(text, buttonElement) {
        if (!('speechSynthesis' in window)) return;
        stopVoiceTTS();

        const originalLabel = buttonElement ? buttonElement.innerHTML : (AGENT_PLAY_LABELS[activeLang] || "🔊 Play Voice");
        if (buttonElement) {
            currentSpeechButton = buttonElement;
            currentSpeechOriginalLabel = originalLabel;
            buttonElement.innerHTML = AGENT_STOP_LABELS[activeLang] || "🛑 Stop";
            buttonElement.classList.add("speaking");
        }

        const cleanText = text.replace(/\*\*/g, '').replace(/\*/g, '').replace(/•/g, '').replace(/<[^>]+>/g, '');
        const utterance = new SpeechSynthesisUtterance(cleanText);
        const vMap = { en: "en-US", te: "te-IN", hi: "hi-IN", ta: "ta-IN", kn: "kn-IN" };
        const targetLang = vMap[activeLang] || "en-US";
        utterance.lang = targetLang;
        utterance.rate = 0.95;
        const voice = pickBrowserVoice(targetLang);
        if (voice) utterance.voice = voice;

        utterance.onend = () => {
            if (currentSpeechButton === buttonElement) stopVoiceTTS();
        };
        utterance.onerror = () => {
            if (currentSpeechButton === buttonElement) stopVoiceTTS();
        };
        window.speechSynthesis.speak(utterance);
    }

    async function playVoiceTTS(text, buttonElement) {
        if (currentSpeechButton === buttonElement) {
            stopVoiceTTS();
            return;
        }
        stopVoiceTTS();

        const originalLabel = buttonElement.innerHTML;
        currentSpeechButton = buttonElement;
        currentSpeechOriginalLabel = originalLabel;

        buttonElement.innerHTML = AGENT_STOP_LABELS[activeLang] || "🛑 Stop";
        buttonElement.classList.add("speaking");

        const browserOnlyLangs = new Set(["te", "ta", "kn"]);
        if (browserOnlyLangs.has(activeLang)) {
            speakBrowserTTS(text, buttonElement, originalLabel);
            return;
        }

        try {
            const resp = await fetch("/api/agent-chat/tts", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest" },
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
                    if (currentSpeechButton === buttonElement) stopVoiceTTS();
                };
            } else {
                speakBrowserTTS(text, buttonElement, originalLabel);
            }
        } catch (err) {
            speakBrowserTTS(text, buttonElement, originalLabel);
        }
    }

    function pickBrowserVoice(bcp47) {
        const voices = window.speechSynthesis.getVoices();
        const lang = bcp47.toLowerCase();
        const prefix = lang.split("-")[0];

        let match = voices.find(v => v.lang.toLowerCase() === lang);
        if (!match) match = voices.find(v => v.lang.toLowerCase().startsWith(prefix));
        if (!match) match = voices.find(v => v.lang.toLowerCase().includes(prefix));
        return match || null;
    }

    function speakBrowserTTS(text, buttonElement, originalLabel) {
        if (!("speechSynthesis" in window)) {
            stopVoiceTTS();
            return;
        }
        window.speechSynthesis.cancel();
        const cleanText = text.replace(/\*\*/g, "").replace(/\*/g, "").replace(/•/g, "").replace(/<[^>]+>/g, '');

        const voiceLangMap = { en: "en-US", te: "te-IN", hi: "hi-IN", ta: "ta-IN", kn: "kn-IN" };
        const targetLang = voiceLangMap[activeLang] || "en-US";

        const utterance = new SpeechSynthesisUtterance(cleanText);
        utterance.lang = targetLang;
        const voice = pickBrowserVoice(targetLang);
        if (voice) utterance.voice = voice;

        utterance.onend = () => {
            if (currentSpeechButton === buttonElement) stopVoiceTTS();
        };
        utterance.onerror = () => {
            if (currentSpeechButton === buttonElement) stopVoiceTTS();
        };
        window.speechSynthesis.speak(utterance);
    }

    // Thinking Indicator
    let thinkingElement = null;
    function showThinkingIndicator() {
        removeThinkingIndicator();
        
        const loader = document.createElement("div");
        loader.className = "chat-msg assistant";
        loader.id = "agent-loader-bubble";

        const avatar = document.createElement("div");
        avatar.className = "chat-msg-avatar";
        avatar.textContent = AGENTS_CONFIG[activeAgent].emoji;
        avatar.style.background = "var(--agent-bg-light)";
        avatar.style.borderColor = "var(--agent-accent-alpha)";

        const bubble = document.createElement("div");
        bubble.className = "chat-msg-bubble kisanmitra-thinking";
        bubble.style.borderColor = "var(--agent-accent-alpha)";
        
        const label = AGENT_THINKING_LABELS[activeLang] || "Thinking…";

        bubble.innerHTML = `
            <span>${label}</span>
            <div class="thinking-dots">
                <span style="background: var(--agent-accent);"></span>
                <span style="background: var(--agent-accent);"></span>
                <span style="background: var(--agent-accent);"></span>
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
        const oldLoader = document.getElementById("agent-loader-bubble");
        if (oldLoader) oldLoader.remove();
    }

    // Submit handler
    async function handleSendMessage() {
        const text = inputField.value.trim();
        if (!text) return;

        inputField.value = "";
        appendMessageBubble("user", text);
        showThinkingIndicator();

        try {
            const resp = await fetch("/api/agent-chat", {
                method: "POST",
                headers: { "Content-Type": "application/json", "X-Requested-With": "XMLHttpRequest" },
                body: JSON.stringify({
                    agent: activeAgent,
                    message: text,
                    language: activeLang
                })
            });
            const data = await resp.json();
            
            removeThinkingIndicator();

            if (data.success && data.message) {
                appendMessageBubble("assistant", data.message);
            } else {
                appendMessageBubble("assistant", data.message || data.error || "AI service is temporarily unavailable. Please try again.");
            }
        } catch (err) {
            removeThinkingIndicator();
            appendMessageBubble("assistant", "AI service is temporarily unavailable. Please try again.");
        }
    }

    // Speech recognition
    const voiceLangMap = { en: "en-US", te: "te-IN", hi: "hi-IN", ta: "ta-IN", kn: "kn-IN" };
    const listeningLabels = { en: "Listening…", te: "వింటోంది…", hi: "सुन रहा है…", ta: "கேட்கிறது…", kn: "ಕೇಳುತ್ತಿದೆ…" };

    let recognition = null;
    let isListening = false;
    let finalTranscript = "";

    function startVoiceInput() {
        const SpeechRecognition = window.SpeechRecognition || window.webkitSpeechRecognition;
        if (!SpeechRecognition) {
            alert("Voice input is not supported in this browser. Please use Google Chrome.");
            return;
        }

        finalTranscript = "";
        if (inputField) inputField.value = "";

        recognition = new SpeechRecognition();
        recognition.lang = voiceLangMap[activeLang] || "en-US";
        recognition.interimResults = true;
        recognition.maxAlternatives = 1;
        recognition.continuous = false;

        recognition.onstart = () => {
            isListening = true;
            if (micBtn) micBtn.classList.add("mic-active");
            if (voiceStatusBar) {
                document.getElementById("agent-voice-status-text").textContent = listeningLabels[activeLang] || "Listening…";
                voiceStatusBar.classList.add("visible");
            }
            if (inputField) inputField.placeholder = listeningLabels[activeLang] || "Listening…";
        };

        recognition.onresult = (event) => {
            let interimTranscript = "";
            for (let i = event.resultIndex; i < event.results.length; i++) {
                const res = event.results[i];
                if (res.isFinal) {
                    finalTranscript += res[0].transcript;
                } else {
                    interimTranscript += res[0].transcript;
                }
            }
            if (inputField) inputField.value = finalTranscript + interimTranscript;
        };

        recognition.onend = () => {
            isListening = false;
            if (micBtn) micBtn.classList.remove("mic-active");
            if (voiceStatusBar) voiceStatusBar.classList.remove("visible");
            if (inputField) inputField.placeholder = "Ask this agent...";
            if (inputField && inputField.value.trim()) {
                handleSendMessage();
            }
        };

        recognition.onerror = () => {
            isListening = false;
            if (micBtn) micBtn.classList.remove("mic-active");
            if (voiceStatusBar) voiceStatusBar.classList.remove("visible");
            if (inputField) inputField.placeholder = "Ask this agent...";
        };

        recognition.start();
    }

    function stopVoiceInput() {
        if (recognition) recognition.stop();
    }

    if (micBtn) {
        micBtn.addEventListener("click", () => {
            if (isListening) stopVoiceInput();
            else startVoiceInput();
        });
    }

    // Markdown Parser
    function formatMarkdown(text) {
        if (!text) return "";
        let escaped = text
            .replace(/&/g, "&amp;")
            .replace(/</g, "&lt;")
            .replace(/>/g, "&gt;")
            .replace(/"/g, "&quot;")
            .replace(/'/g, "&#039;");

        escaped = escaped.replace(/\*\*(.*?)\*\*/g, "<strong>$1</strong>");

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
});
