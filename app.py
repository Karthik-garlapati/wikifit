import streamlit as st
try:
    import transformers
    import torch
    from transformers import pipeline
    ai_enabled = True
except ImportError as e:
    ai_enabled = False
    st.warning("⚠️ AI features are not available. Please install required libraries: pip install transformers torch")

import random
import logging  # For better error tracking
import pandas as pd  # For chart data
from datetime import datetime  # For progress tracking
import wikimedia  # Import our Wikimedia module


# Set page config first before any other st commands
st.set_page_config(page_title="WikiFit", page_icon="💪")

# Setup basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Check for transformers library after setting page config
try:
    from transformers import pipeline
    AI_AVAILABLE = True
except ImportError:
    AI_AVAILABLE = False

# WikiFit - Health & Fitness App with AI Integration
#
# Required packages:
# - streamlit
# - requests
# - transformers
# - torch (automatically installed with transformers)
#
# To install all requirements:
# pip install streamlit requests transformers torch

# -------------------------------
# Utils
# -------------------------------

# Cache the Wikimedia functions using Streamlit's caching decorator
@st.cache_data(ttl=3600)
def get_wikipedia_summary(term):
    """Get summary of a topic from Wikipedia."""
    result = wikimedia.get_wikipedia_summary(term)
    return result

@st.cache_data(ttl=3600)
def get_wiktionary_definition(term):
    """Get word definitions from Wiktionary"""
    return wikimedia.get_wiktionary_definition(term)

@st.cache_data(ttl=3600)
def get_wikiquote_quotes(term):
    """Get quotes related to a topic from Wikiquote"""
    return wikimedia.get_wikiquote_quotes(term)

@st.cache_data(ttl=3600)
def get_wikibooks_content(term):
    """Get educational content from Wikibooks"""
    return wikimedia.get_wikibooks_content(term)

@st.cache_data(ttl=3600)
def get_wikimedia_commons_images(term, limit=5):
    """Get relevant images from Wikimedia Commons"""
    return wikimedia.get_wikimedia_commons_images(term, limit)

@st.cache_data(ttl=3600)
def get_wikisource_texts(term):
    """Get health-related texts from Wikisource"""
    return wikimedia.get_wikisource_texts(term)

@st.cache_data(ttl=3600)
def get_wikiversity_resources(term):
    """Get educational resources from Wikiversity"""
    return wikimedia.get_wikiversity_resources(term)

@st.cache_data(ttl=3600)
def get_wikispecies_info(species_name):
    """Get species information from Wikispecies"""
    return wikimedia.get_wikispecies_info(species_name)

@st.cache_data(ttl=3600)
def get_wikidata_health_info(term):
    """Get structured health data from Wikidata"""
    return wikimedia.get_wikidata_health_info(term)

# Add a new function to search across all Wikimedia sources at once
@st.cache_data(ttl=3600)
def search_all_wikimedia(term):
    """Search for a term across all Wikimedia platforms."""
    return wikimedia.search_all_wikimedia(term)


