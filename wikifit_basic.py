import streamlit as st
import random
from datetime import datetime
import wikimedia  # Import our Wikimedia module

# Setup page config
st.set_page_config(page_title="WikiFit Basic", page_icon="💪")
st.title("💪 WikiFit Basic – Health & Fitness App")

# -------------------------------
# Utility Functions
# -------------------------------

def get_wikipedia_summary(term):
    """Get summary from Wikipedia API with error handling"""
    try:
        return wikimedia.get_wikipedia_summary(term)
    except Exception as e:
        st.error(f"Request error: {str(e)}")
        return "Connection error. Please try again later."

def get_random_health_tip():
    """Return a random health tip with seasonal awareness"""
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
            "Stay hydrated even when it's cold.",
            "Wash hands frequently to prevent seasonal colds and flu."
        ],
        # Spring (Mar-May)
        "spring": [
            "Consider seasonal allergy preparations before symptoms start.",
            "Spring clean your diet - add fresh seasonal produce.",
            "Gradually increase outdoor exercise as weather improves."
        ],
        # Summer (Jun-Aug)
        "summer": [
            "Apply sunscreen 30 minutes before sun exposure.",
            "Stay extra hydrated during hot days.",
            "Exercise during cooler parts of the day to avoid heat exhaustion."
        ],
        # Fall (Sep-Nov)
        "fall": [
            "Boost immune system as cold and flu season approaches.",
            "Adjust exercise routines for cooling temperatures.",
            "Incorporate seasonal produce like pumpkins and apples."
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

def get_workout_plan(workout_type="full_body"):
    """Get workout plan based on workout type"""
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

def get_did_you_know_fact():
    """Return a random health fact"""
    facts = [
        "The human body has 206 bones.",
        "Your heart beats about 100,000 times a day.",
        "The skin is the body's largest organ.",
        "The brain uses around 20% of the body's oxygen.",
        "Laughter is good for your heart and can reduce stress.",
        "Adults have fewer bones than babies. Babies are born with 300 bones, but some fuse together.",
        "The strongest muscle in your body is your masseter (jaw muscle)."
    ]
    return random.choice(facts)

def calculate_bmi(weight, height, unit="m"):
    """Calculate BMI based on weight and height"""
    if weight <= 0 or height <= 0:
        return None, None
    
    # Convert height to meters for calculation
    if unit == "cm":
        height = height / 100.0
    elif unit == "ft":
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

# -------------------------------
# UI
# -------------------------------

# Initialize session state
if 'workout_completed' not in st.session_state:
    st.session_state.workout_completed = 0
if 'quiz_score' not in st.session_state:
    st.session_state.quiz_score = 0

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

# Display current date
st.sidebar.markdown(f"**Today**: {datetime.now().strftime('%B %d, %Y')}")

# Navigation sidebar
menu = st.sidebar.selectbox("Navigate", [
    "Daily Tip", 
    "Health Search", 
    "Workout Plans", 
    "Home Remedies", 
    "Did You Know?", 
    "BMI Calculator"
])

st.sidebar.info("This is the basic version of WikiFit that works without advanced dependencies.")
st.sidebar.markdown("To access AI features and the Knowledge Center, [install the required packages](https://github.com/your-username/wikifit#installation) and run `ai.py`.")

# Page content based on menu selection
if menu == "Daily Tip":
    st.subheader("📆 Daily Fitness/Nutrition Tip")
    st.success(get_random_health_tip())

elif menu == "Health Search":
    st.subheader("🔍 Search Health Info from Wikipedia")
    query = st.text_input("Enter a health topic (e.g., Vitamin D, Yoga)")
    if query:
        with st.spinner("Searching..."):
            result = get_wikipedia_summary(query.replace(" ", "_"))
        st.info(result)

elif menu == "Workout Plans":
    st.subheader("🏋️‍♀️ Basic Workout Plans")
    workout_type = st.selectbox("Choose workout type", ["full_body", "cardio", "strength", "flexibility"])
    plan = get_workout_plan(workout_type)
    for step in plan:
        st.write(f"- {step}")
        
    if st.button("Mark as Completed"):
        st.session_state.workout_completed += 1
        st.success(f"Great job! You've completed {st.session_state.workout_completed} workouts.")

elif menu == "Home Remedies":
    st.subheader("🌿 Traditional Remedies")
    remedies = [
        ("Turmeric Milk", "Used for colds and inflammation."),
        ("Honey & Ginger", "Relieves sore throat and cough."),
        ("Amla Juice", "Boosts immunity and rich in Vitamin C."),
        ("Mint Tea", "Aids digestion and relieves headaches.")
    ]
    for title, desc in remedies:
        st.markdown(f"**{title}** – {desc}")

elif menu == "Did You Know?":
    st.subheader("❓ Fun Health Facts")
    st.info(get_did_you_know_fact())

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

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown(f"© WikiFit {datetime.now().year}")