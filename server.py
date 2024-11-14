import json
from flask import Flask, request, jsonify

app = Flask(__name__)

def read_ids_from_file(file_path):
    try:
        with open(file_path, 'r') as f:
            ids = f.readlines()
        ids = [id.strip() for id in ids] 
        return ids
    except Exception as e:
        raise ValueError(f"Error reading the file: {str(e)}")

def filter_by_branch(ids, branch):
    filtered_ids = [id for id in ids if id.lower().startswith(branch.lower())]
    return filtered_ids

# Helper function to filter by year
def filter_by_year(ids, year):
    if year == '1':
        filtered_ids = [id for id in ids if id[0:4] == '2024']
    elif year == '2':
        filtered_ids = [id for id in ids if id[0:4] == '2023']
    elif year == '3':
        filtered_ids = [id for id in ids if id[0:4] == '2022']
    elif year == '4':
        filtered_ids = [id for id in ids if id[0:4] == '2021']
    elif year == '5':
        filtered_ids = [id for id in ids if id[0:4] == '2020']
    elif year == '6':
        filtered_ids = [id for id in ids if id[0:4] == '2019']
    else:
        filtered_ids = []  
    return filtered_ids

file_path = "data.txt"  
ids = read_ids_from_file(file_path)

@app.route('/')
def get_all_ids():
    year = request.args.get('year')
    format = request.args.get('format', default='json', type=str)
    if year:
        filtered_ids = filter_by_year(ids, year)
        if not filtered_ids:
            return jsonify({"error": f"No IDs found for year {year}"}), 404
    else:
        filtered_ids = ids 

    if format == 'text':
        return '\n'.join(filtered_ids)
    return jsonify({'ids': filtered_ids})

def get_all_ids():
    format = request.args.get('format', default='json', type=str)
    if format == 'text':
        return '\n'.join(ids)  # Return plain text
    return jsonify({'ids': ids})

@app.route('/filter_by_branch')
def get_by_branch():
    branch = request.args.get('branch')
    if branch is None:
        return jsonify({"error": "No branch provided"}), 400
    
    filtered_ids = filter_by_branch(ids, branch)
    if not filtered_ids:
        return jsonify({"error": "No data found for the specified branch"}), 404

    return jsonify({'ids': filtered_ids})

@app.route('/<id>')
def get_id_details(id):
    if id not in ids:
        return jsonify({"error": f"ID {id} not found"}), 404
    
    uid = f"{id[8:12]}" 
    if id[12] == 'P':
        campus = 'Pilani'
    elif id[12] == 'G':
        campus = 'Goa'
    elif id[12] == 'H':
        campus = 'Hyderabad'
    email = f"f{id[0:4]}{id[8:12]}@{campus.lower()}.bits-pilani.ac.in"
    year = 2024 - int(id[0:4]) + 1 

    return jsonify({
        "id": id,
        "uid": uid,
        "email": email,
        "year": year,
        "campus": campus
    })

# Error handling
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({"error": "Resource not found"}), 404

@app.errorhandler(400)
def bad_request(e):
    return jsonify({"error": "Bad request"}), 400

if __name__ == '__main__':
    app.run(debug=True, port=8000)