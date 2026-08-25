/**
 * Settings Page Interactions
 * Syncs user voice preferences to localStorage.
 */

document.addEventListener("DOMContentLoaded", () => {
    const autoPlayVoiceChk = document.getElementById("auto-play-voice-chk");
    const AUTOSPEAK_KEY = "kisanmitra_autospeak";

    if (autoPlayVoiceChk) {
        // Sync local storage setting on toggle change
        autoPlayVoiceChk.addEventListener("change", () => {
            localStorage.setItem(AUTOSPEAK_KEY, autoPlayVoiceChk.checked ? "1" : "0");
        });
    }
});
