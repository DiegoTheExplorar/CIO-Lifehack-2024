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

Devpost

## Inspiration
Our world is constantly changing and evolving. Instability, nationalism and threats to peace are on the rise in every corner of the globe. Here in Singapore, we are not sheltered from the fallouts of Geopolitical events, nor are we immune to threats to our small nation’s stability. Domestic security is something that concerns us, for everybody wants to live in safety. With this view, the problem statement on strengthening our domestic security resonated with us the most. We know that government agencies, such as the police force do their best to protect us. We also know that they would seek to optimise their manpower and resources as much as possible, to be able to help anyone in times of need. One manner in which they keep our communities safe is by patrolling around our heartlands and neighbourhoods, with the aim of deterring criminals and helping people in need, yet because of limited resources, need to do so efficiently. We felt that this was a technical problem that we would be able to make a meaningful contribution towards solving, and thus embarked on it.

## What it does 
There are a few steps for the end users. Firstly, they upload a CSV file containing the crime data in the jurisdiction, containing details of locations of crimes committed over a sufficient period of time. The web app processes this data, clusters different locations, and then uses a Machine Learning model to predict future crime hotspots. This data is then plotted onto a map for reference. Following that. the information is then used, together with data on police force districts (within the jurisdiction) in a Geojson file and data on neighbourhood police stations in a CSV file, to classify predicted future crime hotspots into the district they are expected to occur in. Then, a Travelling Salesman Problem algorithm is used to find an optimal path for a police patrol in the district, and this path is then displayed on a map for the planning officers’ reference.

## How we built it
The backend is managed by Flask in Python. The functions for the clustering and Machine Learning algorithm were called from libraries like RandomForestClassifier and DBScan clustering libraries. The functions for location classification were obtained from the Pandas and GeoPandas libraries. Finally, the functions for the TSP algorithm and mapping display were obtained from Folium, GeoPy and NetworkX libraries, and OpenStreetMap APIs.

## Challenges we ran into
The biggest challenge was debugging the backend for our web app. We do not have significant expertise in this area and are relatively new to full stack development, and thus getting the backend functional and ensuring the intended functionality of the system. Following that, integration of the front end and user interface for our web app was also a challenge, but we managed to overcome this with less difficulty than debugging the back end. In particular, creating the map visualisations was not easy. Finally, it was difficult to find a site that could host the entirety of our web app, including the backend functionality, due to the slightly large space and computational resource demands that free web hosting services do not provide, and thus we were unable to deploy our project from a web server, and instead it has to be run from a local server.

## Accomplishments that we’re proud of
We successfully built a full-stack project in just 48 hours, from ideation to a functioning product. This included creating and using a machine learning model, data cleaning and clustering functionality, and mapping functionality. We learnt a lot through tireless trial and error, but gained much insight into web development and a software engineering process.

## What we learned
We learned how to build a functional backend with significant time constraints, and successfully integrate it with a simple front end user interface. We also learned to use all the APIs and libraries that were mentioned earlier, along with refining our skills in implementing a machine learning model, and data cleaning and clustering functions.

## What’s next for CrimeWhere
We aim to increase the accuracy of the predictions provided by the model by incorporating a larger number of variables that would be more reflective of real-world conditions and factors that can lead to variations in crime that our current model may not always accurately provide for. Furthermore, we aim to allow more customisation and scalability in patrol route options, such as by implementing solutions to the mutli-vehicle depot scheduling problem. Finally we aim to make the final map displayed more interactive, and possibly provide real-time guidance for patrol officers.

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
   ```
Alternatively create your own python environment on VScode with ctrl+shift+p. VScode will automatically detect the requirements.txt file and automatically download the necessary files for the python environment

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
