import streamlit as st
import google.generativeai as genai

# Page Configuration
st.set_page_config(page_title="AI Question Paper Generator", page_icon="📝", layout="centered")

st.title("📝 AI Question Paper Generator")
st.write("সহজেই যেকোনো শ্রেণি ও বিষয়ের প্রশ্নপত্র তৈরি করুন!")

# Gemini API Key Input
api_key = st.text_input("আপনার Google Gemini API Key দিন:", type="password", help="Gemini API Key পেতে Google AI Studio ব্যবহার করুন।")

st.markdown("---")

# Input Fields
col1, col2 = st.columns(2)

with col1:
    subject = st.text_input("বিষয় / টপিক (Subject / Topic):", "পদার্থবিজ্ঞান - গতি")
    class_level = st.selectbox("শ্রেণি (Class):", ["Class 6", "Class 7", "Class 8", "Class 9", "Class 10", "HSC / Class 11-12", "Other"])
    lang = st.selectbox("ভাষা (Language):", ["বাংলা", "English"])

with col2:
    q_type = st.selectbox("প্রশ্নের ধরন:", ["সৃজনশীল (CQ)", "বহুনির্বাচনী (MCQ)", "সংক্ষিপ্ত প্রশ্ন (Short Questions)", "মিক্সড (CQ + MCQ)"])
    total_marks = st.number_input("মোট নম্বর (Total Marks):", min_value=10, max_value=100, value=50, step=5)

num_questions = st.slider("প্রশ্নের সংখ্যা / উদ্দীপকের সংখ্যা:", 1, 15, 5)
special_instructions = st.text_area("বিশেষ কোনো নির্দেশ (ঐচ্ছিক):", placeholder="যেমন: উত্তরসহ তৈরি করুন, অথবা বিগত বছরের বোর্ড পরীক্ষার আদলে তৈরি করুন।")

# Generate Button
if st.button("🚀 প্রশ্নপত্র জেনারেট করুন", type="primary"):
    if not api_key:
        st.error("⚠️ মেহেরবানি করে আপনার Gemini API Key প্রদান করুন!")
    elif not subject:
        st.warning("⚠️ মেহেরবানি করে বিষয়টি লিখুন!")
    else:
        try:
            genai.configure(api_key=api_key)
            model = genai.GenerativeModel('gemini-1.5-flash')
            
            with st.spinner("প্রশ্ন তৈরি হচ্ছে... অনুগ্রহ করে কিছুটা সময় অপেক্ষা করুন..."):
                prompt = f"""
                You are an expert teacher and exam question paper maker.
                Create a formal, highly structured, and standard question paper based on the following specifications:

                - Subject / Topic: {subject}
                - Grade / Class: {class_level}
                - Language: {lang}
                - Question Type: {q_type}
                - Total Marks: {total_marks}
                - Number of main questions: {num_questions}
                - Additional Instructions: {special_instructions}

                Format instructions:
                1. Include a realistic exam header (School Name placeholder, Subject, Class, Time, Full Marks).
                2. Use clear section headers.
                3. If Creative Question (CQ): Provide a proper Stem (উদ্দীপক) followed by ক (১ mark), খ (২ marks), গ (৩ marks), ঘ (৪ marks).
                4. If MCQ: Provide question stem and 4 distinct options (ক, খ, গ, ঘ) for each question.
                5. Ensure accurate terminology in {lang}.
                """
                
                response = model.generate_content(prompt)
                
                st.success("🎉 প্রশ্নপত্র সফলভাবে তৈরি হয়েছে!")
                st.markdown("---")
                st.markdown(response.text)
                
                # Download Button
                st.download_button(
                    label="📥 প্রশ্নপত্র ডাউনলোড করুন (TXT)",
                    data=response.text,
                    file_name=f"Question_Paper_{subject}.txt",
                    mime="text/plain"
                )
        except Exception as e:
            st.error(f"একটি সমস্যা ঘটেছে: {str(e)}")
