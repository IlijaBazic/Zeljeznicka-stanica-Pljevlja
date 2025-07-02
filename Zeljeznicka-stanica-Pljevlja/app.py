from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlite3

app = Flask(__name__)
CORS(app)

def get_db_connection():
    conn = sqlite3.connect('vozovi.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/api/vozni_red', methods=['GET'])
def vozni_red():
    datum = request.args.get('datum')
    grad_od = request.args.get('grad_od')
    grad_ka = request.args.get('grad_ka')

    query = "SELECT * FROM vozni_red WHERE 1=1"
    params = []
    if datum:
        query += " AND datum=?"
        params.append(datum)
    if grad_od:
        query += " AND grad_od=?"
        params.append(grad_od)
    if grad_ka:
        query += " AND grad_ka=?"
        params.append(grad_ka)

    conn = get_db_connection()
    rows = conn.execute(query, params).fetchall()
    conn.close()

    # Vraćanje kao dict sa ID-evima kao ključevima
    rows_dict = {row['id']: dict(row) for row in rows}
    return jsonify(rows_dict)

@app.route('/api/vozni_red', methods=['POST']) # Kupi kartu
def kupi_kartu():
    data = request.get_json()
    id = data.get('id')
    broj_karti = data.get('broj_karti')

    if not id or not broj_karti:
        return jsonify({'error': 'Missing id or broj_karti'}), 400

    conn = get_db_connection()
    voz = conn.execute('SELECT slobodna_mjesta FROM vozni_red WHERE id=?', (id,)).fetchone()

    if not voz:
        return jsonify({'error': 'Voz not found'}), 404

    slobodna_mjesta = voz['slobodna_mjesta']

    if slobodna_mjesta < broj_karti:
        return jsonify({'error': 'Not enough free seats'}), 400

    new_slobodna_mjesta = slobodna_mjesta - broj_karti
    conn.execute('UPDATE vozni_red SET slobodna_mjesta=? WHERE id=?', (new_slobodna_mjesta, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Karta kupljena successfully', 'new_slobodna_mjesta': new_slobodna_mjesta})

@app.route('/api/vozni_red', methods=['PUT']) # Otkazi kartu
def otkazi_kartu():
    data = request.get_json()
    id = data.get('id')
    broj_karti = data.get('broj_karti')

    if not id or not broj_karti:
        return jsonify({'error': 'Missing id or broj_karti'}), 400

    conn = get_db_connection()
    voz = conn.execute('SELECT slobodna_mjesta FROM vozni_red WHERE id=?', (id,)).fetchone()

    if not voz:
        return jsonify({'error': 'Voz not found'}), 404

    slobodna_mjesta = voz['slobodna_mjesta']
    new_slobodna_mjesta = slobodna_mjesta + broj_karti
    conn.execute('UPDATE vozni_red SET slobodna_mjesta=? WHERE id=?', (new_slobodna_mjesta, id))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Karta otkazana successfully', 'new_slobodna_mjesta': new_slobodna_mjesta})

@app.route('/api/vozni_red', methods=['DELETE']) # Obrisi voz
def obrisi_voz():
    id_voz = request.args.get('id')

    if not id_voz:
        return jsonify({'error': 'Missing id'}), 400

    conn = get_db_connection()
    voz = conn.execute('SELECT * FROM vozni_red WHERE id=?', (id_voz,)).fetchone()

    if not voz:
        return jsonify({'error': 'Voz not found'}), 404

    conn.execute('DELETE FROM vozni_red WHERE id=?', (id_voz,))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Voz deleted successfully'})

@app.route('/api/vozni_red', methods=['PUT']) # Ažuriraj voz
def azuriraj_voz():
    data = request.get_json()
    id_voz = data.get('id')
    vrijeme_polaska = data.get('vrijeme_polaska')
    vrijeme_dolaska = data.get('vrijeme_dolaska')
    datum = data.get('datum')
    grad_od = data.get('grad_od')
    grad_ka = data.get('grad_ka')
    slobodna_mjesta = data.get('slobodna_mjesta')

    if not id_voz or not datum or not grad_od or not grad_ka or slobodna_mjesta is None:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    voz = conn.execute('SELECT * FROM vozni_red WHERE id=?', (id_voz,)).fetchone()

    if not voz:
        return jsonify({'error': 'Voz not found'}), 404

    conn.execute('UPDATE vozni_red SET datum=?, grad_od=?, grad_ka=?, slobodna_mjesta=? WHERE id=?',
                 (datum, grad_od, grad_ka, slobodna_mjesta, id_voz))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Voz updated successfully'})

@app.route('/api/vozni_red', methods=['POST']) # Dodaj voz
def dodaj_voz():
    data = request.get_json()
    datum = data.get('datum')
    grad_od = data.get('grad_od')
    grad_ka = data.get('grad_ka')
    slobodna_mjesta = data.get('slobodna_mjesta')

    if not datum or not grad_od or not grad_ka or slobodna_mjesta is None:
        return jsonify({'error': 'Missing required fields'}), 400

    conn = get_db_connection()
    conn.execute('INSERT INTO vozni_red (datum, grad_od, grad_ka, slobodna_mjesta) VALUES (?, ?, ?, ?)',
                 (datum, grad_od, grad_ka, slobodna_mjesta))
    conn.commit()
    conn.close()

    return jsonify({'message': 'Voz added successfully'}), 201

@app.route('/api/placanje', methods=['POST'])
def placanje():
    data = request.get_json()
    iznos = data.get('iznos')
    kartica_broj = data.get('kartica_broj')
    kartica_vrsta = data.get('kartica_vrsta')

    if not iznos or not kartica_broj or not kartica_vrsta:
        return jsonify({'error': 'Missing required fields'}), 400

    if len(kartica_broj) != 16 or not kartica_broj.isdigit():
        return jsonify({'error': 'Invalid card number'}), 400
    if kartica_vrsta not in ['Visa', 'MasterCard', 'American Express']:
        return jsonify({'error': 'Invalid card type'}), 400
    if iznos <= 0:
        return jsonify({'error': 'Invalid amount'}), 400

    return jsonify({'message': 'Payment successful', 'iznos': iznos, 'kartica_broj': kartica_broj, 'kartica_vrsta': kartica_vrsta})

@app.route('/api/vozni_red/<int:id>', methods=['GET'])
def get_polazak(id):
    conn = None
    try:
        conn = get_db_connection()
        polazak = conn.execute('SELECT * FROM vozni_red WHERE id = ?', (id,)).fetchone()
        if polazak is None:
            return jsonify({
                'error': 'Детаљи за овај полазак нису доступни',
                'button_text': 'у реду'
            }), 404
        return jsonify({
            'id': polazak['id'],
            'datum': polazak['datum'],
            'grad_od': polazak['grad_od'], 
            'grad_ka': polazak['grad_ka'],
            'slobodna_mjesta': polazak['slobodna_mjesta'],
            'vrijeme_polaska': polazak['vrijeme_polaska'],
            # 'vrijeme_dolaska': polazak['vrijeme_dolaska'],
            'napomena': polazak['napomena'],
            'prevoznik': polazak['prevoznik'],
            # 'cena': polazak['cena'],
            "tip_karte": polazak['tip_karte'],
            'rezervacija': polazak['rezervacija_moguca'],
            'placanje_online': polazak['placanje_online'],
            'student': polazak['popust_student'],
            'penzioner': polazak['popust_penzioner'],
            'kolosjek': polazak['kolosjek'],
        })
    except Exception as e:
        print(str(e))
        return jsonify({'error': 'Internal server error', 'message': str(e)}), 500
    finally:
        if conn:
            conn.close()

@app.after_request
def after_request(response):
    response.headers.add('Access-Control-Allow-Headers', 'Content-Type, Authorization')
    response.headers.add('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
    return response

if __name__ == '__main__':
    app.run(debug=True)