def get_random_health_tip():
    # Get current month to provide seasonal tips
    current_month = datetime.now().month
    
    # Base tips that apply all year
    base_tips = [
        "Drink at least 2 liters of water every day.",
        "Do at least 30 minutes of physical activity daily.",
        "Maintain a regular sleep schedule.",
        "Include fruits and vegetables in every meal.",
        "Take short breaks during long sitting hours.",
        "Practice mindfulness meditation for 10 minutes daily.",
        "Reduce sodium intake to help control blood pressure.",
        "Limit screen time before bedtime for better sleep.",
        "Choose whole grains over refined carbohydrates.",
        "Incorporate strength training at least twice a week."
    ]
    
    # Seasonal tips
    seasonal_tips = {
        # Winter (Dec-Feb)
        "winter": [
            "Increase vitamin D intake during winter months.",
            "Stay hydrated even when it's cold - indoor heating dehydrates you.",
            "Wash hands frequently to prevent seasonal colds and flu.",
            "Keep exercise routines indoor when weather is harsh.",
            "Moisturize skin more frequently in dry winter air."
        ],
        # Spring (Mar-May)
        "spring": [
            "Consider seasonal allergy preparations before symptoms start.",
            "Spring clean your diet - add fresh seasonal produce.",
            "Gradually increase outdoor exercise as weather improves.",
            "Check and replace air filters to reduce spring allergens.",
            "Stay hydrated as temperatures begin to rise."
        ],
        # Summer (Jun-Aug)
        "summer": [
            "Apply sunscreen 30 minutes before sun exposure.",
            "Stay extra hydrated during hot days.",
            "Exercise during cooler parts of the day to avoid heat exhaustion.",
            "Include electrolytes if sweating heavily.",
            "Check for signs of dehydration in hot weather."
        ],
        # Fall (Sep-Nov)
        "fall": [
            "Boost immune system as cold and flu season approaches.",
            "Adjust exercise routines for cooling temperatures.",
            "Incorporate seasonal produce like pumpkins and apples.",
            "Keep up vitamin D as sunlight exposure decreases.",
            "Prepare indoor exercise options for colder days ahead."
        ]
    }
    
    # Determine current season
    if current_month in [12, 1, 2]:
        season = "winter"
    elif current_month in [3, 4, 5]:
        season = "spring"
    elif current_month in [6, 7, 8]:
        season = "summer"
    else:  # 9, 10, 11
        season = "fall"
    
    # Combine base tips with seasonal tips
    all_tips = base_tips + seasonal_tips[season]
    return random.choice(all_tips)


def generate_quiz():
    """Generate a random health quiz question with multiple choice options"""
    questions = [
        ("How many bones are there in the human body?", ["206", "201", "212", "195"], "206"),
        ("What vitamin do we get from sunlight?", ["Vitamin A", "Vitamin B12", "Vitamin D", "Vitamin C"], "Vitamin D"),
        ("Which organ uses the most oxygen?", ["Heart", "Brain", "Lungs", "Liver"], "Brain"),
        ("What percentage of the human body is water?", ["50-60%", "60-70%", "70-80%", "80-90%"], "60-70%"),
        ("Which nutrient is the primary source of energy for the body?", ["Protein", "Fats", "Carbohydrates", "Vitamins"], "Carbohydrates")
    ]
    return random.choice(questions)


def calculate_bmi(weight, height, unit="m"):
    """Calculate BMI (Body Mass Index).
    
    Args:
        weight: Weight in kilograms
        height: Height in meters, centimeters, or feet (with decimal for inches)
        unit: Unit of height measurement ("m", "cm", or "ft")
        
    Returns:
        tuple: (bmi_value, bmi_category)
    """
    if weight <= 0 or height <= 0:
        return None, None
    
    # Convert height to meters for calculation
    if unit == "cm":
        height = height / 100.0
    elif unit == "ft":
        # Convert feet/inches to meters (1 foot = 0.3048 meters)
        feet_whole = int(height)
        inches = (height - feet_whole) * 10
        height = feet_whole * 0.3048 + inches * 0.0254
        
    bmi = weight / (height ** 2)
    
    if bmi < 18.5:
        category = "Underweight"
    elif 18.5 <= bmi < 25:
        category = "Normal weight"
    elif 25 <= bmi < 30:
        category = "Overweight"
    else:
        category = "Obese"
        
    return round(bmi, 2), category


def get_workout_plan(workout_type="full_body"):
    workouts = {
        "full_body": [
            "10 Jumping Jacks",
            "10 Push-ups",
            "15 Squats",
            "20-second Plank",
            "10 Lunges (each leg)",
            "Repeat 3 times"
        ],
        "cardio": [
            "30 seconds Jumping Jacks",
            "30 seconds High Knees",
            "30 seconds Butt Kicks",
            "30 seconds Mountain Climbers",
            "30 seconds rest",
            "Repeat 4 times"
        ],
        "strength": [
            "12 Push-ups",
            "15 Squats with 5 second hold",
            "10 Tricep Dips",
            "10 Glute Bridges",
            "8 Superman Holds",
            "Repeat 3 times"
        ],
        "flexibility": [
            "30 seconds Hamstring Stretch",
            "30 seconds Quad Stretch (each leg)",
            "30 seconds Child's Pose",
            "30 seconds Cat-Cow Stretch",
            "30 seconds Butterfly Stretch",
            "Repeat 2 times"
        ]
    }
    return workouts.get(workout_type, workouts["full_body"])


