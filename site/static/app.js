(() => {
  const copy = {
    ru: {
      eyebrow: "БЫСТРЫЙ ГЕНЕРАТОР КОДОВ КОМАНДЫ",
      titleA: "БОЛЬШЕ",
      titleB: "ВАРИАНТОВ.",
      heroCopy: "Вставь код команды или ссылку-приглашение. Получи 10 ссылок со смещением — и сразу зови друзей.",
      stamp: "КОМАНДА<br>ГОТОВА",
      generatorTitle: "СОБЕРИ СВОИ ССЫЛКИ",
      barNote: "БЫСТРО · БЕЗ ЛИШНЕГО",
      inputLabel: "Код команды или ссылка-приглашение",
      inputPlaceholder: "Например: XQWERTY или ссылка приглашения",
      paste: "Вставить",
      pasteError: "Не удалось прочитать буфер обмена. Вставь код вручную.",
      offsetLabel: "Смещение",
      offsetHint: "между исходным и первым кодом",
      offsetAria: "Смещение",
      customOffset: "Другое",
      generate: "Сгенерировать 10 ссылок",
      generating: "Считаем коды",
      resultsKicker: "ТВОЙ НАБОР",
      resultsTitle: "ГОТОВЫЕ ССЫЛКИ",
      resultsMeta: "10 ссылок появятся здесь",
      loadingMeta: "Готовим 10 ссылок…",
      copyAll: "Скопировать все",
      emptyTitle: "Тут будет твой набор",
      emptyCopy: "Введи код выше — и ссылки появятся сразу после генерации.",
      noteLead: "Важно:",
      noteText: "коды и ссылки рассчитываются автоматически. Активность игровых комнат не проверяется.",
      footerNote: "Неофициальный инструмент для игроков Brawl Stars",
      soundOn: "Звук вкл.",
      soundOff: "Звук выкл.",
      soundEnable: "Включить звук",
      soundDisable: "Выключить звук",
      soundGroup: "Язык",
      copyCode: "Скопировать код команды",
      copyInvite: "Скопировать ссылку приглашения",
      openGame: "Открыть в игре",
      openGameAria: "Открыть приглашение {code} в игре",
      offsetMeta: "База {base} · смещение {offset} · 10 ссылок",
      generated: "Готово: создано 10 ссылок.",
      copiedCode: "Код команды {code} скопирован.",
      copiedInvite: "Ссылка приглашения {code} скопирована.",
      copiedAll: "Все 10 ссылок скопированы.",
      clipboardError: "Не удалось скопировать. Проверь разрешения браузера.",
      invalidOffset: "Смещение должно быть целым числом от 0 до 10000.",
      retry: "Повторить",
      networkError: "Не удалось связаться с генератором. Попробуй ещё раз.",
      copyFailure: "Не удалось скопировать ссылку."
    },
    en: {
      eyebrow: "QUICK TEAM CODE GENERATOR",
      titleA: "MORE",
      titleB: "WAYS IN.",
      heroCopy: "Paste a team code or invite link. Get 10 offset invite links, then bring your crew straight in.",
      stamp: "SQUAD<br>READY",
      generatorTitle: "BUILD YOUR INVITE SET",
      barNote: "FAST · NO FUSS",
      inputLabel: "Team code or invite link",
      inputPlaceholder: "For example: XQWERTY or an invite link",
      paste: "Paste",
      pasteError: "Clipboard access failed. Paste your code into the field.",
      offsetLabel: "Offset",
      offsetHint: "between the original and first code",
      offsetAria: "Offset",
      customOffset: "Custom",
      generate: "Generate 10 invite links",
      generating: "Calculating codes",
      resultsKicker: "YOUR SET",
      resultsTitle: "INVITE LINKS",
      resultsMeta: "Your 10 links will show up here",
      loadingMeta: "Preparing 10 invite links…",
      copyAll: "Copy all",
      emptyTitle: "Your set will land here",
      emptyCopy: "Enter a code above and your invite links will appear as soon as they are ready.",
      noteLead: "Heads up:",
      noteText: "codes and links are calculated automatically. Active game rooms are not checked.",
      footerNote: "An unofficial tool for Brawl Stars players",
      soundOn: "Sound on",
      soundOff: "Sound off",
      soundEnable: "Enable sound",
      soundDisable: "Disable sound",
      soundGroup: "Language",
      copyCode: "Copy team code",
      copyInvite: "Copy invite link",
      openGame: "Open in game",
      openGameAria: "Open invite {code} in game",
      offsetMeta: "Base {base} · offset {offset} · 10 links",
      generated: "Done: 10 invite links are ready.",
      copiedCode: "Team code {code} copied.",
      copiedInvite: "Invite link for {code} copied.",
      copiedAll: "All 10 invite links copied.",
      clipboardError: "Could not copy. Check your browser permissions.",
      invalidOffset: "Offset must be a whole number from 0 to 10000.",
      retry: "Try again",
      networkError: "Could not reach the generator. Please try again.",
      copyFailure: "Could not copy the invite link."
    }
  };

  const form = document.getElementById("generator-form");
  const input = document.getElementById("team-input");
  const customOffset = document.getElementById("custom-offset");
  const generateButton = document.getElementById("generate-button");
  const generateLabel = document.getElementById("generate-label");
  const feedback = document.getElementById("feedback");
  const resultList = document.getElementById("result-list");
  const resultPlaceholder = document.getElementById("result-placeholder");
  const resultsMeta = document.getElementById("results-meta");
  const copyAllButton = document.getElementById("copy-all");
  const pasteButton = document.getElementById("paste-button");
  const soundToggle = document.getElementById("sound-toggle");
  const soundLabel = document.getElementById("sound-label");
  const languageButtons = [...document.querySelectorAll("[data-language]")];
  const offsetButtons = [...document.querySelectorAll("[data-offset]")];
  let language = "ru";
  let generatedResults = [];
  let soundsEnabled = false;
  let audioContext = null;
  let isGenerating = false;

  const tr = (key, values = {}) => {
    let text = copy[language][key] || key;
    Object.entries(values).forEach(([name, value]) => {
      text = text.replaceAll(`{${name}}`, String(value));
    });
    return text;
  };

  function setLanguage(nextLanguage) {
    language = nextLanguage === "en" ? "en" : "ru";
    document.documentElement.lang = language;
    document.title = language === "ru" ? "Team Code Lab — Brawl Stars" : "Team Code Lab — Brawl Stars";
    document.querySelectorAll("[data-i18n]").forEach((element) => {
      const key = element.dataset.i18n;
      if (copy[language][key]) element.innerHTML = copy[language][key];
    });
    input.placeholder = tr("inputPlaceholder");
    customOffset.placeholder = tr("customOffset");
    customOffset.setAttribute("aria-label", tr("customOffset"));
    document.querySelector(".language-switch").setAttribute("aria-label", tr("soundGroup"));
    document.querySelector(".offset-options").setAttribute("aria-label", tr("offsetAria"));
    generateLabel.textContent = isGenerating ? tr("generating") : tr("generate");
    if (isGenerating) resultsMeta.textContent = tr("loadingMeta");
    languageButtons.forEach((button) => {
      button.setAttribute("aria-pressed", String(button.dataset.language === language));
    });
    updateSoundControl();
    if (generatedResults.length) renderResults(generatedResults, generatedResults.baseCode, generatedResults.offset);
  }

  function updateSoundControl() {
    const soundText = soundsEnabled ? tr("soundOn") : tr("soundOff");
    soundLabel.textContent = soundText;
    soundToggle.setAttribute("aria-pressed", String(soundsEnabled));
    soundToggle.setAttribute("aria-label", soundsEnabled ? tr("soundDisable") : tr("soundEnable"));
    soundToggle.title = soundsEnabled ? tr("soundDisable") : tr("soundEnable");
    const icon = soundToggle.querySelector("svg");
    icon.innerHTML = soundsEnabled
      ? '<path d="M11 5 6 9H3v6h3l5 4V5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M16 9a5 5 0 0 1 0 6M19 6a9 9 0 0 1 0 12" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>'
      : '<path d="M11 5 6 9H3v6h3l5 4V5Z" stroke="currentColor" stroke-width="1.7" stroke-linejoin="round"/><path d="M16 9a5 5 0 0 1 0 6" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/><path d="m17 4 4 4m0-4-4 4" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/>';
  }

  function playTone(kind = "success") {
    if (!soundsEnabled || !audioContext) return;
    const now = audioContext.currentTime;
    const oscillator = audioContext.createOscillator();
    const gain = audioContext.createGain();
    oscillator.type = "triangle";
    oscillator.frequency.setValueAtTime(kind === "error" ? 185 : 520, now);
    oscillator.frequency.exponentialRampToValueAtTime(kind === "error" ? 130 : 760, now + 0.085);
    gain.gain.setValueAtTime(0.0001, now);
    gain.gain.exponentialRampToValueAtTime(0.045, now + 0.012);
    gain.gain.exponentialRampToValueAtTime(0.0001, now + 0.12);
    oscillator.connect(gain);
    gain.connect(audioContext.destination);
    oscillator.start(now);
    oscillator.stop(now + 0.13);
  }

  function showFeedback(message, kind = "success", retryable = false) {
    feedback.replaceChildren();
    const block = document.createElement("div");
    block.className = `feedback-message ${kind}`;
    const icon = document.createElementNS("http://www.w3.org/2000/svg", "svg");
    icon.setAttribute("viewBox", "0 0 24 24");
    icon.setAttribute("fill", "none");
    icon.setAttribute("aria-hidden", "true");
    icon.innerHTML = kind === "error"
      ? '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7"/><path d="m9 9 6 6m0-6-6 6" stroke="currentColor" stroke-width="1.8" stroke-linecap="round"/>'
      : '<circle cx="12" cy="12" r="9" stroke="currentColor" stroke-width="1.7"/><path d="m8 12 2.5 2.5L16 9" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/>';
    const text = document.createElement("span");
    text.textContent = message;
    block.append(icon, text);
    if (retryable) {
      const retry = document.createElement("button");
      retry.className = "retry-button";
      retry.type = "button";
      retry.textContent = tr("retry");
      retry.addEventListener("click", () => form.requestSubmit());
      block.append(retry);
    }
    feedback.append(block);
  }

  function clearFeedback() {
    feedback.replaceChildren();
  }

  function currentOffset() {
    if (!customOffset.value.trim()) {
      return Number(offsetButtons.find((button) => button.getAttribute("aria-pressed") === "true")?.dataset.offset ?? 50);
    }
    const value = customOffset.value.trim();
    if (!/^\d+$/.test(value)) return null;
    const parsed = Number(value);
    return Number.isSafeInteger(parsed) && parsed >= 0 && parsed <= 10000 ? parsed : null;
  }

  function clearResults() {
    generatedResults = [];
    resultList.replaceChildren();
    resultPlaceholder.hidden = false;
    copyAllButton.disabled = true;
    resultsMeta.textContent = tr("resultsMeta");
  }

  function showLoadingResults() {
    resultPlaceholder.hidden = true;
    resultList.replaceChildren();
    resultsMeta.textContent = tr("loadingMeta");
    for (let index = 0; index < 10; index += 1) {
      const skeleton = document.createElement("div");
      skeleton.className = "skeleton-row";
      skeleton.setAttribute("aria-hidden", "true");
      skeleton.innerHTML = '<span class="skeleton-number"></span><span class="skeleton-copy"><i></i><i></i></span><span class="skeleton-action"></span>';
      resultList.append(skeleton);
    }
  }

  function renderResults(results, baseCode, offset) {
    generatedResults = results;
    generatedResults.baseCode = baseCode;
    generatedResults.offset = offset;
    resultList.replaceChildren();
    resultPlaceholder.hidden = true;
    resultsMeta.textContent = tr("offsetMeta", { base: baseCode, offset });
    copyAllButton.disabled = results.length === 0;
    results.forEach((result, position) => {
      const row = document.createElement("article");
      row.className = "result-row";
      row.style.animationDelay = `${Math.min(position * 20, 180)}ms`;
      row.innerHTML = `
        <span class="result-number"></span>
        <div class="result-codes"><span class="team-code"></span><span class="hash-code"></span></div>
         <div class="result-actions">
           <button class="icon-action copy-code" type="button">
             <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><rect x="8" y="8" width="13" height="13" rx="2" stroke="currentColor" stroke-width="1.7"/><path d="M16 8V5a2 2 0 0 0-2-2H5a2 2 0 0 0-2 2v9a2 2 0 0 0 2 2h3" stroke="currentColor" stroke-width="1.7"/></svg>
           </button>
           <button class="icon-action copy-invite" type="button">
             <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M10 13.5a4 4 0 0 0 5.8.2l3-3a4 4 0 0 0-5.7-5.7l-1.7 1.7M14 10.5a4 4 0 0 0-5.8-.2l-3 3a4 4 0 0 0 5.7 5.7l1.7-1.7" stroke="currentColor" stroke-width="1.8" stroke-linecap="round" stroke-linejoin="round"/></svg>
           </button>
          <a class="open-action" rel="noopener" target="_blank">
            <span></span>
            <svg viewBox="0 0 24 24" fill="none" aria-hidden="true"><path d="M14 4h6v6m0-6-9 9" stroke="currentColor" stroke-width="1.7" stroke-linecap="round" stroke-linejoin="round"/><path d="M18 13v5a2 2 0 0 1-2 2H6a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h5" stroke="currentColor" stroke-width="1.7" stroke-linecap="round"/></svg>
          </a>
        </div>`;
      row.querySelector(".result-number").textContent = String(result.index).padStart(2, "0");
      row.querySelector(".team-code").textContent = result.teamCode;
      row.querySelector(".hash-code").textContent = result.hashCode;
       const copyCodeButton = row.querySelector(".copy-code");
       copyCodeButton.setAttribute("aria-label", tr("copyCode"));
       copyCodeButton.title = tr("copyCode");
       copyCodeButton.addEventListener("click", async () => {
         const ok = await writeClipboard(result.teamCode);
         showFeedback(ok ? tr("copiedCode", { code: result.teamCode }) : tr("copyFailure"), ok ? "success" : "error");
         if (ok) playTone();
       });
       const copyInviteButton = row.querySelector(".copy-invite");
       copyInviteButton.setAttribute("aria-label", tr("copyInvite"));
       copyInviteButton.title = tr("copyInvite");
       copyInviteButton.addEventListener("click", async () => {
         const ok = await writeClipboard(result.inviteUrl);
         showFeedback(ok ? tr("copiedInvite", { code: result.teamCode }) : tr("copyFailure"), ok ? "success" : "error");
         if (ok) playTone();
       });
      const openLink = row.querySelector(".open-action");
      openLink.href = result.inviteUrl;
      openLink.setAttribute("aria-label", tr("openGameAria", { code: result.teamCode }));
      openLink.title = tr("openGameAria", { code: result.teamCode });
      openLink.querySelector("span").textContent = tr("openGame");
      resultList.append(row);
    });
  }

  async function writeClipboard(text) {
    try {
      if (navigator.clipboard && window.isSecureContext) {
        await navigator.clipboard.writeText(text);
        return true;
      }
      const temporary = document.createElement("textarea");
      temporary.value = text;
      temporary.setAttribute("readonly", "");
      temporary.style.position = "fixed";
      temporary.style.opacity = "0";
      document.body.append(temporary);
      temporary.select();
      const ok = document.execCommand("copy");
      temporary.remove();
      return ok;
    } catch {
      return false;
    }
  }

  offsetButtons.forEach((button) => {
    button.addEventListener("click", () => {
      offsetButtons.forEach((item) => item.setAttribute("aria-pressed", String(item === button)));
      customOffset.value = "";
      clearFeedback();
    });
  });

  customOffset.addEventListener("input", () => {
    if (customOffset.value) offsetButtons.forEach((item) => item.setAttribute("aria-pressed", "false"));
    clearFeedback();
  });

  languageButtons.forEach((button) => {
    button.addEventListener("click", () => setLanguage(button.dataset.language));
  });

  pasteButton.addEventListener("click", async () => {
    try {
      if (!navigator.clipboard?.readText) throw new Error("Clipboard unavailable");
      const value = await navigator.clipboard.readText();
      if (!value) {
        showFeedback(tr("pasteError"), "error");
        return;
      }
      input.value = value.trim();
      input.focus();
      clearFeedback();
    } catch {
      showFeedback(tr("pasteError"), "error");
    }
  });

  soundToggle.addEventListener("click", async () => {
    soundsEnabled = !soundsEnabled;
    if (soundsEnabled) {
      const AudioContextClass = window.AudioContext || window.webkitAudioContext;
      if (!AudioContextClass) {
        soundsEnabled = false;
        return;
      }
      try {
        audioContext = audioContext || new AudioContextClass();
        if (audioContext.state === "suspended") await audioContext.resume();
      } catch {
        soundsEnabled = false;
      }
    }
    updateSoundControl();
    if (soundsEnabled) playTone();
  });

  copyAllButton.addEventListener("click", async () => {
    if (!generatedResults.length) return;
    const ok = await writeClipboard(generatedResults.map((result) => result.inviteUrl).join("\n"));
    showFeedback(ok ? tr("copiedAll") : tr("clipboardError"), ok ? "success" : "error");
    if (ok) playTone();
  });

  form.addEventListener("submit", async (event) => {
    event.preventDefault();
    clearFeedback();
    const offset = currentOffset();
    if (offset === null) {
      showFeedback(tr("invalidOffset"), "error");
      customOffset.focus();
      playTone("error");
      return;
    }
    const requestLanguage = language;
    isGenerating = true;
    generateButton.disabled = true;
    generateButton.classList.add("is-loading");
    generateLabel.textContent = tr("generating");
    generateButton.setAttribute("aria-busy", "true");
    clearResults();
    showLoadingResults();
    try {
      const response = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          teamCodeOrLink: input.value,
          offset,
          language: requestLanguage
        })
      });
      let payload;
      try {
        payload = await response.json();
      } catch {
        payload = {};
      }
      if (!response.ok) {
        clearResults();
        showFeedback(payload.error || copy[requestLanguage].networkError, "error", response.status >= 500);
        playTone("error");
        return;
      }
      renderResults(payload.results || [], payload.baseCode, payload.offset);
      showFeedback(tr("generated"), "success");
      playTone();
      const reducedMotion = window.matchMedia("(prefers-reduced-motion: reduce)").matches;
      document.getElementById("results-title").scrollIntoView({
        behavior: reducedMotion ? "auto" : "smooth",
        block: "nearest"
      });
    } catch {
      clearResults();
      showFeedback(tr("networkError"), "error", true);
      playTone("error");
    } finally {
      isGenerating = false;
      generateButton.disabled = false;
      generateButton.classList.remove("is-loading");
      generateButton.removeAttribute("aria-busy");
      generateLabel.textContent = tr("generate");
    }
  });

  setLanguage("ru");
})();
