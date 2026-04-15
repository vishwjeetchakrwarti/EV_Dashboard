# =============================================
#   EVPULSE DASHBOARD — app.py
#   Path: ev_dashboard/app.py
#
#   Run karne ka tarika:
#   > pip install flask pandas
#   > python app.py
#   Open in Browser: http://localhost:5000
# =============================================

from flask import Flask, render_template, jsonify, send_from_directory
import pandas as pd
import os

# ============ APP SETUP ============
app = Flask(
    __name__,
    template_folder="templates",   # index.html yahan se load hoga
    static_folder="static"         # CSS, JS yahan se serve hoga
)

# ============ PATHS ============
BASE_DIR  = os.path.dirname(os.path.abspath(__file__))
CSV_PATH  = os.path.join(BASE_DIR, "data", "Electric_Vehicle_Population_Data.csv")
CHART_DIR = os.path.join(BASE_DIR, "charts")


# ============================================================
#   ROUTE 1 — Home Page
#   URL: http://localhost:5000/
# ============================================================
@app.route("/")
def index():
    return render_template("index.html")


# ============================================================
#   ROUTE 2 — Chart Images Serve Karna
#   URL: http://localhost:5000/charts/<filename>
#   Example: /charts/top_makes.png
# ============================================================
@app.route("/charts/<path:filename>")
def serve_chart(filename):
    return send_from_directory(CHART_DIR, filename)


# ============================================================
#   ROUTE 3 — Stats API (JSON)
#   URL: http://localhost:5000/api/stats
#   main.js bhi CSV se read karta hai, yeh backup API hai
# ============================================================
@app.route("/api/stats")
def api_stats():
    try:
        df = pd.read_csv(CSV_PATH)

        total_evs  = len(df)
        total_bev  = int((df["Electric Vehicle Type"].str.contains("BEV", na=False)).sum())
        total_phev = int((df["Electric Vehicle Type"].str.contains("PHEV", na=False)).sum())
        total_cities = int(df["City"].nunique())

        return jsonify({
            "status"       : "success",
            "total_evs"    : total_evs,
            "total_bev"    : total_bev,
            "total_phev"   : total_phev,
            "total_cities" : total_cities
        })

    except FileNotFoundError:
        return jsonify({
            "status" : "error",
            "message": "CSV file nahi mili — data/Electric_Vehicle_Population_Data.csv check karo"
        }), 404

    except Exception as e:
        return jsonify({
            "status" : "error",
            "message": str(e)
        }), 500


# ============================================================
#   ROUTE 4 — Top Makes API (JSON)
#   URL: http://localhost:5000/api/top-makes?limit=10
# ============================================================
@app.route("/api/top-makes")
def api_top_makes():
    try:
        df    = pd.read_csv(CSV_PATH)
        limit = int(app.request.args.get("limit", 10)) if hasattr(app, "request") else 10

        from flask import request as freq
        limit = int(freq.args.get("limit", 10))

        top   = df["Make"].value_counts().head(limit)
        data  = [{"make": k, "count": int(v)} for k, v in top.items()]

        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
#   ROUTE 5 — Top Cities API (JSON)
#   URL: http://localhost:5000/api/top-cities?limit=15
# ============================================================
@app.route("/api/top-cities")
def api_top_cities():
    try:
        from flask import request as freq
        df    = pd.read_csv(CSV_PATH)
        limit = int(freq.args.get("limit", 15))

        top  = df["City"].value_counts().head(limit)
        data = [{"city": k, "count": int(v)} for k, v in top.items()]

        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
#   ROUTE 6 — Model Year Trend API (JSON)
#   URL: http://localhost:5000/api/year-trend
# ============================================================
@app.route("/api/year-trend")
def api_year_trend():
    try:
        df   = pd.read_csv(CSV_PATH)
        df   = df[df["Model Year"].notna()]
        df["Model Year"] = df["Model Year"].astype(int)

        trend = df["Model Year"].value_counts().sort_index()
        data  = [{"year": int(k), "count": int(v)} for k, v in trend.items()]

        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
#   ROUTE 7 — EV Type Split API (JSON)
#   URL: http://localhost:5000/api/ev-type
# ============================================================
@app.route("/api/ev-type")
def api_ev_type():
    try:
        df   = pd.read_csv(CSV_PATH)
        cols = df["Electric Vehicle Type"].value_counts()
        data = [{"type": k, "count": int(v)} for k, v in cols.items()]

        return jsonify({"status": "success", "data": data})

    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500


# ============================================================
#   ROUTE 8 — 404 Custom Error Page
# ============================================================
@app.errorhandler(404)
def not_found(e):
    return jsonify({
        "status" : "error",
        "message": "Page nahi mili — URL check karo"
    }), 404


# ============================================================
#   APP START
# ============================================================
if __name__ == "__main__":
    # Charts folder exist na kare to bana do
    os.makedirs(CHART_DIR, exist_ok=True)

    print("=" * 50)
    print("  ⚡ EVPULSE Dashboard Server Starting...")
    print("=" * 50)
    print(f"  📂 CSV Path   : {CSV_PATH}")
    print(f"  📊 Charts Dir : {CHART_DIR}")
    print(f"  🌐 URL        : http://localhost:5000")
    print("=" * 50)

    # CSV exist karta hai ya nahi check karo
    if not os.path.exists(CSV_PATH):
        print("  ⚠️  WARNING: CSV file nahi mili!")
        print(f"     '{CSV_PATH}' mein daalo")
    else:
        df_check = pd.read_csv(CSV_PATH)
        print(f"  ✅ CSV Loaded : {len(df_check):,} records found")

    print("=" * 50)

    app.run(debug=True, host="0.0.0.0", port=5000)
