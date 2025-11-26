import music21.converter
from music21 import interval, note
import os

# --- CORES ---
COR_SUJEITO = '#DC2626'       # Vermelho
COR_CONTRASSUJEITO = '#2563EB' # Azul

# --- PADRÕES ---
# Sujeito (C -> B -> C -> G): Desce m2, Sobe m2, Desce P4
sujeito_padrao = ['m-2', 'm2', 'P-4']

# Contrassujeito simplificado
contrassujeito_padrao = ['M2', 'P-5'] 

def analisar_e_pintar():
    # Define caminhos robustos
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    xml_input = os.path.join(base_dir, 'public', 'BWV847.xml')
    xml_output = os.path.join(base_dir, 'public', 'BWV847_colorido.xml')

    print(f"--- Iniciando Análise Morfológica ---")
    
    # Verifica se o arquivo de entrada existe antes de tentar abrir
    if not os.path.exists(xml_input):
        print(f"ERRO: Arquivo de entrada não encontrado: {xml_input}")
        # Tenta listar o diretório para debug na Vercel
        print(f"Conteúdo de public/: {os.listdir(os.path.join(base_dir, 'public'))}")
        return

    try:
        score = music21.converter.parse(xml_input)
    except Exception as e:
        print(f"ERRO CRÍTICO ao ler XML: {e}")
        return

    total_pintadas = 0

    for part in score.parts:
        print(f"Analisando voz: {part.partName or 'Sem Nome'}")
        
        # Pega todas as notas
        notas = [n for n in part.flat.notes if isinstance(n, note.Note)]
        
        # Calcula intervalos DIRECIONADOS
        intervalos = []
        for i in range(len(notas) - 1):
            try:
                inv = interval.Interval(noteStart=notas[i], noteEnd=notas[i+1])
                intervalos.append(inv.directedName)
            except:
                intervalos.append("X")
        
        # Busca Padrões
        for i in range(len(intervalos)):
            # 1. Sujeito
            fatia = intervalos[i : i + len(sujeito_padrao)]
            if fatia == sujeito_padrao:
                for k in range(len(sujeito_padrao) + 1):
                    notas[i+k].style.color = COR_SUJEITO
                    total_pintadas += 1

            # 2. Contrassujeito
            fatia_c = intervalos[i : i + len(contrassujeito_padrao)]
            if fatia_c == contrassujeito_padrao:
                if not notas[i].style.color:
                    for k in range(len(contrassujeito_padrao) + 1):
                        notas[i+k].style.color = COR_CONTRASSUJEITO
                        total_pintadas += 1

    print(f"🎨 Total de notas coloridas: {total_pintadas}")
    
    # Garante que o diretório de saída existe (importante para Vercel)
    os.makedirs(os.path.dirname(xml_output), exist_ok=True)
    
    score.write('xml', fp=xml_output)
    print(f"📁 Arquivo salvo: {xml_output}")

if __name__ == "__main__":
    analisar_e_pintar()