def get_wikibooks_remedies():
    # Placeholder text simulating Wikibooks data
    return [
        ("Turmeric Milk", "Used for colds and inflammation."),
        ("Honey & Ginger", "Relieves sore throat and cough."),
        ("Amla Juice", "Boosts immunity and rich in Vitamin C."),
        ("Mint Tea", "Aids digestion and relieves headaches."),
        ("Aloe Vera Gel", "Soothes skin irritation and burns."),
        ("Fenugreek Seeds", "Helps control blood sugar levels.")
    ]


def get_did_you_know_fact():
    facts = [
        "The human body has 206 bones.",
        "Your heart beats about 100,000 times a day.",
        "The skin is the body's largest organ.",
        "The brain uses around 20% of the body's oxygen.",
        "Laughter is good for your heart and can reduce stress.",
        "Adults have fewer bones than babies. Babies are born with 300 bones, but some fuse together.",
        "The strongest muscle in your body is your masseter (jaw muscle).",
        "Your stomach acid is strong enough to dissolve zinc and sometimes metal.",
        "The human nose can detect over 1 trillion different scents."
    ]
    return random.choice(facts)


@st.cache_resource
def load_qa_pipeline():
    if not AI_AVAILABLE:
        return None
        
    try:
        return pipeline("question-answering", model="distilbert-base-cased-distilled-squad")
    except Exception as e:
        logging.error(f"Error loading QA model: {str(e)}")
        return None

# Load the pipeline at startup
qa_pipeline = load_qa_pipeline()

def answer_health_question(question, context):
    """
    Process a health-related question using the QA pipeline and provided context
    
    Args:
        question: The user's question as a string
        context: Health information context for the model to use
        
    Returns:
        Answer string or error message
    """
    if qa_pipeline is None:
        return "AI model is not available. Please check if transformers and torch are installed correctly."
    
    try:
        # Add disclaimer for health info
        if len(question) < 5:
            return "Please ask a more specific question."
            
        # Process the question
        result = qa_pipeline(
            question=question, 
            context=context, 
            max_answer_len=100,  # Limit very long answers
            handle_impossible_answer=True
        )
        
        # Check confidence score
        if result.get('score', 0) < 0.1:
            return "I don't have enough information to answer that question accurately. Please try a different question related to the topics covered."
            
        return result['answer']
    except Exception as e:
        logging.error(f"QA error: {str(e)}")
        return f"Sorry, I couldn't process your question. Error: {str(e)}"


# -------------------------------
# UI
# -------------------------------

st.title("💪 WikiFit – Health & Fitness from Wikimedia")

# Initialize session state for visit_history first
if 'visit_history' not in st.session_state:
    st.session_state.visit_history = []
    
# Get time of day for personalized welcome
current_hour = datetime.now().hour
if 5 <= current_hour < 12:
    greeting = "Good morning"
elif 12 <= current_hour < 17:
    greeting = "Good afternoon"
else:
    greeting = "Good evening"

# Welcome message in the sidebar
st.sidebar.markdown(f"### {greeting}!")
st.sidebar.markdown("Welcome to WikiFit, your personal health assistant.")

# Display current date and streak
st.sidebar.markdown(f"**Today**: {datetime.now().strftime('%B %d, %Y')}")
days_visited = len(st.session_state.visit_history)
if days_visited > 0:
    st.sidebar.markdown(f"**Streak**: {days_visited} days")
    
current_date = datetime.now().strftime("%Y-%m-%d")
if current_date not in st.session_state.visit_history:
    st.session_state.visit_history.append(current_date)

# Initialize session state for tracking progress
if 'workout_completed' not in st.session_state:
    st.session_state.workout_completed = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0
