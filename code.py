import streamlit as st

# --- Configurações Iniciais do App ---
st.set_page_config(
    page_title="Poker Macedo",
    layout="centered" # "centered" ou "wide"
)

st.title("🏆 Poker Macedo 🏆")
st.markdown("Gerencie a pontuação do seu torneio de poker!")

# --- Inicialização dos Participantes (usando st.session_state para persistir dados) ---
# st.session_state é como um dicionário que armazena dados entre as interações do usuário.
if 'participants' not in st.session_state:
    st.session_state.participants = [
        {"name": "Rodrigo", "score": 0},
        {"name": "Gui", "score": 0},
        {"name": "Raquel", "score": 0},
        {"name": "Nilsa", "score": 0},
        {"name": "Cleber", "score": 0},
        {"name": "Leandro", "score": 0},
    ]

# --- Função para Ordenar e Exibir a Classificação ---
def display_leaderboard():
    st.subheader("Classificação Atual")
    
    # Ordena os participantes pela pontuação em ordem decrescente
    sorted_participants = sorted(st.session_state.participants, key=lambda x: x['score'], reverse=True)
    
    # Exibe a classificação
    if sorted_participants:
        for i, participant in enumerate(sorted_participants):
            st.write(f"**{i+1}. {participant['name']}**: {participant['score']} pontos")
    else:
        st.write("Nenhum participante cadastrado ainda.")

# --- Seção de Adição de Pontuação ---
st.subheader("➕ Registrar Pontuação da Partida")

# Usamos um formulário para agrupar as entradas de pontuação e o botão de submissão.
# Isso evita que o app seja recarregado a cada número digitado.
with st.form(key='add_score_form'):
    st.markdown("Insira os pontos que cada jogador ganhou nesta partida:")
    
    new_scores_input = {} # Dicionário temporário para guardar os pontos digitados nesta submissão
    
    # Cria uma entrada de número para cada participante
    # O truque 'key=f"score_input_{p['name']}"' é crucial para que cada widget seja único.
    for participant in st.session_state.participants:
        new_scores_input[participant['name']] = st.number_input(
            f"Pontos para {participant['name']}",
            min_value=0,      # Pontuação mínima é 0
            value=0,          # Valor inicial é 0
            step=1,           # Incrementa de 1 em 1
            key=f"score_input_{participant['name']}", # Chave única para o widget
            label_visibility="collapsed" # Esconde o label padrão, pois já temos o texto acima
        )
            
    submit_button = st.form_submit_button(label='Adicionar Pontos da Partida')

    if submit_button:
        # Itera sobre os participantes e atualiza suas pontuações no st.session_state
        for i, participant in enumerate(st.session_state.participants):
            name = participant['name']
            score_to_add = new_scores_input[name]
            
            if score_to_add > 0:
                st.session_state.participants[i]['score'] += score_to_add
        
        st.success("Pontuações adicionadas com sucesso!")
        # Força o app a recarregar para exibir a nova classificação
        st.rerun()

# --- Exibir a Classificação no final ---
# Isso garante que a classificação seja sempre a última coisa mostrada e atualizada.
display_leaderboard()

# --- Rodapé (Opcional) ---
st.markdown("---")
st.info("Desenvolvido para o torneio Poker Macedo.")