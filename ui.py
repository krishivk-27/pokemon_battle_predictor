import streamlit as st
from battle_ai import predict_battle

st.set_page_config(
    page_title="Pokémon Battle AI",
    page_icon="⚔️",
    layout="centered"
)

st.title("⚔️ Pokémon Battle AI")
st.write("Choose two Pokémon and let AI predict the winner!")

pokemon1 = st.text_input("Pokémon 1", "Charizard")
pokemon2 = st.text_input("Pokémon 2", "Blastoise")

if st.button("⚔️ Predict Battle"):

    with st.spinner("🤖 AI is analyzing the battle..."):

        result = predict_battle(pokemon1, pokemon2)

    st.markdown("---")

    st.markdown(result)