if 'last_visit' not in st.session_state:
    st.session_state.last_visit = None
# visit_history is already initialized above

# Check if this is a new day visit
current_date = datetime.now().strftime("%Y-%m-%d")
if st.session_state.last_visit != current_date:
    st.session_state.last_visit = current_date
    # Add this date to visit history if not already there
    if current_date not in st.session_state.visit_history:
        st.session_state.visit_history.append(current_date)
    st.sidebar.success("Welcome to a new day of health & fitness!")

# Main navigation
menu = st.sidebar.selectbox("Navigate", [
    "Daily Tip", 
    "Health Search", 
    "Workout Plans", 
    "Home Remedies", 
    "Did You Know?", 
    "Fitness Quiz", 
    "BMI Calculator",
    "AI Health Q&A",
    "Knowledge Center",  # New Wikimedia endpoints integration
    "Progress Tracker"   # Added progress tracker option
])

if menu == "Daily Tip":
    st.subheader("📆 Daily Fitness/Nutrition Tip")
    tip = get_random_health_tip()
    st.success(tip)
    
    # Determine if this is a seasonal tip
    current_month = datetime.now().month
    if any(keyword in tip.lower() for keyword in ["winter", "vitamin d", "cold", "indoor", "flu"]) and current_month in [12, 1, 2]:
        st.info("💡 This is a seasonal winter health tip.")
    elif any(keyword in tip.lower() for keyword in ["spring", "allergy", "pollen", "seasonal"]) and current_month in [3, 4, 5]:
        st.info("💡 This is a seasonal spring health tip.")
    elif any(keyword in tip.lower() for keyword in ["summer", "sun", "heat", "hydrated", "sunscreen"]) and current_month in [6, 7, 8]:
        st.info("💡 This is a seasonal summer health tip.")
    elif any(keyword in tip.lower() for keyword in ["fall", "autumn", "immune", "cooling"]) and current_month in [9, 10, 11]:
        st.info("💡 This is a seasonal fall health tip.")

elif menu == "Health Search":
    st.subheader("🔍 Search Health Info from Wikipedia")
    query = st.text_input("Enter a health topic (e.g., Vitamin D, Yoga)")
    if query:
        result = get_wikipedia_summary(query.replace(" ", "_"))
        st.info(result)

elif menu == "Workout Plans":
    st.subheader("🏋️‍♀️ Basic Workout Plans from Wikibooks")
    workout_type = st.selectbox("Choose workout type", ["full_body", "cardio", "strength", "flexibility"])
    plan = get_workout_plan(workout_type)
    for step in plan:
        st.write(f"- {step}")
        
    if st.button("Mark as Completed"):
        st.session_state.workout_completed += 1
        st.success(f"Great job! You've completed {st.session_state.workout_completed} workouts.")

elif menu == "Home Remedies":
    st.subheader("🌿 Traditional Remedies from Wikibooks")
    remedies = get_wikibooks_remedies()
    for title, desc in remedies:
        st.markdown(f"**{title}** – {desc}")

elif menu == "Did You Know?":
    st.subheader("❓ Fun Health Facts from Wikipedia")
    st.info(get_did_you_know_fact())

elif menu == "Fitness Quiz":
    st.subheader("🧠 Quick Fitness Quiz")
    q, options, answer = generate_quiz()
    user_answer = st.radio(q, options)
    if st.button("Submit"):
        if user_answer == answer:
            st.success("Correct! ✅")
            st.session_state.quiz_score += 10
            st.success(f"You earned 10 points! Total score: {st.session_state.quiz_score}")
        else:
            st.error(f"Incorrect. The right answer is {answer}.")

