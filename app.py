from database import create_table


from flask import Flask, jsonify, request, render_template
app = Flask(__name__)




@app.route("/")
def home():
    create_table()
    return render_template("index.html")


from scraper_run import web_scrape
@app.route("/run_web_scraper", methods=["POST"])
def run_web_scraper():
    data = request.get_json()
    area = data["area"]
    web_scrape(area)
    return jsonify({"reply": "running scraper"})


from database import get_price_drop
@app.route("/search_location_in_database", methods=["POST"])
def search_location_in_database():
    data = request.get_json()
    area = data["area"]
    reply = get_price_drop(area)

    return jsonify({"reply": reply})


if __name__ == "__main__":
    app.run(debug=True, use_reloader=False)


