from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

PRODUCT_IMAGES = {
    # ── STATIONARY (50) ──
    "Ball Pen Blue":             "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=300&h=300&fit=crop",
    "Mechanical Pencil 0.7mm":   "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=300&h=300&fit=crop",
    "HB Wood Pencil":            "https://images.unsplash.com/photo-1484820540004-14229fe36ca4?w=300&h=300&fit=crop",
    "Colored Pencils 12 Pack":   "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=300&h=300&fit=crop",
    "Spiral Notebook 200pg":     "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=300&h=300&fit=crop",
    "Permanent Marker Pack":     "https://images.unsplash.com/photo-1586075010923-2dd4570fb338?w=300&h=300&fit=crop",
    "Text Highlighters 5pc":     "https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?w=300&h=300&fit=crop",
    "Rubber Eraser Natural":     "https://images.unsplash.com/photo-1606107557195-0e29a4b5b4aa?w=300&h=300&fit=crop",
    "Pencil Sharpener Electric": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=300&h=300&fit=crop",
    "Grid Notebook A5":          "https://images.unsplash.com/photo-1517842645767-c639042777db?w=300&h=300&fit=crop",
    "Sketch Pad 30 Sheets":      "https://images.unsplash.com/photo-1542626991-cbc4e32524cc?w=300&h=300&fit=crop",
    "Complete Geometry Set":     "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300&h=300&fit=crop",
    "No-slip Stapler":           "https://images.unsplash.com/photo-1527443060795-0402a18106b4?w=300&h=300&fit=crop",
    "Transparent Tape Roll":     "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop",
    "PVA Glue Stick Pack":       "https://images.unsplash.com/photo-1614607242041-df196e5c3d14?w=300&h=300&fit=crop",
    "Hardcover Journal":         "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=300&h=300&fit=crop",
    "Fine Liners 12 Colors":     "https://images.unsplash.com/photo-1560785496-3c9d27877182?w=300&h=300&fit=crop",
    "Wax Crayons 24 Pack":       "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=300&h=300&fit=crop",
    "Artist Brush Set 10pc":     "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=300&h=300&fit=crop",
    "Premium Watercolor Set":    "https://images.unsplash.com/photo-1580428180098-24b353d7e9d9?w=300&h=300&fit=crop",
    "Copy Paper 500 Sheets":     "https://images.unsplash.com/photo-1568667256549-094345857637?w=300&h=300&fit=crop",
    "Memo Pads Neon":            "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=300&h=300&fit=crop",
    "Metal Paper Clips 250pc":   "https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=300&h=300&fit=crop",
    "Bamboo Desk Organizer":     "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=300&h=300&fit=crop",
    "Monthly Wall Planner":      "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=300&h=300&fit=crop",
    "Dot Grid Bullet Journal":   "https://images.unsplash.com/photo-1572726729207-a78d6feb18d7?w=300&h=300&fit=crop",
    "Professional Pencil Set":   "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=300&h=300&fit=crop",
    "Luxury Gel Pen Set":        "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=300&h=300&fit=crop",
    "Executive Fountain Pen":    "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=300&fit=crop",
    "Index Card Box 200pc":      "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=300&h=300&fit=crop",
    "Binder Clips Large 12pc":   "https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=300&h=300&fit=crop&sat=50",
    "Correction Fluid White":    "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=300&h=300&fit=crop&sat=-90",
    "Ruler 30cm Transparent":    "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300&h=300&fit=crop&sat=-20",
    "Scissors Stainless Steel":  "https://images.unsplash.com/photo-1562564055-71e051d33c19?w=300&h=300&fit=crop",
    "Compass Drawing Set":       "https://images.unsplash.com/photo-1509228627152-71e5b4d5bc4b?w=300&h=300&fit=crop",
    "A4 Sketch Book 50pg":       "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300&h=300&fit=crop",
    "Pen Holder Ceramic":        "https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=300&h=300&fit=crop",
    "Whiteboard Marker 4pc":     "https://images.unsplash.com/photo-1596496050755-c923e73e42e1?w=300&h=300&fit=crop",
    "Sticky Notes 5x5 100pc":    "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=300&h=300&fit=crop&hue=60",
    "Calligraphy Pen Set":       "https://images.unsplash.com/photo-1593005510329-8a4035a7238f?w=300&h=300&fit=crop",
    "Pastel Chalk Set 24pc":     "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop",
    "Sketch Pencil Set 12pc":    "https://images.unsplash.com/photo-1508615039623-a25605d2b022?w=300&h=300&fit=crop",
    "Acrylic Paint Set 12pc":    "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=300&h=300&fit=crop",
    "Canvas Board A4":           "https://images.unsplash.com/photo-1607457561901-e6ec3a6d16cf?w=300&h=300&fit=crop",
    "Oil Pastel Set 36pc":       "https://images.unsplash.com/photo-1615228402326-7bbd3b017ece?w=300&h=300&fit=crop",
    "Drawing Board A3":          "https://images.unsplash.com/photo-1608501078713-8e445a709b39?w=300&h=300&fit=crop",
    "Craft Scissors Decorative":  "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=300&h=300&fit=crop",
    "Tape Dispenser Desktop":    "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=300&h=300&fit=crop",
    "Letter Tray 3 Tier":        "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=300&h=300&fit=crop",
    "Stamp Pad Ink Blue":        "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop",

    # ── ELECTRONICS (50) ──
    "Scientific Calculator":     "https://images.unsplash.com/photo-1611532736597-de2d4265fba3?w=300&h=300&fit=crop&hue=200",
    "Wired In-ear Earphones":    "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop",
    "USB-C Data Cable 2m":       "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop",
    "Wireless Mouse 2.4GHz":     "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=300&h=300&fit=crop",
    "RGB Gaming Keyboard":       "https://images.unsplash.com/photo-1595225476474-87563907ef1b?w=300&h=300&fit=crop",
    "LED Desk Lamp USB":         "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop",
    "Over-ear Bluetooth Headphones": "https://images.unsplash.com/photo-1546435770-a3e426bf472b?w=300&h=300&fit=crop",
    "Fitness Tracker Band":      "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300&h=300&fit=crop",
    "USB Hub 4 Port":            "https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=300&h=300&fit=crop",
    "Webcam 1080p HD":           "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=300&h=300&fit=crop",
    "Portable Charger 10000mAh": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=300&h=300&fit=crop",
    "Bluetooth Speaker Mini":    "https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=300&h=300&fit=crop",
    "Screen Cleaning Kit":       "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop&hue=180",
    "Laptop Cooling Pad":        "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=300&h=300&fit=crop&hue=200",
    "HDMI Cable 2m":             "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop&hue=120",
    "Memory Card 32GB":          "https://images.unsplash.com/photo-1631643889786-4e7c9e744dc4?w=300&h=300&fit=crop",
    "USB Flash Drive 64GB":      "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=300&h=300&fit=crop",
    "Phone Stand Adjustable":    "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop",
    "Laptop Stand Aluminium":    "https://images.unsplash.com/photo-1612831455543-a70a0e769a43?w=300&h=300&fit=crop",
    "Wireless Charger Pad":      "https://images.unsplash.com/photo-1614624532983-4ce03382d63d?w=300&h=300&fit=crop",
    "LED Strip Lights 5m":       "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=280",
    "Smart Plug WiFi":           "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop",
    "Keyboard Wrist Rest":       "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop",
    "Mouse Pad XL Gaming":       "https://images.unsplash.com/photo-1616348436168-de43ad0db179?w=300&h=300&fit=crop",
    "Cable Organizer Clips":     "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&sat=-50",
    "Earphone Case Hard":        "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=300&h=300&fit=crop&sat=-30",
    "Laptop Bag Sleeve 15in":    "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop",
    "Numeric Keypad USB":        "https://images.unsplash.com/photo-1595225476474-87563907ef1b?w=300&h=300&fit=crop&sat=-40",
    "Monitor Light Bar":         "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop&hue=60",
    "Gamepad Controller USB":    "https://images.unsplash.com/photo-1593305841991-05c297ba4575?w=300&h=300&fit=crop",
    "Bluetooth Keyboard Mini":   "https://images.unsplash.com/photo-1561112078-7d24e04c3407?w=300&h=300&fit=crop",
    "Digital Alarm Clock":       "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=300&h=300&fit=crop&hue=200",
    "Extension Board 6 Socket":  "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop&hue=60",
    "Cable USB-A to Micro":      "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop&sat=-20",
    "Phone Camera Lens Kit":     "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300&h=300&fit=crop",
    "Portable Mini Fan USB":     "https://images.unsplash.com/photo-1561330256-9b96c4b39c4a?w=300&h=300&fit=crop",
    "Earbuds TWS Wireless":      "https://images.unsplash.com/photo-1572569511254-d8f925fe2cbb?w=300&h=300&fit=crop",
    "Drawing Tablet Small":      "https://images.unsplash.com/photo-1561883088-039e53143d73?w=300&h=300&fit=crop",
    "Pocket Projector Mini":     "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=300&fit=crop&hue=200",
    "Smart LED Bulb WiFi":       "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=60",
    "Keyboard Backlit USB":      "https://images.unsplash.com/photo-1595225476474-87563907ef1b?w=300&h=300&fit=crop&hue=280",
    "VR Headset Mobile":         "https://images.unsplash.com/photo-1622979135225-d2ba269cf1ac?w=300&h=300&fit=crop",
    "Action Camera Mini":        "https://images.unsplash.com/photo-1526170375885-4d8ecf77b99f?w=300&h=300&fit=crop",
    "Digital Scale 5kg":         "https://images.unsplash.com/photo-1543362906-acfc16c67564?w=300&h=300&fit=crop",
    "FM Radio Portable":         "https://images.unsplash.com/photo-1563330232-57114bb0823c?w=300&h=300&fit=crop",
    "Electric Eraser USB":       "https://images.unsplash.com/photo-1508615039623-a25605d2b022?w=300&h=300&fit=crop&hue=200",
    "Webcam Cover Slider":       "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=300&h=300&fit=crop&sat=-60",
    "Type-C Hub 7in1":           "https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=300&h=300&fit=crop&hue=60",
    "Ring Light 10inch":         "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300&h=300&fit=crop&hue=60",
    "Noise Machine Sleep":       "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop&sat=-40",

    # ── BAGS (50) ──
    "Canvas School Bag":         "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop",
    "Neoprene Laptop Sleeve":    "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&sat=-30",
    "Hiking Daypack 25L":        "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop",
    "Rolling Trolley Bag":       "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop",
    "Gym Duffle Bag":            "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=120",
    "Tote Bag Canvas Large":     "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop",
    "Waterproof Dry Bag 10L":    "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&hue=200",
    "Laptop Backpack 30L":       "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop",
    "Mini Crossbody Bag":        "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop",
    "Travel Packing Cubes 4pc":  "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=-20",
    "Camera Bag Shoulder":       "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&hue=30",
    "Tactical Backpack 45L":     "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=-50",
    "Fanny Pack Waist Bag":      "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=60",
    "College Backpack 20L":      "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&hue=30",
    "Diaper Bag Multifunction":  "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&hue=30",
    "Drawstring Bag Sport":      "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-30",
    "Leather Messenger Bag":     "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=30",
    "Foldable Shopping Bag":     "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=-40",
    "Hard Shell Suitcase 20in":  "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&hue=60",
    "Document Holder Bag":       "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&sat=20",
    "String Backpack Mesh":      "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&sat=-40",
    "Laptop Sleeve 13inch":      "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&hue=60",
    "Backpack Rain Cover":       "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&hue=120",
    "Lunch Bag Insulated":       "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=30",
    "Shoulder Bag Oxford":       "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=180",
    "Travel Neck Pouch":         "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&hue=60",
    "Kids School Bag":           "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=280",
    "Trekking Bag 60L":          "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=20",
    "Pouch Set 3pc":             "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=-20",
    "Tool Bag Canvas":           "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&hue=60",
    "Sports Backpack 35L":       "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=30",
    "Yoga Mat Bag":              "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&hue=120",
    "Drawstring Bag Printed":    "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&hue=180",
    "College Sling Bag":         "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=240",
    "Expandable Duffel 40L":     "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=20",
    "Anti-Theft Backpack":       "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&sat=20",
    "Leather Wallet Bag":        "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=40",
    "Book Bag with Handle":      "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=20",
    "Weekender Bag Duffel":      "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&hue=180",
    "Transparent PVC Bag":       "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-60",
    "Backpack Chest Strap":      "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=30",
    "Mini Backpack Cute":        "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=320",
    "Eco Jute Bag":              "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=-20",
    "Garment Bag Travel":        "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&hue=180",
    "Briefcase Laptop Bag":      "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=120",
    "Compression Packing Bag":   "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=-40",
    "Bottle Holder Bag":         "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&sat=-20",
    "Shoe Bag Travel":           "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-20",
    "Pencil Case Large":         "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=40",
    "Pouch Waterproof Phone":    "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=-40",

    # ── ACCESSORIES (50) ──
    "Stainless Steel Water Bottle": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop",
    "Steel Lunch Box Compartment":  "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop&sat=20",
    "Polarized UV Sunglasses":      "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&sat=30",
    "Genuine Leather Wallet":       "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop",
    "Canvas Web Belt":              "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-70",
    "Quartz Wrist Watch":           "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop",
    "Copper Water Bottle":          "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=30",
    "Titanium Metal Watch":         "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&sat=-30",
    "Polarized Sports Goggles":     "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&hue=180",
    "Card Holder Slim":             "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&sat=-20",
    "Travel Pillow Neck":           "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=30",
    "Umbrella Auto Open":           "https://images.unsplash.com/photo-1520923642038-b4259acecbd7?w=300&h=300&fit=crop",
    "Leather Keyholder":            "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&hue=30",
    "Insulated Flask 750ml":        "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&sat=-20",
    "Sports Wristband 2pc":         "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300&h=300&fit=crop&sat=-40",
    "Pocket Knife Swiss":           "https://images.unsplash.com/photo-1562114808-b4b33cf6e7b5?w=300&h=300&fit=crop",
    "Silicone Watch Band":          "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&hue=120",
    "Carabiner Clip 4pc":           "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=-60",
    "Bamboo Sunglasses":            "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&sat=-20",
    "Coin Purse Leather":           "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&sat=30",
    "Phone Pop Socket":             "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop&hue=60",
    "Magnetic Phone Mount":         "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop&hue=180",
    "Luggage Tag Leather":          "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=-60",
    "Passport Holder":              "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&hue=60",
    "Sunscreen Stick SPF50":        "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop",
    "Watch Winder Single":          "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&hue=30",
    "Tie Clip Silver":              "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=300&h=300&fit=crop",
    "Cufflinks Formal":             "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=300&h=300&fit=crop&sat=-30",
    "Hair Tie Set 20pc":            "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop&hue=280",
    "Scrunchie Set 5pc":            "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop&hue=320",
    "Headband Sports":              "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300&h=300&fit=crop&hue=60",
    "Cooling Towel Sport":          "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300&h=300&fit=crop&sat=20",
    "Bottle Opener Keychain":       "https://images.unsplash.com/photo-1562114808-b4b33cf6e7b5?w=300&h=300&fit=crop&sat=-30",
    "Pen Knife Multi Tool":         "https://images.unsplash.com/photo-1562114808-b4b33cf6e7b5?w=300&h=300&fit=crop&hue=60",
    "Slim Bifold Wallet":           "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&hue=180",
    "Compression Socks 3pc":        "https://images.unsplash.com/photo-1584735175315-9d5df23be4be?w=300&h=300&fit=crop",
    "Cap Baseball Cotton":          "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=300&h=300&fit=crop",
    "Beanie Woolen Cap":            "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=300&h=300&fit=crop&hue=60",
    "Scarf Soft Cotton":            "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=300&h=300&fit=crop",
    "Gloves Touch Screen":          "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=300&h=300&fit=crop&hue=180",
    "Sunglasses Case Hard":         "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&sat=-50",
    "Pen Organizer Leather":        "https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=300&h=300&fit=crop&hue=30",
    "Phone Lanyard Neck":           "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop&sat=-20",
    "Wax Shoe Polish Kit":          "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-30",
    "Shoe Horn Long":               "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-60",
    "Travel Adapter Universal":     "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop&hue=120",
    "Silicone Cable Tie 10pc":      "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&sat=-30",
    "Microfiber Cloth 5pc":         "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop&sat=-40",
    "Lens Cleaning Pen":            "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300&h=300&fit=crop&sat=-40",
    "Collapsible Water Cup":        "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=120",

    # ── FOOTWEAR (50) ──
    "Running Sports Shoes":      "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
    "Foam Flip Flops":           "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop",
    "Leather Casual Shoes":      "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop",
    "Canvas Sneakers White":     "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop",
    "Trekking Sandals":          "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=30",
    "High Top Sneakers":         "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=200",
    "Formal Oxford Shoes":       "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&sat=-20",
    "Rain Boots Waterproof":     "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop",
    "Slippers Memory Foam":      "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=-30",
    "Sports Sandals":            "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=60",
    "Ankle Boots Chelsea":       "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=30",
    "Ballet Flats Women":        "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop",
    "Loafers Slip-on Men":       "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=30",
    "Platform Sneakers":         "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=60",
    "Moccasins Suede":           "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=60",
    "Sandals Flat Casual":       "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=120",
    "Trail Running Shoes":       "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=30",
    "Espadrilles Canvas":        "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&sat=-20",
    "Work Boots Steel Toe":      "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&sat=-30",
    "Gym Training Shoes":        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=20",
    "Wedge Heels Women":         "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&hue=30",
    "Clogs Wooden Sole":         "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&sat=-40",
    "Boat Shoes Deck":           "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=120",
    "Sandals Kolhapuri":         "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=30",
    "Slip Resistant Kitchen":    "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-40",
    "Hiking Boots Mid":          "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=60",
    "Dress Sandals Heeled":      "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&hue=60",
    "Kids Sports Shoes":         "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=280",
    "Breathable Mesh Shoes":     "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-20",
    "Slip-on Vans Style":        "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&sat=20",
    "Formal Derby Shoes":        "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&sat=20",
    "Open Toe Heels":            "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&sat=20",
    "Snow Boots Warm":           "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&sat=20",
    "Casual Chukka Boots":       "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=120",
    "Pool Slides Comfort":       "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=-50",
    "Woven Flat Sandals":        "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=180",
    "Sneakers Chunky Sole":      "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&sat=40",
    "Driving Moccasins":         "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=180",
    "Toe Ring Sandals":          "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=240",
    "Faux Leather Boots":        "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=180",
    "Jelly Sandals Kids":        "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=280",
    "Athleisure Shoes":          "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=60",
    "Platform Sandals":          "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&sat=30",
    "Lace-up Canvas Shoes":      "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=120",
    "Gum Sole Sneakers":         "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=180",
    "Rubber Rain Sandals":       "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=-20",
    "Toe Post Flip Flops":       "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=320",
    "Walking Shoes Wide":        "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=120",
    "Ankle Strap Heels":         "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&hue=120",
    "Barefoot Minimalist":       "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-60",
}

