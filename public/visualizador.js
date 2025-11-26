(async () => {
  console.log("🧛 INICIANDO CURSOR 'SANGUESSUGA'...");

  const PATHS = { xml: "./public/BWV847_colorido.xml" };

  const ui = {
    playBtn: document.getElementById("btn-play"),
    stopBtn: document.getElementById("btn-stop"),
    bpmSlider: document.getElementById("bpm-slider"),
    bpmValue: document.getElementById("bpm-value"),
    status: document.getElementById("status"),
    legenda: document.getElementById("legenda"),
    container: document.getElementById("osmd-container"),
    cursor: document.getElementById("cursor-manual"),
  };

  let osmd = null;
  let isPlaying = false;
  let audioContextReady = false;
  // Sintetizador (Volume ajustado)
  const synth = new Tone.PolySynth(Tone.Synth, { volume: -10 }).toDestination();

  async function iniciar() {
    try {
      const check = await fetch(PATHS.xml);
      if (!check.ok) throw new Error("XML não encontrado.");

      ui.status.innerHTML = "Carregando...";

      osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(ui.container, {
        backend: "svg",
        drawingParameters: "default",
        autoResize: true,
        drawTitle: false,
        followCursor: true, // Essencial: faz o OSMD calcular a posição interna
      });

      await osmd.load(PATHS.xml);
      await osmd.render();

      ui.status.innerHTML = "(Cursor Sincronizado)";
      ui.status.className = "text-green-600 font-bold text-sm";

      ui.legenda.innerHTML = `
                <div class="flex items-center gap-2"><div style="width:12px;height:12px;background:#DC2626;border-radius:2px;"></div>Sujeito</div>
                <div class="flex items-center gap-2 ml-4"><div style="width:12px;height:12px;background:#2563EB;border-radius:2px;"></div>Contrassujeito</div>
            `;

      // Inicializa o cursor nativo (invisível, mas calcula posições)
      osmd.cursor.show();

      // Posiciona nosso cursor manual pela primeira vez
      sincronizarCursor();
    } catch (e) {
      console.error(e);
      ui.status.innerHTML = `<span class="text-red-600">Erro: ${e.message}</span>`;
    }
  }

  // --- A SOLUÇÃO SANGUESSUGA ---
  function sincronizarCursor() {
    // Tenta pegar o elemento do cursor nativo que o OSMD cria
    const nativeCursor = document.getElementById("cursorImg-0");

    if (nativeCursor) {
      // Rouba as coordenadas dele!
      const top = nativeCursor.style.top;
      const left = nativeCursor.style.left;

      // Só atualiza se o OSMD tiver calculado algo válido
      if (top && left && top !== "0px") {
        ui.cursor.style.top = top;
        ui.cursor.style.left = left;

        // Força dimensões visíveis (ignorando o tamanho do nativo)
        // A altura 0 é o bug comum do OSMD, aqui corrigimos na força
        ui.cursor.style.height = "60px"; // Altura fixa suficiente para cobrir a pauta

        // Ajuste fino vertical se necessário (subir um pouco para centralizar)
        // ui.cursor.style.transform = "translateY(-10px)";

        ui.cursor.style.display = "block";
      }
    }
  }

  // --- PLAYBACK ---
  function tick() {
    if (!isPlaying) return;

    if (osmd.cursor.Iterator.EndReached) {
      stop();
      return;
    }

    // 1. Tocar som
    const iterator = osmd.cursor.Iterator;
    const voices = iterator.CurrentVoiceEntries;

    if (voices) {
      for (let v of voices) {
        for (let note of v.Notes) {
          if (note && !note.isRest() && note.Pitch) {
            synth.triggerAttackRelease(note.Pitch.Frequency, "16n");
          }
        }
      }
    }

    // 2. Mover Cursor
    osmd.cursor.next(); // Manda o OSMD calcular a próxima posição interna
    sincronizarCursor(); // Atualiza nosso cursor visual baseado na conta do OSMD

    // 3. Loop
    const bpm = parseInt(ui.bpmSlider.value);
    const stepTime = (60 / bpm) * 1000 * 0.25; // Semicolcheias

    setTimeout(tick, stepTime);
  }

  // --- CONTROLES ---
  ui.playBtn.addEventListener("click", async () => {
    if (!audioContextReady) {
      await Tone.start();
      audioContextReady = true;
    }

    if (isPlaying) {
      isPlaying = false;
      ui.playBtn.innerHTML =
        '<span id="icon-play">▶</span> <span id="text-play">Continuar</span>';
      ui.playBtn.className =
        "bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg shadow transition flex items-center gap-2";
    } else {
      isPlaying = true;
      ui.playBtn.innerHTML =
        '<span id="icon-play">⏸</span> <span id="text-play">Pause</span>';
      ui.playBtn.className =
        "bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-6 rounded-lg shadow transition flex items-center gap-2";

      if (osmd.cursor.Iterator.EndReached) osmd.cursor.reset();

      osmd.cursor.show();
      sincronizarCursor();
      tick();
    }
  });

  ui.stopBtn.addEventListener("click", stop);

  function stop() {
    isPlaying = false;
    ui.playBtn.innerHTML =
      '<span id="icon-play">▶</span> <span id="text-play">Play</span>';
    ui.playBtn.className =
      "bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow transition flex items-center gap-2";
    if (osmd) {
      osmd.cursor.reset();
      sincronizarCursor();
      // ui.cursor.style.display = 'none'; // Opcional: esconder ao parar
    }
  }

  ui.bpmSlider.addEventListener(
    "input",
    (e) => (ui.bpmValue.innerText = e.target.value)
  );

  iniciar();
})();
