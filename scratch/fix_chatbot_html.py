import sys
import os

filepath = "c:/Users/kooki/Desktop/Farm/templates/chatbot.html"

with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

# Let's find where the send btn line is:
send_btn_line = -1
for i, line in enumerate(lines):
    if 'id="page-send-btn"' in line:
        send_btn_line = i
        break

# The </div> for kisanmitra-input-row is immediately after it (usually 1 or 2 lines)
input_row_end = -1
for i in range(send_btn_line + 1, len(lines)):
    if '</div>' in lines[i]:
        input_row_end = i
        break

DOMContentLoaded_idx = -1
for i, line in enumerate(lines):
    if 'document.addEventListener("DOMContentLoaded"' in line:
        DOMContentLoaded_idx = i
        break

print(f"send_btn_line: {send_btn_line}, input_row_end: {input_row_end}, DOMContentLoaded: {DOMContentLoaded_idx}")

# Using raw string (r""") so backslashes for \n remain as backslash+n
correct_middle = r"""          </div>

        </div>

      </div>

    </div>

  </div>
</div>
{% endblock %}

{% block scripts %}
<script>
  // Simple quick actions configuration
  const PAGE_QUICK_ACTIONS = {
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
          { label: "🧠 आज की योजना", query: "??वर्तमान कृषि योजना सारांश स्पष्ट करें।" },
          { label: "📊 सिफारिशें समझाएं", query: "क्या आप मेरी सक्रिय सिफारिशों को समझा सकते हैं?" }
      ],
      ta: [
          { label: "🌱 என் மண் பரிசோதனை", query: "என் மண்ணின் அளவீடுகளை பகுப்பாய்வு செய்ய முடியுமா?" },
          { label: "💧 நீர் பாய்ச்ச வேண்டுமா?", query: "நான் இன்று பயிருக்கு நீர் பாய்ச்ச வேண்டுமா?" },
          { label: "🌾 பயிர் ஆரோக்கியம்", query: "என் பயிரின் ஆரோக்கிய நிலை என்ன?" },
          { label: "☀️ பண்ணை வானிலை", query: "என் பண்ணையின் தற்போதைய வெப்பநிலை மற்றும் வானிலை சுருக்கத்தை கூறுங்கள்." },
          { label: "📋 இன்றைய திட்டம்", query: "தற்போதைய பண்ணை திட்டமிடல் சுருக்கத்தை விளக்குங்கள்." },
          { label: "📊 பரிந்துரைகளின் விளக்கம்", query: "என் செயலில் உள்ள பரிந்துரைகளை விளக்க முடியுமா?" }
      ],
      kn: [
          { label: "🌱 ಮಣ್ಣಿನ ಪರೀಕ್ಷೆ", query: "ನನ್ನ ಮಣ್ಣಿನ ಅಳತೆಗಳನ್ನು ವಿಶ್ಲೇಷಿಸಬಹುದೇ?" },
          { label: "💧 ನೀರುಣಿಸಬೇಕೇ?", query: "ನಾನು ಇಂದು ಬೆಳೆಗೆ ನೀರುಣಿಸಬೇಕೇ?" },
          { label: "🌾 ಬೆಳೆ ಆರೋಗ್ಯ", query: "ನನ್ನ ಬೆಳೆಯ ಆರೋಗ್ಯ ಸ್ಥಿತಿ ಹೇಗಿದೆ?" },
          { label: "☀️ ಹವಾಮಾನ ಪರಿಸ್ಥಿತಿ", query: "ನನ್ನ ತೋಟದ ಪ್ರಸ್ತುತ ತಾಪಮಾನ ಮತ್ತು ಹವಾಮಾನದ ಸಾರಾಂಶವೇನು?" },
          { label: "📋 ಇಂದಿನ ಕೃಷಿ ಯೋಜನೆ", query: "ಪ್ರಸ್ತುತ ಕೃಷಿ ಯೋಜನೆ ಸಾರಾಂಶವನ್ನು ವಿವರಿಸಿ." },
          { label: "📊 ಶಿಫારಸುಗಳನ್ನು ವಿವರಿಸಿ", query: "ನನ್ನ ಸಕ್ರಿಯ ಶಿಫಾರಸುಗಳನ್ನು ವಿವರಿಸಬಹುದೇ?" }
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

  const PAGE_WELCOME_MESSAGES = {
      en: "Hello, I'm KisanMitra AI. Your intelligent farm companion. I can help you understand:\n\n• Your soil\n• Crop health\n• Irrigation\n• Fertilizer needs\n• Farm recommendations\n• AI agent results\n• Farm planning\n\nAsk me anything about your farm.",
      te: "నమస్కారం, నేను కిసాన్ మిత్ర AI. మీ తెలివైన వ్యవసాయ సహచరుడిని. వీటిని అర్థం చేసుకోవడంలో నేను మీకు సహాయపడగలను:\n\n• మీ మట్టి\n• పంట ఆరోగ్యం\n• నీటి పారుదల\n• ఎరువుల అవసరాలు\n• వ్యవసాయ సిఫార్సులు\n• AI ఏజెంట్ ఫలితాలు\n• వ్యవసాయ ప్రణాళిక\n\nమీ వ్యవసాయం గురించి నన్ను ఏదైనా అడగండి.",
      hi: "नमस्ते, मैं किसानमित्र AI हूँ। आपका बुद्धिमान कृषि साथी। मैं आपको समझने में मदद कर सकता हूँ:\n\n• आपकी मिट्टी\n• फसल का स्वास्थ्य\n• सिंचाई की आवश्यकताएं\n• उर्वरक की आवश्यकता\n• खेत की सिफारिशें\n• एआई एजेंट के परिणाम\n• कृषि योजना\n\nअपने खेत के बारे में मुझसे कुछ भी पूछें।",
      ta: "வணக்கம், நான் கிசான்மித்ரா AI. உங்கள் புத்திசாலித்தனமான பண்ணை கூட்டாளி. இவற்றை நீங்கள் புரிந்து கொள்ள நான் உதவ முடியும்:\n\n• உங்கள் மண்\n• பயிர் ஆரோக்கியம்\n• நீர் பாசனம்\n• உரத் தேவைகள்\n• பண்ணை பரிந்துரைகள்\n• AI ஏஜென்ட் முடிவுகள்\n• பண்ணை திட்டமிடல்\n\nஉங்கள் பண்ணை பற்றி என்னிடம் எது வேண்டுமானாலும் கேளுங்கள்.",
      kn: "ನಮಸ್ಕಾರ, ನಾನು ಕಿಸಾನ್ ಮಿತ್ರ AI. ನಿಮ್ಮ ಬುದ್ಧಿವಂತ ಕೃಷಿ ಸಂಗಾತಿ. ಈ ಕೆಳಗಿನವುಗಳನ್ನು ಅರ್ಥಮಾಡಿಕೊಳ್ಳಲು ನಾನು ನಿಮಗೆ ಸಹಾಯ ಮಾಡಬಲ್ಲೆ:\n\n• ನಿಮ್ಮ ಮಣ್ಣು\n• ಬೆಳೆ ಆರೋಗ್ಯ\n• ನೀರಾವರಿ\n• ರಸಗೊಬ್ಬರ ಅಗತ್ಯಗಳು\n• ತೋಟದ ಶಿಫಾರಸುಗಳು\n• ಎಐ ಏಜೆಂಟ್ ಫಲಿತಾಂಶಗಳು\n• ಕೃಷಿ ಯೋಜನೆ\n\nನಿಮ್ಮ ತೋಟದ ಬಗ್ಗೆ ನನ್ನನ್ನು ಏನಾದರೂ ಕೇಳಿ.",
      ja: "こんにちは、KisanMitra AIです。あなたのインテリジェントな農場アシスタント。以下についてお手伝いできます:\n\n• 土壌分析\n• 作物の健康\n• 灌漑\n• 肥料のニーズ\n• 農場の推奨事項\n• AIエージェントの結果\n• 農場計画\n\n農場について何でも聞いてください。",
      ko: "안녕하세요, 저는 KisanMitra AI입니다. 당신의 지능형 농장 도우미입니다. 다음 사항에 도움을 드릴 수 있습니다:\n\n• 토양 분석\n• 작물 건강\n• 관개\n• 비료 필요량\n• 농장 추천 사항\n• AI 에이전트 결과\n• 농장 계획\n\n농장에 대해 무엇이든 물어보세요."
  };

  const PAGE_PLAY_LABELS = {
      en: "🔊 Play Voice",
      te: "🔊 వినిపించు",
      hi: "🔊 आवाज सुनाएं",
      ta: "🔊 ஒலிபரப்பு",
      kn: "🔊 ಧ್ವನಿ ಪ್ಲೇ",
      ja: "🔊 音声再生",
      ko: "🔊 음성 재생"
  };
"""

# Reconstruct file
new_lines = lines[:input_row_end + 1] + [correct_middle] + lines[DOMContentLoaded_idx:]

with open(filepath, "w", encoding="utf-8") as f:
    f.writelines(new_lines)

print("HTML script successfully repaired with RAW string.")