LIMITED_OFFER_CATEGORIES = {
    "electronic": {"label": "⚡ Flash Sale", "hours": 6},
    "footwear":   {"label": "👟 Weekend Deal", "hours": 24},
    "bag":        {"label": "🎒 Limited Stock", "hours": 12},
}

def get_image_url(name):
    return PRODUCT_IMAGES.get(
        name,
        f"https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=300&h=300&fit=crop"
    )

def get_offer(category):
    return LIMITED_OFFER_CATEGORIES.get(category, None)

def db():
    conn = sqlite3.connect("store.db")
    conn.row_factory = sqlite3.Row
    return conn

def get_cart_count():
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT COUNT(*) as cnt FROM cart")
    cnt = cur.fetchone()["cnt"]
    conn.close()
    return cnt

def enrich(products):
    for p in products:
        p['image_url'] = get_image_url(p['name'])
        p['offer'] = get_offer(p['category'])
        # Calculate discount percentage
        orig = p.get('original_price', 0)
        price = p.get('price', 0)
        if orig and orig > price:
            p['discount'] = round((1 - price / orig) * 100)
        else:
            p['discount'] = 0
    return products

@app.route("/")
def home():
    conn = db()
    cur = conn.cursor()
    category = request.args.get("category", "all")
    if category and category != "all":
        cur.execute("SELECT * FROM products WHERE category=?", (category,))
    else:
        cur.execute("SELECT * FROM products")
    products = enrich([dict(p) for p in cur.fetchall()])
    conn.close()
    return render_template("index.html", products=products, cart_count=get_cart_count(), active_category=category)