elif menu == "BMI Calculator":
    st.subheader("📊 BMI Calculator")
    
    col1, col2 = st.columns(2)
    
    with col1:
        weight = st.number_input("Weight (kg)", min_value=0.0, max_value=300.0, value=70.0, step=0.1)
    
    with col2:
        unit = st.selectbox("Height unit", ["m", "cm", "ft"], index=0)
        
        if unit == "m":
            height = st.number_input("Height (m)", min_value=0.0, max_value=3.0, value=1.70, step=0.01)
        elif unit == "cm":
            height = st.number_input("Height (cm)", min_value=0.0, max_value=300.0, value=170.0, step=1.0)
        else:  # ft
            height = st.number_input("Height (ft.in)", 
                                   min_value=0.0, 
                                   max_value=8.0, 
                                   value=5.6, 
                                   step=0.1,
                                   help="Enter feet as whole number and inches as decimal (e.g., 5.6 for 5'6\")")
    
    if st.button("Calculate BMI"):
        bmi_value, bmi_category = calculate_bmi(weight, height, unit)
        
        if bmi_value and bmi_category:
            st.info(f"Your BMI: **{bmi_value}**")
            
            if bmi_category == "Underweight":
                st.warning(f"Category: **{bmi_category}**")
            elif bmi_category == "Normal weight":
                st.success(f"Category: **{bmi_category}**")
            elif bmi_category == "Overweight":
                st.warning(f"Category: **{bmi_category}**")
            else:
                st.error(f"Category: **{bmi_category}**")
                
            st.write("BMI Categories:")
            st.write("- Underweight: < 18.5")
            st.write("- Normal weight: 18.5–24.9")
            st.write("- Overweight: 25–29.9")
            st.write("- Obese: ≥ 30")

elif menu == "AI Health Q&A":
    st.subheader("🤖 Ask any health or fitness question")
    
    if not AI_AVAILABLE:
        st.error("AI features are not available. Please install required libraries: `pip install transformers torch`")
        st.info("After installing, please restart the application.")
        st.stop()
    
    # Create tabs for different knowledge sources
    tab1, tab2, tab3 = st.tabs(["General Health", "Nutrition", "Fitness"])
    
    with tab1:
        # General health context
        health_context = """
        Regular check-ups with healthcare providers are essential for preventive care.
        Vaccination helps prevent infectious diseases by building immunity.
        Mental health is as important as physical health for overall well-being.
        Chronic stress can lead to various physical and mental health problems.
        Sleep hygiene practices include consistent sleep schedule and limiting screen time before bed.
        Proper handwashing is one of the most effective ways to prevent illness.
        Smoking is the leading cause of preventable death worldwide.
        Moderate alcohol consumption means up to 1 drink per day for women and 2 for men.
        """
        
        question1 = st.text_input("Ask a general health question", key="general_health")
        if question1:
            with st.spinner("Finding answer..."):
                answer = answer_health_question(question1, health_context)
            st.info(f"**Answer:** {answer}")
            st.caption("Note: This AI provides general information and should not replace professional medical advice.")
    
    with tab2:
        # Nutrition context
        nutrition_context = """
        The five main food groups are fruits, vegetables, grains, protein foods, and dairy.
        Proteins are essential for building and repairing tissues in the body.
        Carbohydrates are the body's main source of energy.
        Healthy fats support cell growth and protect organs.
        Fiber aids digestion and helps maintain bowel health.
        Vitamins and minerals are essential for various bodily functions.
        Antioxidants help protect cells from damage caused by free radicals.
        Turmeric contains curcumin which has anti-inflammatory properties.
        Green tea is rich in antioxidants called catechins.
        Processed foods often contain high levels of sodium, sugar, and unhealthy fats.
        """
        
        question2 = st.text_input("Ask a nutrition question", key="nutrition")
        if question2:
            with st.spinner("Finding answer..."):
                answer = answer_health_question(question2, nutrition_context)
            st.info(f"**Answer:** {answer}")
            st.caption("Consult with a nutritionist for personalized dietary advice.")
    
    with tab3:
        # Fitness context
        fitness_context = """
        Cardiovascular exercise improves heart health and increases stamina.
        Strength training helps build and maintain muscle mass.
        Flexibility exercises help maintain joint mobility and prevent injuries.
        Rest days are important for muscle recovery and growth.
        Progressive overload is necessary for continued fitness improvements.
        HIIT (High-Intensity Interval Training) involves short bursts of intense exercise.
        Proper form during exercise helps prevent injuries.
        Warming up before exercise prepares your body for physical activity.
        Cooling down after exercise helps reduce muscle stiffness.
        Functional fitness focuses on exercises that help with everyday activities.
        """
        
        question3 = st.text_input("Ask a fitness question", key="fitness")
        if question3:
            with st.spinner("Finding answer..."):
                answer = answer_health_question(question3, fitness_context)
            st.info(f"**Answer:** {answer}")
            st.caption("Always consult with a fitness professional before starting a new exercise program.")

