import os
import time

import streamlit as st
from huffman import build_huffman_tree, draw_tree, generate_codes
from streamlit_cookies_controller import CookieController


def main():
    st.text(f"Streamlit app is {os.environ['APP_NAME']}")
    cookie_controller = CookieController()
    st.markdown("""
        <style>
            div[data-testid="stForm"]:nth-of-type(1) {
                border: none;
                box-shadow: none;
                padding: 0;
            }
        </style>
    """, unsafe_allow_html=True)
    if "pending_rerun" not in st.session_state:
        st.session_state.pending_rerun = False
    st.session_state.symbols = cookie_controller.get("symbols") or []

    with st.form("add_symbol_form", clear_on_submit=True):
        symbol = st.text_input("Symbol")
        prob = st.number_input("Probability", min_value=0.0, max_value=1.0, step=0.01, format="%.2f")
        submitted = st.form_submit_button("Add Symbol")
        if submitted:
            if not symbol:
                st.warning("Symbol cannot be empty.")
            elif any(s["symbol"] == symbol for s in st.session_state.symbols):
                st.warning("Symbol already exists.")
            else:
                st.session_state.symbols.append({"symbol": symbol, "prob": prob})
                cookie_controller.set("symbols", st.session_state.symbols)


    # --- Total Probability Check ---
    total_prob = sum(item["prob"] for item in st.session_state.symbols)
    c1, c2 = st.columns(2)
    c1.markdown(f"**Total Probability:** {total_prob:.2f}")
    c2.markdown(f"**Probability left:** {1 - total_prob:.2f}")
    if abs(total_prob - 0.00) > 1e-6:
        st.warning("Total probability must sum to 0.0 to generate the Huffman Tree.")

    # --- Display and Edit Table ---
    st.subheader("📋 Current Symbols and Probabilities")
    for idx, item in enumerate(st.session_state.symbols):
        col1, col2, col3, col4 = st.columns([2, 2, 1, 1], vertical_alignment="bottom")
        with col1:
            new_symbol = st.text_input(f"Symbol {idx}", value=item["symbol"], key=f"sym_{idx}")
        with col2:
            new_prob = st.number_input(f"Prob {idx}", min_value=0.0, max_value=1.0,
                                       value=float(item["prob"]), step=0.01, key=f"prob_{idx}")
        with col3:
            with st.form("modify_symbol_form"+str(idx), clear_on_submit=True):
                submitted = st.form_submit_button("💾 Save")
                if submitted:
                    st.session_state.symbols[idx] = {"symbol": new_symbol, "prob": new_prob}
                    cookie_controller.set("symbols", st.session_state.symbols)
        with col4:
            with st.form("delete_symbol_form"+str(idx), clear_on_submit=True):
                submitted = st.form_submit_button("❌ Delete")
                if submitted:
                    st.session_state.symbols.pop(idx)
                    cookie_controller.set("symbols", st.session_state.symbols)


    # --- Generate Huffman Encoding ---
    if st.button("🚀 Generate Huffman Codes"):
        if abs(total_prob - 1.0) > 1e-6:
            st.error("Fix total probability before generating the tree.")
        elif not st.session_state.symbols:
            st.error("Add at least one symbol.")
        else:
            data = [(item["symbol"], item["prob"]) for item in st.session_state.symbols]
            tree = build_huffman_tree(data)
            codes = generate_codes(tree)
            dot = draw_tree(tree)

            st.subheader("🧬 Huffman Codes")
            for symbol, code in codes.items():
                st.write(f"`{symbol}` → `{code}`")

            st.subheader("🌳 Huffman Tree")
            st.graphviz_chart(dot)

if __name__ == "__main__":
    
    main()