@app.route("/product/<int:id>")
def product(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE id=?", (id,))
    row = cur.fetchone()
    if not row:
        conn.close()
        return "Product not found", 404
    product = dict(row)
    product['image_url'] = get_image_url(product['name'])
    product['offer'] = get_offer(product['category'])
    cur.execute("SELECT * FROM products WHERE category=? AND id!=? LIMIT 4", (product['category'], id))
    rec = enrich([dict(r) for r in cur.fetchall()])
    conn.close()
    return render_template("product.html", product=product, rec=rec, cart_count=get_cart_count())

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)", ('%' + q + '%',))
    products = enrich([dict(p) for p in cur.fetchall()])
    rec = []
    if products:
        cur.execute("SELECT * FROM products WHERE category=? AND id!=? LIMIT 4",
                    (products[0]["category"], products[0]["id"]))
        rec = enrich([dict(r) for r in cur.fetchall()])
    conn.close()
    return render_template("products.html", products=products, rec=rec, query=q, cart_count=get_cart_count())

@app.route("/addcart/<int:id>")
def addcart(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("INSERT INTO cart(product_id) VALUES(?)", (id,))
    conn.commit()
    conn.close()
    return redirect("/cart")

@app.route("/removecart/<int:id>")
def removecart(id):
    conn = db()
    cur = conn.cursor()
    cur.execute("DELETE FROM cart WHERE id=?", (id,))
    conn.commit()
    conn.close()
    return redirect("/cart")

@app.route("/cart")
def cart():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT cart.id, products.name, products.price, products.image,
               products.id as product_id, products.category
        FROM cart JOIN products ON cart.product_id = products.id
    """)
    items = [dict(i) for i in cur.fetchall()]
    for item in items:
        item['image_url'] = get_image_url(item['name'])
        item['offer'] = get_offer(item['category'])
    total = sum(item["price"] for item in items)
    conn.close()
    return render_template("cart.html", items=items, total=total, cart_count=get_cart_count())

@app.route("/admin")
def admin():
    return render_template("admin.html", cart_count=get_cart_count())

if __name__ == "__main__":
    app.run(debug=True)