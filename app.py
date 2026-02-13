from flask import Flask, render_template, jsonify, request
import gspread
from google.oauth2.service_account import Credentials
import os
import json

app = Flask(__name__)

# Google Sheets setup
SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive'
]

def get_sheet():
    """Connect to Google Sheet"""
    # For local development, use credentials.json file
    # For production (Render), use environment variable
    if os.path.exists('credentials.json'):
        creds = Credentials.from_service_account_file('credentials.json', scopes=SCOPES)
    else:
        # Load from environment variable (for deployment)
        creds_json = os.environ.get('GOOGLE_CREDENTIALS')
        if creds_json:
            creds_dict = json.loads(creds_json)
            creds = Credentials.from_service_account_info(creds_dict, scopes=SCOPES)
        else:
            raise Exception("No credentials found")
    
    client = gspread.authorize(creds)
    
    # Open the spreadsheet by name - change this to your sheet name
    spreadsheet = client.open(os.environ.get('SHEET_NAME', 'Resource Forecast'))
    return spreadsheet.sheet1

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/associates', methods=['GET'])
def get_associates():
    """Fetch all associates from Google Sheet"""
    try:
        sheet = get_sheet()
        records = sheet.get_all_records()
        
        associates = []
        for i, row in enumerate(records):
            associates.append({
                'id': i + 2,  # Row number (1-indexed, skip header)
                'name': row.get('Name', ''),
                'businessUnit': row.get('Business Unit', ''),
                'startDate': row.get('Start Date', ''),
                'endDate': row.get('End Date', ''),
                'numberOfDays': row.get('Number of Days', 0),
                'perDiem': row.get('Per Diem', 0),
                'costRate': row.get('Cost Rate', 0)
            })
        
        return jsonify(associates)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/associates', methods=['POST'])
def add_associate():
    """Add a new associate to Google Sheet"""
    try:
        sheet = get_sheet()
        data = request.json
        
        # Append new row
        sheet.append_row([
            data.get('name', ''),
            data.get('businessUnit', ''),
            data.get('startDate', ''),
            data.get('endDate', ''),
            data.get('numberOfDays', 0),
            data.get('perDiem', 0),
            data.get('costRate', 0)
        ])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/associates/<int:row_id>', methods=['PUT'])
def update_associate(row_id):
    """Update an associate in Google Sheet"""
    try:
        sheet = get_sheet()
        data = request.json
        
        # Update the row (row_id is the actual row number)
        sheet.update(f'A{row_id}:G{row_id}', [[
            data.get('name', ''),
            data.get('businessUnit', ''),
            data.get('startDate', ''),
            data.get('endDate', ''),
            data.get('numberOfDays', 0),
            data.get('perDiem', 0),
            data.get('costRate', 0)
        ]])
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/associates/<int:row_id>', methods=['DELETE'])
def delete_associate(row_id):
    """Delete an associate from Google Sheet"""
    try:
        sheet = get_sheet()
        sheet.delete_rows(row_id)
        
        return jsonify({'success': True})
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
