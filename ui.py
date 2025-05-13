import streamlit as st

from loader import load_units
from scraper import scrape_unit
from doc_builder import build_doc

st.image("logo.png", width=100)

st.markdown("------")


st.title("RTO Course Description Generator")

st.markdown("""
- Go to the **RTO Manager's Course** tab  
- Select course subjects from the dropdown  
- Select your desired course and export the Excel

**Heads up:** The file you export from RTO Manager is *technically* an HTML file (even though it opens in Excel). Before uploading it here, open it in Excel and use **File → Save As → Excel Workbook (.xlsx)** to convert it properly.
""")


course_name = st.text_input("Enter Course Name")
header_image = st.file_uploader("Upload your institution's header image (optional)", type=["png", "jpg", "jpeg"])
excel_file = st.file_uploader('Upload Excel (Subject Code, Subject Name, Subject Type, Contact Hours)', type=['xls', 'xlsx'])


if excel_file:
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
        doc_buffer = build_doc(units, course_title=course_name, header_image=header_image)
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