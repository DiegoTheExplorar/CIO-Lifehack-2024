# CrimeWhere

CrimeWhere is a web application designed to enhance urban safety by optimizing police patrol routes using real-time crime data and machine learning. The application identifies crime hotspots, streamlines patrols, and reduces response times efficiently.

## Table of Contents

- [Inspiration](#inspiration)
- [What it does](#what-it-does)
- [How we built it](#how-we-built-it)
- [Challenges we ran into](#challenges-we-ran-into)
- [Accomplishments that we're proud of](#accomplishments-that-were-proud-of)
- [What we learned](#what-we-learned)
- [What's next for CrimeWhere](#whats-next-for-crimewhere)
- [Installation](#installation)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)

## Inspiration

When looking through all the problem statements, the one on strengthening domestic security intrigued us the most. We often complain about inefficiencies we observe around us, and this was a prime opportunity to make a meaningful impact in an important field. We were convinced that this is what we should work on.

## What it does

First, you upload a CSV file with the city's crime data, detailing where and when crimes occurred over a period. The website processes this data, clusters different locations, and uses an ML model to predict future crime hotspots. Using this information, we apply the Traveling Salesman Problem algorithm to find the optimal path for a police patrol vehicle in any given district within the police station's jurisdiction. This path is then displayed on a map for the officers' reference.

## How we built it

We used Flask for the backend, coding the entire logic of the website in Python. The frontend was developed using HTML and CSS.

## Challenges we ran into

The biggest challenge was integrating the frontend with our backend. Since all of us are new to frontend development, getting the code right and hosting it was a significant hurdle. Adapting to new libraries and APIs, such as GeoPandas, Folium, and OpenStreetMap, and making them work as needed was also challenging.

## Accomplishments that we're proud of

We successfully built our first full-stack project within just 48 hours, including a machine learning model and mapping functionalities. We learned a lot through trial and error. Despite the tiring process, we gained valuable software engineering skills.

## What we learned

We learned how to build a functional frontend and integrate it with the backend. We also learned to use APIs for mapping software and gained basic data analysis skills.

## What's next for CrimeWhere

We aim to enhance our model's accuracy in predicting crime hotspots by incorporating more variables. Additionally, we plan to make the final map more interactive, providing real-time guidance for patrol officers.

## Installation

1. **Clone the repository:**

   ```bash
   git clone https://github.com/DiegoTheExplorar/CIO-Lifehack-2024.git
   ```

2. **Set up the Flask environment:**

   ```bash
   python3 -m venv env_name
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   pip install -r requirements.txt

   Alternatively create your own python environment on VScode with ctrl+shift+p. VScode will automatically detect the requirements.txt file and automatically download the necessary files for the python environment
   ```

## Usage

1. **Run the Flask application:**

   ```bash
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   export FLASK_APP=actuallysuper.py
   export FLASK_ENV=development
   flask run
   ```

   On Windows, use `set` instead of `export`:

   ```bash
   set FLASK_APP=actuallysuper.py
   set FLASK_ENV=development
   flask run
   ```

2. **Open your browser:**

   Navigate to `http://localhost:5000` to use the application.

## Contributing

We welcome contributions to enhance CrimeWhere. Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-branch-name`.
3. Make your changes and commit them: `git commit -m 'Add some feature'`.
4. Push to the branch: `git push origin feature-branch-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
