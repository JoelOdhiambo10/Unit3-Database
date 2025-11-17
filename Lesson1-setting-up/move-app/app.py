"""
CineMatch - Movie Discovery Platform
Lesson 3.1 STARTER CODE
"""
from flask import Flask, render_template, request, redirect, url_for, flash
# from sample_movies import movies
from models import db, Movie

app = Flask(__name__)
app.config['SECRET_KEY'] = 'dev-secret-key-change-in-production'

# ⚠️ PROBLEM: These movies only exist in RAM (temporary memory)
# When you stop the Flask app, this data is GONE forever!

# DATABASE CONFIGURATION
#SQLite database will be stored in instance/cinematch.db
#instance folder is automatically created by Flask
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///cinematch.db'

app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

#initialize the database
db.init_app(app)

#DATABASE INITIALIZATION
def create_tables():
    '''Create all database tables
    This runs once to set up the database'''
    with app.app_context():
        db.create+all()
        print("✅Database tables created!")

def load_initial_movies():
    '''Checks if the database is empty, and id so adds sample movies'''
    with app.app_context():
        #Check if any movies exist
        if Movie.query.count() == 0:
            print("🎥Loading initial movies!")
            #Create movie objects
            movies =[
                Movie(
                    # skip id because it will be auto generated
                    title="Inception",
                    year=2010,
                    genre="Sci-Fi",
                    director="Christopher Nolan",
                    rating=8.8,
                    description="A thief who steals corporate secrets through dream-sharing technology is given the inverse task of planting an idea.",
                    poster_url="https://placehold.co/300x450/667eea/ffffff?text=Inception"
                     ),
                Movie(
                     title="Interstellar",
                     year=2014,
                     genre="Sci-Fi",
                     director="Christopher Nolan",
                     rating=8.6,
                     description="A team of explorers travel through a wormhole in space in an attempt to ensure humanity's survival.",
                     poster_url="https://placehold.co/300x450/667eea/ffffff?text=Interstellar"
                     ),
                Movie(
                     title="The Dark Knight",
                     year=2008,
                     genre="Action",
                     director="Christopher Nolan",
                     rating=9.0,
                     description="Batman faces the Joker, a criminal mastermind who wants to plunge Gotham into anarchy.",
                     poster_url="https://placehold.co/300x450/667eea/ffffff?text=The+Dark+Knight"
                     ),
                Movie(
                     title="Tenet",
                     year=2020,
                     genre="Action/Sci-Fi",
                     director="Christopher Nolan",
                     rating=7.4,
                     description="Armed with one word, Tenet, a secret agent fights for the survival of the world in a twilight mission that unfolds in something beyond real time.",
                     poster_url="https://placehold.co/300x450/667eea/ffffff?text=Tenet"
                     ),
                Movie(
                     title="Memento",
                     year=2000,
                     genre="Thriller",
                     director="Christopher Nolan",
                     rating=8.4,
                     description="A man with short-term memory loss attempts to track down his wife's murderer using notes and tattoos to keep track of information.",
                     poster_url="https://placehold.co/300x450/667eea/ffffff?text=Memento"
                    )
                    
            ]

            #Add all the movies to the seesion(staging area)
            for movie in movies:
                db.session.add(movie)
            #Commit to database (make changes permanent)
            db.session.commit()
            print(f"Added {len(movies)} movies to database!")

# ============================================================================
# ROUTES
# ============================================================================

@app.route('/')
def index():
    #Get the first 4 movies for homepage preview 
    movies = Movie.query.limit
    """Homepage with hero section"""
    return render_template('index.html', movies=movies)


@app.route('/movies')
def movies_list():
    """
    Display all movies
    
    TODO (Later in Unit 3): Change this to query from database instead of list
    """
    movies = Movie.query.order_by(Movie.rating.desc()).all()
    return render_template('movies.html', movies=movies)


@app.route('/about')
def about():
    """About CineMatch page"""
    return render_template('about.html')


# ============================================================================
# ERROR HANDLERS
# ============================================================================

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors"""
    return render_template('errors/404.html'), 404


@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors"""
    return render_template('errors/500.html'), 500


# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    #create tables on first run
    create_tables()
    #load initial movies if database is empty
    load_initial_movies()

    # Debug mode: Shows errors and auto-reloads on code changes
    app.run(debug=True, host='0.0.0.0', port=5070)
