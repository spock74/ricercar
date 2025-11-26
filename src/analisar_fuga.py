(async () => {
    console.log("LUZES, CÂMERA, CURSOR!");

    const PATHS = { xml: './public/BWV847_colorido.xml' };
    
    const ui = {
        playBtn: document.getElementById('btn-play'),
        stopBtn: document.getElementById('btn-stop'),
        bpmSlider: document.getElementById('bpm-slider'),
        bpmValue: document.getElementById('bpm-value'),
        status: document.getElementById('status'),
        legenda: document.getElementById('legenda'),
        container: document.getElementById('osmd-container')
    };

    let osmd = null;
    let isPlaying = false;
    let audioContextReady = false;
    // Sintetizador com volume mais baixo para não assustar
    const synth = new Tone.PolySynth(Tone.Synth, { volume: -10 }).toDestination();

    async function iniciar() {
        try {
            const check = await fetch(PATHS.xml);
            if(!check.ok) throw new Error("XML não encontrado.");

            ui.status.innerHTML = "Carregando...";

            // CONFIGURAÇÃO DO OSMD
            osmd = new opensheetmusicdisplay.OpenSheetMusicDisplay(ui.container, {
                backend: 'svg', 
                // REMOVIDO 'compacttight' -> Isso expande a partitura e dá espaço pro cursor
                drawingParameters: 'default', 
                autoResize: true,
                drawTitle: false,
                followCursor: true, 
            });

            await osmd.load(PATHS.xml);
            await osmd.render();

            ui.status.innerHTML = "Pronto (Cursor Forçado)";
            ui.status.className = "text-green-600 font-bold text-sm";
            
            ui.legenda.innerHTML = `
                <div class="flex items-center gap-2"><div style="width:12px;height:12px;background:#DC2626;border-radius:2px;"></div>Sujeito</div>
                <div class="flex items-center gap-2 ml-4"><div style="width:12px;height:12px;background:#2563EB;border-radius:2px;"></div>Contrassujeito</div>
            `;

            // Inicializa cursor
            osmd.cursor.show();
            osmd.cursor.reset();

        } catch (e) {
            console.error(e);
            ui.status.innerHTML = `<span class="text-red-600">Erro: ${e.message}</span>`;
        }
    }

    // --- Lógica de Playback ---
    function tick() {
        if (!isPlaying || !osmd.cursor) return;

        if (osmd.cursor.Iterator.EndReached) {
            stop();
            return;
        }

        const iterator = osmd.cursor.Iterator;
        const voices = iterator.CurrentVoiceEntries;
        
        // Toca as notas que o cursor está passando por cima agora
        if(voices) {
            for(let v of voices) {
                for(let note of v.Notes) {
                    if(note && !note.isRest() && note.Pitch) {
                        // Duração curta para não embolar
                        synth.triggerAttackRelease(note.Pitch.Frequency, "16n");
                    }
                }
            }
        }

        // Avança o cursor
        osmd.cursor.next();
        
        // Calcula tempo para o próximo passo
        const bpm = parseInt(ui.bpmSlider.value);
        // Avança em semicolcheias (4 passos por batida) para ficar fluido
        const stepTime = (60 / bpm) * 1000 * 0.25; 

        setTimeout(tick, stepTime);
    }

    // --- Controles ---
    ui.playBtn.addEventListener('click', async () => {
        if(!audioContextReady) { await Tone.start(); audioContextReady = true; }
        
        if(isPlaying) {
            // Pause
            isPlaying = false;
            ui.playBtn.innerHTML = '<span id="icon-play">▶</span> <span id="text-play">Continuar</span>';
            ui.playBtn.className = "bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-6 rounded-lg shadow transition flex items-center gap-2";
        } else { 
            // Play
            isPlaying = true; 
            ui.playBtn.innerHTML = '<span id="icon-play">⏸</span> <span id="text-play">Pause</span>';
            ui.playBtn.className = "bg-yellow-500 hover:bg-yellow-600 text-white font-bold py-2 px-6 rounded-lg shadow transition flex items-center gap-2";
            
            // Garante que o cursor aparece ao dar play
            osmd.cursor.show();
            tick(); 
        }
    });

    ui.stopBtn.addEventListener('click', stop);

    function stop() {
        isPlaying = false;
        ui.playBtn.innerHTML = '<span id="icon-play">▶</span> <span id="text-play">Play</span>';
        ui.playBtn.className = "bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-6 rounded-lg shadow transition flex items-center gap-2";
        if(osmd) { 
            osmd.cursor.reset(); 
            osmd.cursor.show(); 
        }
    }

    ui.bpmSlider.addEventListener('input', (e) => ui.bpmValue.innerText = e.target.value);

    iniciar();
})();