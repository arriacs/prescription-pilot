import pandas as pd
import streamlit as st

med_data = pd.read_csv("data/cleaned_meds2.csv")

# displaying column names
print(med_data.columns.tolist())
print(med_data.head())


def search_medication(search_term):
    """
    Allows a user to search brand and generic medication names and returns matching
    records with their associated drug interaction information.
    """
    # converting search term to lowercase
    search_term = search_term.lower().strip() 
    # searching for brand names
    # fillna('') handles missing values, str.lower() makes searches case insensitve, 
    # regex=False treats special characters as regular text
    brand_match = med_data['brand_names'].fillna('').str.lower().str.contains(
        search_term, regex=False
    )
    # using same process to search for generic names
    generic_match = med_data['generic_names'].fillna('').str.lower().str.contains(
        search_term, regex=False
    )
    # combine and use both search results
    search_results = med_data[brand_match | generic_match]
    # check whether any medications matched the search
    if search_results.empty:
        print('No matching medication was found.')
        return search_results
    return search_results

def display_medication_info(search_results):
    """
    Extracts and displays relevant medication information from search results to the user.
    """

    # Extracting the medication information relevant to the user
    if search_results.empty: # Empty search result scenario
        print('No medication information available for the medication entered.')
        return search_results
    medication_info = search_results[['brand_names', 'generic_names', 'active_ingredients', 'drug_interactions']]
    return medication_info

# testing search_medication()
results = search_medication('glyburide')
print(results[['brand_names', 'generic_names', 'drug_interactions']])

results2 = search_medication('unknown') # testing using an unknown prescription
print(results2)

# testing display_medication_info()
print(display_medication_info(results))
print(display_medication_info(results2))

# Streamlit page title
st.title('Medication Interactions')

st.write(
    'Search for a prescription medication using its brand or generic name to view its potential drug interactions.'

)

# Medication search 
with st.form(key='medication_search_form'):
    search_term = st.text_input('Enter medication name:')
    search_button = st.form_submit_button('Search')
# Search for medications when medication is entered
if search_button:
    if search_term.strip():
        results = search_medication(search_term)
        medication_info = display_medication_info(results)

        if not medication_info.empty:
            st.subheader('Medication Search Results')
            for i, medication in medication_info.iterrows():
                st.write('**Brand Name:**', medication['brand_names'])
                st.write('**Generic Name:**', medication['generic_names'])
                st.write('**Active Ingredients:**', medication['active_ingredients'])

                with st.expander('Potential Drug Interactions'):
                    st.write(medication['drug_interactions'])
                st.divider() # handles scenarios with multiple matching medication records
        else:
            st.warning('Medication information is unavailable for the medication entered.') # This is if the given input has no information in the associated data
    else:
        st.warning('Please enter a medication name.') # This is for an empty input

# Disclaimer 
st.caption(
    'DISCLAIMER: All drug interaction information comes from DailyMed prescribing labels and is intended '
    'for basic informational uses only. It should not replace professional medical advice.'
)
# Data source info
st.write('Data Source: [DailyMed](https://www.dailymed.nlm.nih.gov/dailymed/about-dailymed.cfm)')