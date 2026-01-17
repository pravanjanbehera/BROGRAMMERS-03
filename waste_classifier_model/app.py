import os
from flask import Flask, render_template, request
from werkzeug.utils import secure_filename


from data_store import save_waste_data
from dashboard_logic import create_graphs
from module1 import analyze_waste_image, classify_hotspot
from module56 import smart_action_recommendation, environmental_impact_message



BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "static", "uploads")

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER



@app.route("/", methods=["GET", "POST"])
def home():

    label = hotspot = smart_action = impact_message = None
    detected_object = None
    image_name = None

    if request.method == "POST":
        area = request.form.get("area")
        image = request.files.get("image")

        if image:
           
            filename = secure_filename(image.filename)
            image_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image.save(image_path)

            label, risk, detected_object = analyze_waste_image(image_path)
            hotspot = classify_hotspot(risk)

         
            smart_action = smart_action_recommendation(label)
            impact_message = environmental_impact_message(label)

         
            save_waste_data(area, label, hotspot)

            image_name = filename

    return render_template(
        "index.html",
        label=label,
        hotspot=hotspot,
        smart_action=smart_action,
        impact_message=impact_message,
        detected_object=detected_object,
        image=image_name
    )



@app.route("/dashboard")
def dashboard():
    create_graphs()
    return render_template("dashboard.html")


if __name__ == "__main__":
    app.run(debug=True)