elif menu == "Knowledge Center":
    st.subheader("📚 Health & Fitness Knowledge Center")
    st.write("Explore a wealth of knowledge from various Wikimedia projects")
    
    # Create tabs for different Wikimedia sources
    wiki_tabs = st.tabs([
        "Wikipedia", "Wiktionary", "Wikiquote", 
        "Wikibooks", "Wikimedia Commons", "Wikisource", 
        "Wikiversity", "Wikispecies", "Wikidata"
    ])
    
    query = st.text_input("Search across Wikimedia projects", placeholder="Enter a health or fitness topic...")
    
    if query:
        search_term = query.strip().replace(" ", "_")
        
        # Wikipedia Tab
        with wiki_tabs[0]:
            st.subheader(f"📖 Wikipedia: {query}")
            with st.spinner("Searching Wikipedia..."):
                wiki_result = get_wikipedia_summary(search_term)
                st.info(wiki_result)
                st.caption("Source: Wikipedia, the free encyclopedia")
        
        # Wiktionary Tab
        with wiki_tabs[1]:
            st.subheader(f"📕 Wiktionary: {query}")
            with st.spinner("Searching Wiktionary..."):
                wikt_result = get_wiktionary_definition(search_term)
                st.info(wikt_result)
                st.caption("Source: Wiktionary, the free dictionary")
        
        # Wikiquote Tab
        with wiki_tabs[2]:
            st.subheader(f"💬 Wikiquote: {query}")
            with st.spinner("Searching Wikiquote..."):
                quote_result = get_wikiquote_quotes(search_term)
                st.info(quote_result)
                st.caption("Source: Wikiquote, the free quote compendium")
        
        # Wikibooks Tab
        with wiki_tabs[3]:
            st.subheader(f"📚 Wikibooks: {query}")
            with st.spinner("Searching Wikibooks..."):
                books_result = get_wikibooks_content(search_term)
                st.info(books_result)
                st.caption("Source: Wikibooks, open books for an open world")
        
        # Wikimedia Commons Tab
        with wiki_tabs[4]:
            st.subheader(f"🖼️ Wikimedia Commons: {query}")
            with st.spinner("Searching Wikimedia Commons..."):
                images = get_wikimedia_commons_images(search_term)
                if images:
                    cols = st.columns(min(3, len(images)))
                    for i, img in enumerate(images):
                        with cols[i % 3]:
                            st.image(img["url"], caption=img["title"])
                            if img["description"]:
                                st.caption(img["description"][:100] + "..." if len(img["description"]) > 100 else img["description"])
                else:
                    st.info("No images found for this topic on Wikimedia Commons.")
                st.caption("Source: Wikimedia Commons, the free media repository")
        
        # Wikisource Tab
        with wiki_tabs[5]:
            st.subheader(f"📜 Wikisource: {query}")
            with st.spinner("Searching Wikisource..."):
                source_results = get_wikisource_texts(search_term)
                if source_results:
                    for result in source_results:
                        st.markdown(f"**{result['title']}**")
                        st.write(result["snippet"])
                        st.markdown("---")
                else:
                    st.info("No relevant texts found on Wikisource.")
                st.caption("Source: Wikisource, the free digital library")
        
        # Wikiversity Tab
        with wiki_tabs[6]:
            st.subheader(f"🎓 Wikiversity: {query}")
            with st.spinner("Searching Wikiversity..."):
                university_result = get_wikiversity_resources(search_term)
                st.info(university_result)
                st.caption("Source: Wikiversity, a learning platform")
        
        # Wikispecies Tab
        with wiki_tabs[7]:
            st.subheader(f"🦠 Wikispecies: {query}")
            with st.spinner("Searching Wikispecies..."):
                species_result = get_wikispecies_info(search_term)
                st.info(species_result)
                st.caption("Source: Wikispecies, free species directory")
        
        # Wikidata Tab
        with wiki_tabs[8]:
            st.subheader(f"🗃️ Wikidata: {query}")
            with st.spinner("Searching Wikidata..."):
                data_result = get_wikidata_health_info(search_term)
                if isinstance(data_result, dict):
                    st.markdown(f"**{data_result['label']}**")
                    st.write(data_result['description'])
                    
                    if data_result['properties']:
                        st.subheader("Related properties:")
                        for prop, values in data_result['properties'].items():
                            st.write(f"**{prop}**: {', '.join(values)}")
                else:
                    st.info(data_result)
                st.caption("Source: Wikidata, the free knowledge base")
    
    else:
        st.info("Enter a health or fitness topic above to explore information from all Wikimedia projects")
        
        # Show some example topics
        st.markdown("### Example topics to search:")
        example_cols = st.columns(3)
        with example_cols[0]:
            st.markdown("**Health topics**")
            st.markdown("- Vitamin D")
            st.markdown("- Diabetes")
            st.markdown("- Mental health")
            st.markdown("- Immune system")
        
        with example_cols[1]:
            st.markdown("**Fitness topics**")
            st.markdown("- HIIT")
            st.markdown("- Strength training")
            st.markdown("- Flexibility")
            st.markdown("- Cardiovascular exercise")
            
        with example_cols[2]:
            st.markdown("**Nutrition topics**")
            st.markdown("- Protein")
            st.markdown("- Carbohydrates")
            st.markdown("- Antioxidants")
            st.markdown("- Superfoods")
            
        st.info("The Knowledge Center brings together health and fitness information from across all Wikimedia projects in one place.")

