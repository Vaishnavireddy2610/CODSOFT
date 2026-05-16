import streamlit as st
import random
import time

st.set_page_config(page_title="Tic Tac Toe AI", page_icon="🎮", layout="centered")

# ---------- STYLE ----------
st.markdown("""
<style>
.stApp {
    background-color: #f5f7fa;
}

h1 {
    text-align: center;
    color: #2c3e50;
}

button {
    height: 85px !important;
    font-size: 26px !important;
    border-radius: 10px !important;
    background-color: #ffffff;
    color: black;
    border: 2px solid #dcdfe6;
}

.stButton > button:hover {
    background-color: #409eff;
    color: white;
}

/* WIN CELLS */
.win {
    background-color: #67c23a !important;
    color: white !important;
    border: 2px solid #2ecc71 !important;
    text-align: center;
    padding: 20px;
    font-size: 28px;
    border-radius: 10px;
}
</style>
""", unsafe_allow_html=True)

# ---------- TITLE ----------
st.title("🎮 Tic Tac Toe AI")

# ---------- MODE ----------
mode = st.radio("Mode", ["Play vs AI", "2 Player"], horizontal=True)

# ---------- DIFFICULTY ----------
difficulty = st.selectbox("Difficulty", ["Easy", "Medium", "Hard"])

# ---------- SESSION ----------
if "board" not in st.session_state:
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.session_state.score_updated = False
    st.session_state.win_pattern = []

# ---------- WIN CHECK ----------
def check_winner(board):
    patterns = [
        [0,1,2],[3,4,5],[6,7,8],
        [0,3,6],[1,4,7],[2,5,8],
        [0,4,8],[2,4,6]
    ]
    for pattern in patterns:
        a,b,c = pattern
        if board[a] and board[a] == board[b] == board[c]:
            return board[a], pattern
    return None, []

# ---------- MINIMAX ----------
def minimax(board, is_max):
    winner, _ = check_winner(board)

    if winner == "O":
        return 1
    elif winner == "X":
        return -1
    elif "" not in board:
        return 0

    if is_max:
        best = -100
        for i in range(9):
            if board[i] == "":
                board[i] = "O"
                score = minimax(board, False)
                board[i] = ""
                best = max(best, score)
        return best
    else:
        best = 100
        for i in range(9):
            if board[i] == "":
                board[i] = "X"
                score = minimax(board, True)
                board[i] = ""
                best = min(best, score)
        return best

# ---------- BEST MOVE ----------
def best_move():
    best_score = -100
    move = None

    for i in range(9):
        if st.session_state.board[i] == "":
            st.session_state.board[i] = "O"
            score = minimax(st.session_state.board, False)
            st.session_state.board[i] = ""

            if score > best_score:
                best_score = score
                move = i

    return move

# ---------- AI MOVE ----------
def ai_move():
    empty = [i for i in range(9) if st.session_state.board[i] == ""]

    # 🤖 thinking delay
    time.sleep(0.6)

    if difficulty == "Easy":
        move = random.choice(empty)
    elif difficulty == "Medium":
        move = random.choice(empty) if random.random() < 0.5 else best_move()
    else:
        move = best_move()

    st.session_state.board[move] = "O"

# ---------- PLAYER MOVE ----------
def player_move(i):
    if st.session_state.board[i] == "" and not st.session_state.game_over:

        if mode == "Play vs AI":
            st.session_state.board[i] = "X"
            winner, pattern = check_winner(st.session_state.board)

            if not winner:
                ai_move()
                winner, pattern = check_winner(st.session_state.board)

        else:
            turn = "X" if st.session_state.board.count("X") <= st.session_state.board.count("O") else "O"
            st.session_state.board[i] = turn
            winner, pattern = check_winner(st.session_state.board)

        # ✅ handle win instantly
        if winner:
            st.session_state.game_over = True
            st.session_state.win_pattern = pattern

            if not st.session_state.score_updated:
                st.session_state.score_updated = True

                if winner == "X":
                    st.session_state.player_score += 1
                else:
                    st.session_state.ai_score += 1

        st.rerun()

# ---------- SCOREBOARD ----------
col1, col2 = st.columns(2)
col1.metric("👤 Player (X)", st.session_state.player_score)
col2.metric("🤖 AI (O)", st.session_state.ai_score)

st.divider()

# ---------- TURN ----------
if not st.session_state.game_over:
    if mode == "Play vs AI":
        if st.session_state.board.count("X") == st.session_state.board.count("O"):
            st.info("👉 Your Turn")
        else:
            st.info("🤖 AI Thinking...")
    else:
        turn = "X" if st.session_state.board.count("X") <= st.session_state.board.count("O") else "O"
        st.info(f"👉 Player {turn}'s Turn")

# ---------- GRID ----------
for i in range(3):
    cols = st.columns(3)
    for j in range(3):
        idx = i * 3 + j
        val = st.session_state.board[idx]

        if val == "X":
            display = "❌"
        elif val == "O":
            display = "⭕"
        else:
            display = " "

        if idx in st.session_state.win_pattern:
            cols[j].markdown(f"<div class='win'>{display}</div>", unsafe_allow_html=True)
        else:
            if cols[j].button(display, key=idx, use_container_width=True):
                player_move(idx)

# ---------- RESULT MESSAGE ----------
winner, _ = check_winner(st.session_state.board)

if winner:
    if winner == "X":
        st.success("🎉 X Wins!")
    else:
        st.error("🤖 O Wins!")

elif "" not in st.session_state.board:
    st.warning("🤝 Draw!")

# ---------- BUTTONS ----------
col1, col2 = st.columns(2)

if col1.button("🔄 Restart"):
    st.session_state.board = [""] * 9
    st.session_state.game_over = False
    st.session_state.score_updated = False
    st.session_state.win_pattern = []
    st.rerun()

if col2.button("🗑 Reset Score"):
    st.session_state.player_score = 0
    st.session_state.ai_score = 0
    st.rerun()