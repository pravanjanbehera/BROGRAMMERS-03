import os
import pandas as pd


import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt


def create_graphs():

   
    if not os.path.exists("waste_data.csv"):
        return

    
    data = pd.read_csv("waste_data.csv")

    
    data["area"] = data["area"].str.strip().str.title()

   
    data["date"] = pd.to_datetime(data["date"])

    
    os.makedirs("static/graphs", exist_ok=True)

   
    waste_count = data["waste_type"].value_counts()

    plt.figure()
    waste_count.plot(kind="bar")
    plt.title("Waste Type Trend")
    plt.xlabel("Waste Type")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/graphs/waste_trend.png")
    plt.close()

   
    area_count = data["area"].value_counts()

    plt.figure()
    area_count.plot(kind="pie", autopct="%1.1f%%")
    plt.title("Area-wise Waste Generation")
    plt.ylabel("")
    plt.tight_layout()
    plt.savefig("static/graphs/area_wise.png")
    plt.close()

   
    impact_count = data["impact"].value_counts()

    plt.figure()
    impact_count.plot(kind="bar")
    plt.title("Environmental Impact Levels")
    plt.xlabel("Impact")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/graphs/impact.png")
    plt.close()

    
    date_trend = data.groupby("date").size()

    plt.figure()
    date_trend.plot(kind="line", marker="o")
    plt.title("Date-wise Waste Generation Trend")
    plt.xlabel("Date")
    plt.ylabel("Entries")
    plt.tight_layout()
    plt.savefig("static/graphs/date_trend.png")
    plt.close()


    def disposal_method(waste):
        if waste == "Organic":
            return "Compost"
        elif waste in ("Paper", "metal"):
            return "Recycle"
        else:
            return "Landfill"

    data["disposal"] = data["waste_type"].apply(disposal_method)
    disposal_count = data["disposal"].value_counts()

    plt.figure()
    disposal_count.plot(kind="bar")
    plt.title("Disposal Method Summary")
    plt.xlabel("Method")
    plt.ylabel("Count")
    plt.tight_layout()
    plt.savefig("static/graphs/disposal_summary.png")
    plt.close()


    hotspot_score = data["area"].value_counts()

    plt.figure()
    hotspot_score.plot(kind="bar")
    plt.title("Waste Hotspot Score by Area")
    plt.xlabel("Area")
    plt.ylabel("Score")
    plt.tight_layout()
    plt.savefig("static/graphs/hotspot_score.png")
    plt.close()
