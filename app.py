import streamlit as st
import duckdb

con = duckdb.connect(database='database.duckdb', read_only=True)

st.set_page_config(layout="wide")

st.title('Fantasy Duck Sauce')

st.subheader('All Players')

players = con.execute("""
        select * from players;
    """).df()

st.write(players)

st.subheader('Playing')

playing = con.execute("""
        select *
        from players
        where playingStatus = 'playing' and
        ownerId is null
        order by average asc;
    """).df()

st.write(playing)

st.subheader('Returning')

returning = con.execute("""
        select * from players
        where injuryEta is not null and
        ownerId is null
        order by average asc;
    """).df()

st.write(returning)
