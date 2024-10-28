from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from config import Config
from sqlalchemy import text
import json

app = Flask(__name__)
app.config.from_object(Config)

# Initialize the database connection
db = SQLAlchemy(app)

# Model for spatial data
class SpatialData(db.Model):
    __tablename__ = 'point_data'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50))
    geom = db.Column(db.String)  # Using String for simplicity

    def __repr__(self):
        return f'<SpatialData {self.name}>'

# Route for displaying the map with data
@app.route('/')
def index():
    # Retrieve data from PostGIS, converting geom to WKT format
    query = text("SELECT id, name, ST_AsText(geom) as geom FROM point_data")
    result = db.session.execute(query)
    points = result.fetchall()

    geojson_features = []
    for point in points:
        lon, lat = map(float, point.geom.replace('POINT(', '').replace(')', '').split())
        geojson_features.append({
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [lon, lat]
            },
            'properties': {
                'name': point.name
            }
        })

    geojson_data = json.dumps(geojson_features)
    return render_template('index.html', points=geojson_data)

# Route for displaying the profile page
@app.route('/profile')
def profile():
    return render_template('profile.html')

if __name__ == '__main__':
    app.run(debug=True)
