import streamlit as st
import google.generativeai as genai

# Page configuration
st.set_page_config(layout="wide")
st.title("🤖 Interview Guide: Embedded Systems (Senior Professionals)")
st.caption(f"Developed by [Madhu Hegde] {chr(0x00A9)} 2025")
st.markdown("""
This app acts as a **Technical Interviewer** from a top semiconductor company. 

It generates advanced questions, architectural patterns, and nuances for experienced engineers (typically **15+ years**, e.g., Principal/Staff).

**Key Sections:**
1. Connections to design patterns
2. System design questions
3. Code snippets and examples from top RTOS & Linux
4. Content derived only from authentic books and interviews
5. ARM architecture support for the mentioned context
""")


# Get API key from Streamlit secrets
if "GEMINI_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GEMINI_API_KEY"])
else:
    st.error("Missing API Key in secrets.")

# --- COMPLEX PROMPT / SYSTEM INSTRUCTION ---
# Updated to include ARM Cortex Architecture Specifics
system_instruction = """
Role: You are a Principal Embedded Systems Architect and Technical Interviewer at a top semiconductor company. 
Target Audience: A candidate with 15+ years of experience (Staff/Principal Engineer level).

Task: When the user enters an embedded concept, analyze it strictly from the perspective of high-level systems architecture, silicon-software interaction, and expert debugging. Do not explain basics.

Constraints:
1. Source material must be derived from top semiconductor company interview loops and renowned books (e.g., "The Art of Designing Embedded Systems" by Ganssle, "Embedded Systems Architecture" by Tammy Noergaard).
2. Do not provide generic web summaries. Focus on "gotchas," race conditions, memory barriers, and hardware constraints.

Output Format (Strictly follow these headers):
1. **Brief Concept Introduction**
   - Keep this under 100 words. Simple and concise.

2. **Concept for 15+ Years Experienced Professional**
   - High complexity. Discuss nuances like cache coherency, pipeline hazards, atomic operations, or kernel-level locking mechanisms related to the topic.

3. **Code Snippet**
   - A short, non-generic C or C++ snippet demonstrating a specific edge case, optimization, or low-level driver implementation details.

4. **Embedded Linux & ThreadX RTOS Examples**
   - Provide specific examples of the concept in Embedded Linux (kernel/user space) and ThreadX RTOS.
   - Highlight API differences, context switching implications, or determinism trade-offs between the two.

5. **Design Patterns & Architectural Patterns**
   - Discuss relevant patterns (e.g., HAL, Observer, Active Object).
   - Include ONE realistic System Design Interview Question (e.g., "Design a lock-free ring buffer for an ISR-to-Thread context").

6. **ARM Cortex Architecture Specifics**
   - Detail how the concept is supported or constrained by ARM Cortex (M, R, or A series) hardware.
   - Mention specific instructions (e.g., LDREX/STREX, WFI/WFE), memory barrier instructions (DMB/DSB/ISB), NVIC/GIC behavior, or MPU/MMU attributes relevant to the topic.

7. **Further Reading**
   - Suggest advanced chapters from renowned books or specific IEEE standards or research papers.
"""

# User input
user_topic = st.text_area("Enter an embedded concept (e.g., 'Spinlocks', 'DMA', 'ISR'):", height=100)

# Generate button
if st.button("Generate Interview Context"):
    if user_topic:
        with st.spinner("Consulting the Principal Architect..."):
            try:
                # Initialize model with the System Instruction
                model = genai.GenerativeModel(
                    model_name='gemini-2.5-flash',
                    system_instruction=system_instruction
                )
                
                # Send the specific topic to the specialized model
                response = model.generate_content(user_topic)
                
                st.success("Expert Analysis Generated:")
                st.markdown(response.text)
            except Exception as e:
                st.error(f"An error occurred: {e}")
    else:
        st.warning("Please enter a concept topic first!")

