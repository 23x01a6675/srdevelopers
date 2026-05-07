import os
from flask import Flask, render_template, request, redirect, url_for
from datetime import datetime
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = os.path.join(app.root_path, "static", "images")
app.config["WHATSAPP_PHONE"] = "+919876543210"  # Company WhatsApp number
ALLOWED_EXTENSIONS = {"png", "jpg", "jpeg", "gif", "svg"}

# Property types
PROPERTY_TYPES = {
    "Independent": "🏠",
    "Builder Floor": "🏢",
    "Duplex Villa": "🏡",
    "Open Plot": "🌱",
    "2BHK Apartment": "🏘️",
    "3BHK Apartment": "🏛️"
}

# Sample property data (in-memory database)
properties = [
    # Independent Houses
    {"id": 1, "title": "Modern Independent House", "location": "Hyderabad", "price": "₹1.8 Cr", "type": "Independent", "description": "Spacious independent house with 4 bedrooms, modern kitchen, and beautiful garden.", "image_url": "images/independent1.jpg"},
    {"id": 2, "title": "Luxury Independent Villa", "location": "Bangalore", "price": "₹2.5 Cr", "type": "Independent", "description": "Premium independent villa with swimming pool and smart home features.", "image_url": "images/independent2.jpg"},
    
    # Builder Floors
    {"id": 3, "title": "Builder Floor with Terrace", "location": "Delhi", "price": "₹1.2 Cr", "type": "Builder Floor", "description": "3-floor builder floor with terrace space and separate parking.", "image_url": "images/builderfloor1.jpg"},
    {"id": 4, "title": "Modern Builder Floor", "location": "Pune", "price": "₹95 Lakh", "type": "Builder Floor", "description": "Contemporary builder floor with lift access and modern amenities.", "image_url": "images/builderfloor2.jpg"},
    
    # Duplex Villas
    {"id": 5, "title": "Spacious Duplex Villa", "location": "Pune", "price": "₹1.5 Cr", "type": "Duplex Villa", "description": "3-bedroom duplex villa with large garden and guest house.", "image_url": "images/duplex1.jpg"},
    {"id": 6, "title": "Luxury Duplex Villa", "location": "Bangalore", "price": "₹2.2 Cr", "type": "Duplex Villa", "description": "Premium duplex villa with modern architecture and gated community.", "image_url": "images/duplex2.jpg"},
    
    # Open Plots
    {"id": 7, "title": "Prime Location Plot", "location": "Hyderabad", "price": "₹50 Lakh", "type": "Open Plot", "description": "1000 sqft open plot in excellent location with clear title.", "image_url": "images/plot1.jpg"},
    {"id": 8, "title": "Commercial Plot", "location": "Bangalore", "price": "₹75 Lakh", "type": "Open Plot", "description": "2000 sqft commercial plot ideal for business expansion.", "image_url": "images/plot2.jpg"},
    
    # 2BHK Apartments
    {"id": 9, "title": "Modern 2BHK Apartment", "location": "Bangalore", "price": "₹80 Lakh", "type": "2BHK Apartment", "description": "Modern 2BHK apartment in city center with gym and parking.", "image_url": "images/2bhk1.jpg"},
    {"id": 10, "title": "Cozy 2BHK Flat", "location": "Mumbai", "price": "₹1 Cr", "type": "2BHK Apartment", "description": "Well-designed 2BHK apartment with swimming pool and security.", "image_url": "images/2bhk2.jpg"},
    
    # 3BHK Apartments
    {"id": 11, "title": "Spacious 3BHK Apartment", "location": "Pune", "price": "₹1.2 Cr", "type": "3BHK Apartment", "description": "Spacious 3-bedroom apartment with dedicated parking and laundry room.", "image_url": "images/3bhk1.jpg"},
    {"id": 12, "title": "Luxury 3BHK Flat", "location": "Delhi", "price": "₹1.5 Cr", "type": "3BHK Apartment", "description": "Premium 3BHK apartment with panoramic city views and concierge service.", "image_url": "images/3bhk2.jpg"}
]

