import streamlit as st
import requests

API_KEY = 'eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjAxZDRlNjVhLWVlMTctNDFkZi1iYTFlLTRlYmIzODg1MWY0NCIsImlhdCI6MTcxODUyMTk1OSwic3ViIjoiZGV2ZWxvcGVyLzhjYWU5ZWNmLWJmN2EtMmVkNy1kNzYzLWQ1YTFjMDZkOTM5NiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE1Ny40Ni4xNTguMTUyIl0sInR5cGUiOiJjbGllbnQifV19.Cw0ssnVe8No0C3W7Zr314XXCtJ0MsmUDefGCkmydszis25lDE_bPc3m2ifJtivzJlKtU6e822DFk21_tswj9kA'
def get_clan_members(api_key, clan_tag):
    url = f'https://api.clashofclans.com/v1/clans/{clan_tag.replace("#", "%23")}/members'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def get_player_info(api_key, player_tag):
    url = f'https://api.clashofclans.com/v1/players/{player_tag.replace("#", "%23")}'
    headers = {
        'Authorization': f'Bearer {api_key}'
    }
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    return response.json()

def main():
    st.title('Clash of Clans Clan and Player Info')
    
    clan_tag = st.text_input('Enter Clan Tag (with #):', value='#')
    clan_tag='#J9L2QCJC'
    
    if clan_tag:
        try:
            clan_members = get_clan_members(API_KEY, clan_tag)
        except requests.exceptions.HTTPError as http_err:
            if http_err.response.status_code == 403:
                st.error("Forbidden: Check your API key and IP whitelist settings.")
            else:
                st.error(f"HTTP error occurred: {http_err}")
            return
        except requests.exceptions.RequestException as err:
            st.error(f"Error fetching clan members: {err}")
            return

        member_names = [member['name'] for member in clan_members['items']]
        member_tags = {member['name']: member['tag'] for member in clan_members['items']}
        
        selected_member = st.selectbox('Select a Member:', member_names)
        
        if selected_member:
            player_tag = member_tags[selected_member]
            try:
                player_info = get_player_info(API_KEY, player_tag)
            except requests.exceptions.HTTPError as http_err:
                st.error(f"HTTP error occurred: {http_err}")
                return
            except requests.exceptions.RequestException as err:
                st.error(f"Error fetching player info for {selected_member}: {err}")
                return
            
            st.subheader(f"Player Info: {selected_member}")
            st.write(f"Tag: {player_info['tag']}")
            st.write(f"Town Hall Level: {player_info['townHallLevel']}")
            st.write(f"Experience Level: {player_info['expLevel']}")
            
            st.subheader("Heroes:")
            for hero in player_info.get('heroes', []):
                #st.write(player_info)
                st.write(f"{hero['name']}: Level {hero['level']}")

if __name__ == "__main__":
    main()
