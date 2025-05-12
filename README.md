# 📄 Course Description Generator

This Streamlit app generates formatted Word documents with course descriptions based on a list of training units provided in Excel. It's perfect for academic staff preparing documentation for student university applications.

---

## 🔧 Features

- Upload Excel files containing:
  - Subject Code
  - Subject Name
  - Subject Type (Core/Elective)
  - Contact Hours
- Automatically fetches official *Performance Criteria* from training.gov.au via XML
- Exports a well-formatted `.docx` with:
  - Bulleted criteria
  - Times New Roman styling
  - Custom course title

---

## 🚀 Try It Live

👉 https://masudf6-vet-course-desc-builder-ui-a9lo3t.streamlit.app/

---

## 📁 Excel Format

Make sure your Excel file has the following columns:

| Subject Code | Subject Name                    | Subject Type | Contact Hours |
|--------------|----------------------------------|---------------|----------------|
| BSBCRT512    | Originate and develop concepts   | Core          | 40 hours       |
| ICTDBS506    | Design databases                 | Elective      | 100 hours      |

---

## 🛠 How It Works

1. User provides a course name and uploads an Excel file.
2. The app reads unit metadata.
3. For each unit, it fetches the performance criteria from `training.gov.au`.
4. Generates and returns a downloadable `.docx` file.
