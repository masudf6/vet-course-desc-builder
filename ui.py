import streamlit as st

from loader import load_units
from scraper import scrape_unit
from doc_builder import build_doc

st.image("logo.png", width=100)

st.markdown("------")


st.title("Abbey's Course Description Generator")

course_name = st.text_input("Enter Course Name")
excel_file = st.file_uploader('Upload Excel (Subject Code, Name, Type, Hours)', type=['xls', 'xlsx'])

if excel_file and course_name:
    units = load_units(excel_file)
    st.write(f'Detected {len(units)} units from sheet')

    if st.button('Fetch & Generate DOCX'):
        status = st.empty()
        for idx, u in enumerate(units, start=1):
            status.text(f'Scraping {u.code} ({idx}/{len(units)})')
            try:
                u.criteria = scrape_unit(u.code)
            except Exception as e:
                u.criteria = []
                st.warning(f'Failed to fetch {u.code}: {e}')
        status.text('Building document...')
        doc_buffer = build_doc(units, title=course_name)
        st.success('Done!')
        st.download_button(
            'Download DOCX',
            data=doc_buffer,
            file_name=f'course_description_{course_name}.docx',
            mime='application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        )


st.markdown(
    """
    <hr style="margin-top: 2rem;"/>
    <p style="text-align: center; font-size:0.8rem; color: #666;">
      © 2025 Masud Faruk. All rights reserved.
    </p>
    """,
    unsafe_allow_html=True
)