elif menu == "Progress Tracker":
    st.subheader("📈 Personal Progress Tracker")
    
    # Display current stats
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Workouts Completed", st.session_state.workout_completed)
    with col2:
        st.metric("Quiz Score", f"{st.session_state.quiz_score} points")
    
    # Add workout completion
    st.subheader("Log Your Activity")
    with st.form("workout_form"):
        workout_date = st.date_input("Date", datetime.now())
        workout_type = st.selectbox("Workout Type", 
                                  ["Full Body", "Cardio", "Strength", "Flexibility", "Walking/Running", "Cycling", "Other"])
        duration = st.number_input("Duration (minutes)", min_value=5, max_value=240, step=5)
        intensity = st.slider("Intensity", 1, 10, 5)
        notes = st.text_area("Notes (optional)")
        
        submit = st.form_submit_button("Log Workout")
        
        if submit:
            st.session_state.workout_completed += 1
            st.success(f"Workout logged! You've completed {st.session_state.workout_completed} workouts.")
            
            # Display motivational message based on workout count
            if st.session_state.workout_completed % 5 == 0:
                st.balloons()
                st.success(f"🎉 Congratulations on your {st.session_state.workout_completed}th workout!")
    
    # Allow users to set goals
    st.subheader("Set Health Goals")
    goal = st.text_input("Enter your health goal")
    target_date = st.date_input("Target date", datetime.now())
    
    if st.button("Save Goal"):
        st.success("Goal saved! We'll help you track your progress.")
        
    # Display a simple progress chart (placeholder for now)
    st.subheader("Workout History")
    
    # Create chart data in the format Streamlit expects
    # Create a DataFrame that Streamlit can plot
    chart_data = pd.DataFrame({
        'Workouts': [
            st.session_state.workout_completed,
            max(0, st.session_state.workout_completed - 2),
            max(0, st.session_state.workout_completed - 5),
            max(0, st.session_state.workout_completed - 8)
        ]},
        index=['Week 1', 'Week 2', 'Week 3', 'Week 4']
    )
    
    st.bar_chart(chart_data)
