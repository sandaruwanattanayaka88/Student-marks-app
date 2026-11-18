import os
import pandas as pd
import streamlit as st

st.set_page_config(
    page_title="ගුරු ඇගයීම් ලකුණු පද්ධතිය", page_icon="📚", layout="centered"
)

# දත්ත ගොනුවේ නම
DATA_FILE = "student_marks.csv"


# දත්ත ගොනුව පරීක්ෂා කිරීම හෝ සෑදීම
def load_data():
  if os.path.exists(DATA_FILE):
    return pd.read_csv(DATA_FILE)
  else:
    # මුල් දත්ත ලැයිස්තුව (මෙහි ඔබේ පන්තියේ සිසුන්ගේ විස්තර ඇතුළත් කළ හැක)
    df = pd.DataFrame(
        columns=["Student_ID", "Student_Name", "Assessment_Name", "Marks"]
    )
    return df


df = load_data()

st.title("📚 ගුරු ඇගයීම් ලකුණු කළමනාකරණය")
st.write("ඉගැන්වීම් අතරතුර ඉතා ඉක්මනින් සිසුන්ගේ ලකුණු ඇතුළත් කරන්න.")

# පෝරමය (Form)
with st.form("marks_form"):
  st.subheader("ලකුණු ඇතුළත් කිරීම")

  col1, col2 = st.columns(2)
  with col1:
    student_id = st.text_input("සිසු අංකය (Student ID)", placeholder="උදා: 01")
    student_name = st.text_input("සිසුවාගේ නම", placeholder="උදා: නම...")
  with col2:
    assessment_name = st.selectbox(
        "ඇගයීම / වාරය",
        [
            "පළමු වාර පරීක්ෂණය",
            "දෙවන වාර පරීක්ෂණය",
            "ඒකක පරීක්ෂණය 01",
            "ඒකක පරීක්ෂණය 02",
            "ප්‍රායෝගික ඇගයීම",
        ],
    )
    marks = st.number_input("ලකුණු (0 - 100)", min_value =0.0, max_va=value 0.0, step=1.0)

  submit_button = st.form_submit_button(label="ලකුණු සුරකින්න (Save)")

  if submit_button:
    if student_id and student_name:
      new_entry = pd.DataFrame({
          "Student_ID": [student_id],
          "Student_Name": [student_name],
          "Assessment_Name": [assessment_name],
          "Marks": [marks],
      })
      df = pd.concat([df, new_entry], ignore_index=True)
      df.to_csv(DATA_FILE, index=False)
      st.success(f" සාර්ථකයි! {student_name} ගේ ලකුණු සුරකින ලදී.")
    else:
      st.warning("කරුණාකර සිසු අංකය සහ නම ඇතුළත් කරන්න.")

# ඇතුළත් කළ දත්ත පෙන්වීම
st.divider()
st.subheader("📊 මෙතෙක් ඇතුළත් කළ ලකුණු සාරාංශය")

if not df.empty:
  # සෙවුම් පහසුකමක්
  search_query = st.text_input(
      "සිසු නමින් හෝ අංකයෙන් සොයන්න (Search):", ""
  )
  if search_query:
    filtered_df = df[
        df["Student_Name"].str.contains(search_query, case=False, na=False)
        | df["Student_ID"].str.contains(search_query, case=False, na=False)
    ]
    st.dataframe(filtered_df, use_container_width=True)
  else:
    st.dataframe(df, use_container_width=True)

  # CSV ලෙස ඩවුන්ලෝඩ් කරගැනීමට බොත්තමක්
  csv = df.to_csv(index=False).encode("utf-8")
  st.download_button(
      label="ସ සියලුම දත්ත CSV ලෙස බාගත කරගන්න (Download)",
      data=csv,
      file_name="student_marks_report.csv",
      mime="text/csv",
  )
else:
  st.info("තවම දත්ත ඇතුළත් කර නැත.")
