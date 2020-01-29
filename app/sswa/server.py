from flask import render_template
import connexion

app = connexion.App(__name__, specification_dir='./')

app.add_api("swagger.yml")

@app.route("/")
def home():
    return render_template("home.html")

  
@app.route("/qrCode")
def qr_code():
    return render_template("QRCode.html")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)