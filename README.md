# What's Cookin' - Recipe Finder and Personal Dashboard

"What's Cookin'" is a personalized recipe finder and dashboard application developed using Streamlit, Firebase, and web scraping techniques. This project showcases a user-centric web application with features designed to enhance the user experience by offering tailored recipe recommendations, dietary filtering, user authentication, and the ability to save and like recipes.

This project reflects my skills in data handling, web scraping, authentication, and data visualization to provide an interactive experience. The app is suitable for individuals who want to explore new recipes based on personal preferences and dietary needs while also managing a personal favorites list.

## Table of Contents

-   [Project Features](#project-features)
-   [Technologies Used](#technologies-used)
-   [Setup and Installation](#setup-and-installation)
-   [Skills Demonstrated](#skills-demonstrated)
-   [Future Enhancements](#future-enhancements)

## Project Features

1.  **User Authentication with Firebase**:
    -   User registration and login are powered by Firebase Authentication.
    -   Secure password storage using bcrypt hashing.
    -   Ability to "Like" and save recipes to a personalized dashboard for future reference.
2.  **Recipe Finder with Dietary Preferences and Filtering**:
    -   Users can filter recipes based on ingredients, preparation time, cooking time, servings, and dietary preferences (e.g., vegetarian, vegan, gluten-free).
    -   Allows exclusion of specific allergens to ensure recipes are tailored to dietary restrictions.
3.  **Personalized Dashboard**:
    -   Users can view their liked recipes in an organized list that displays full recipe details when expanded.
    -   A pie chart visually represents the user's preferred recipe categories based on liked recipes.
    -   "Sign Out" feature to protect user privacy and session management.
4.  **Web Scraping for Recipe Data**:
    -   Recipe data is sourced through custom web scraping of popular Pakistani recipe websites, ensuring a culturally relevant and diverse selection.
    -   Scraped data is organized and stored in a CSV file (`cleaned_recipes.csv`), containing essential recipe details like title, ingredients, instructions, and categories.
5.  **Data Visualization**:
    -   Used `matplotlib` to generate pie charts representing users' preferences, adding an engaging visual element to the dashboard.

## Technologies Used

-   **Streamlit**: To build an interactive, user-friendly web application interface.
-   **Firebase**:
    -   **Firebase Authentication** for secure login and signup functionalities.
    -   **Firestore Database** to store user details and liked recipes.
-   **Web Scraping (BeautifulSoup, Requests)**: Used to scrape Pakistani recipes from public sources to build a culturally relevant dataset.
-   **Python Libraries**:
    -   **Pandas** for data handling and manipulation of scraped recipe data.
    -   **Bcrypt** for secure password hashing.
    -   **Matplotlib** for data visualization in the user dashboard.

## Setup and Installation

1.  **Clone the Repository**:
    

    
    `git clone https://github.com/laibashakil/What-s-Cookin-.git
    cd What-s-Cookin-` 
    
2.  **Install Dependencies**: Make sure you have Python installed, then install the required libraries:
    
    
    
    `pip install -r requirements.txt` 
    
3.  **Firebase Setup**:
    
    -   Download your Firebase service account key (JSON file) and rename it to `firebase_credentials.json`.
    -   Place this file in the root directory of the project.
4.  **CSV File**:
    
    -   Ensure the `cleaned_recipes.csv` file (containing scraped recipes) is in the project root directory.
5.  **Run the Application**:
    
    `streamlit run auth.py` 
    
6.  **Navigate to the Local Server**: Open your browser and go to `http://localhost:8501` to access the application.
    

## Skills Demonstrated

1.  **Web Development with Streamlit**:
    
    -   Developed a structured, interactive, and user-friendly web app.
    -   Created a clean navigation and responsive layout, suitable for recipe exploration and personalized user experience.
2.  **User Authentication and Security**:
    
    -   Implemented secure authentication using Firebase and bcrypt hashing for password management.
    -   Enabled users to save their favorite recipes securely, demonstrating a commitment to user data privacy and security.
3.  **Data Handling and Manipulation**:
    
    -   Processed scraped recipe data to organize it in a CSV format, then used Pandas for efficient filtering and data manipulation.
    -   Designed a structured recipe filtering system that allows users to find recipes based on detailed criteria.
4.  **Data Visualization**:
    
    -   Integrated data visualization with `matplotlib`, using a pie chart to display user preferences, showcasing my ability to make data insights visually accessible and engaging.
5.  **Web Scraping**:
    
    -   Utilized web scraping tools like BeautifulSoup and Requests to gather recipe data from Pakistani culinary websites, ensuring a locally relevant dataset.
    -   Cleaned and structured the scraped data to make it suitable for analysis and user interaction.
    

## Future Enhancements

1.  **Recommendation Engine**: Incorporate machine learning to recommend recipes based on user preferences and past interactions.
    
2.  **Enhanced Filtering Options**: Add more specific filters for calorie count, nutritional value, and additional dietary preferences.
    
3.  **Recipe Ratings and Comments**: Enable users to rate and leave comments on recipes, fostering a community-driven platform.
    
4.  **Recipe Sharing**: Allow users to share liked recipes on social media platforms.
    
5.  **Recipe Upload Feature**: Provide a feature for users to upload and share their own recipes within the app, enriching the recipe database.