# Leads management (in-memory database)
leads = [
    {
        "id": 1,
        "name": "John Doe",
        "email": "john@example.com",
        "phone": "+91-9876543210",
        "subject": "Property Inquiry",
        "message": "Interested in luxury villa in Hyderabad",
        "status": "New",
        "created_at": "2024-01-15 10:30:00",
        "property_interest": "Luxury Villa"
    }
]

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/properties")
def available_properties():
    return render_template("properties.html", properties=properties, property_types=PROPERTY_TYPES)

@app.route("/property/<int:property_id>")
def property_detail(property_id):
    property_item = next((p for p in properties if p["id"] == property_id), None)
    return render_template("property.html", property=property_item)

@app.route("/property/<int:property_id>/upload-image", methods=["POST"])
def upload_property_image(property_id):
    property_item = next((p for p in properties if p["id"] == property_id), None)
    if property_item:
        image_file = request.files.get("image_file")
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            property_item["image_url"] = f"images/{filename}"
    return redirect(url_for("property_detail", property_id=property_id))

@app.route("/property/<int:property_id>/delete", methods=["POST"])
def delete_property(property_id):
    global properties
    properties = [p for p in properties if p["id"] != property_id]
    return redirect(url_for("available_properties"))

@app.route("/property/<int:property_id>/edit", methods=["GET", "POST"])
def edit_property(property_id):
    property_item = next((p for p in properties if p["id"] == property_id), None)
    if not property_item:
        return redirect(url_for("available_properties"))
    
    if request.method == "POST":
        image_file = request.files.get("image_file")
        image_url = request.form.get("image_url", "").strip()
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            image_url = f"images/{filename}"
        elif not image_url:
            image_url = property_item["image_url"]  # Keep existing if no new image
        
        property_item["title"] = request.form["title"]
        property_item["location"] = request.form["location"]
        property_item["price"] = request.form["price"]
        property_item["description"] = request.form["description"]
        property_item["image_url"] = image_url
        return redirect(url_for("available_properties"))
    
    return render_template("edit.html", property=property_item)

@app.route("/add", methods=["GET", "POST"])
def add_property():
    if request.method == "POST":
        image_file = request.files.get("image_file")
        image_url = request.form.get("image_url", "").strip()
        if image_file and image_file.filename and allowed_file(image_file.filename):
            filename = secure_filename(image_file.filename)
            save_path = os.path.join(app.config["UPLOAD_FOLDER"], filename)
            image_file.save(save_path)
            image_url = f"images/{filename}"
        if not image_url:
            image_url = "images/default.svg"

        new_id = max([p["id"] for p in properties], default=0) + 1
        new_property = {
            "id": new_id,
            "title": request.form["title"],
            "location": request.form["location"],
            "price": request.form["price"],
            "description": request.form["description"],
            "image_url": image_url
        }
        properties.append(new_property)
        return redirect(url_for("available_properties"))
    return render_template("add.html")

def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/admin")
def admin():
    return render_template("admin.html")

@app.route("/about")
def about():
    return render_template("about.html")

@app.route("/experience")
def experience():
    return render_template("experience.html")

@app.route("/construction-plans")
def construction_plans():
    return render_template("construction_plans.html")

@app.route("/contact", methods=["GET", "POST"])
def contact():
    if request.method == "POST":
        new_lead_id = len(leads) + 1
        new_lead = {
            "id": new_lead_id,
            "name": request.form["name"],
            "email": request.form["email"],
            "phone": request.form["phone"],
            "subject": request.form["subject"],
            "message": request.form["message"],
            "status": "New",
            "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "property_interest": request.form.get("property_interest", "")
        }
        leads.append(new_lead)
        return redirect(url_for("contact_success"))
    return render_template("contact.html")

@app.route("/contact/success")
def contact_success():
    return render_template("contact_success.html")

@app.route("/admin/leads")
def view_leads():
    return render_template("leads.html", leads=leads)

@app.route("/admin/leads/<int:lead_id>/status/<status>")
def update_lead_status(lead_id, status):
    lead = next((l for l in leads if l["id"] == lead_id), None)
    if lead:
        lead["status"] = status
    return redirect(url_for("view_leads"))

@app.route("/admin/leads/<int:lead_id>/delete")
def delete_lead(lead_id):
    global leads
    leads = [l for l in leads if l["id"] != lead_id]
    return redirect(url_for("view_leads"))

if __name__ == "__main__":
    app.run(debug=True)
