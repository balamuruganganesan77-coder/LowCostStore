from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Auto-create DB on first deploy
if not os.path.exists("store.db"):
    import subprocess
    subprocess.run(["python", "database.py"])

PRODUCT_IMAGES = {
    # STATIONARY
    "Ball Pen Blue": "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=300&h=300&fit=crop",
    "HB Wood Pencil": "https://images.unsplash.com/photo-1513364776144-60967b0f800f?w=300&h=300&fit=crop",
    "Colored Pencils 12 Pack": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=300&h=300&fit=crop",
    "Spiral Notebook 200pg": "https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=300&h=300&fit=crop",
    "Permanent Marker Pack": "https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=300&h=300&fit=crop",
    "Text Highlighters 5pc": "https://images.unsplash.com/photo-1456735190827-d1262f71b8a3?w=300&h=300&fit=crop",
    "Rubber Eraser Natural": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop",
    "Pencil Sharpener Electric": "https://images.unsplash.com/photo-1503676260728-1c00da094a0b?w=300&h=300&fit=crop",
    "Grid Notebook A5": "https://images.unsplash.com/photo-1517842645767-c639042777db?w=300&h=300&fit=crop",
    "Sketch Pad 30 Sheets": "https://images.unsplash.com/photo-1542626991-cbc4e32524cc?w=300&h=300&fit=crop",
    "Mechanical Pencil 0.7mm": "https://www.amazon.in/sspa/click?ie=UTF8&spc=MTo4MTQyMDMwNDk5Nzc4OTM3OjE3NzU0ODQ3Mzk6c3BfYXRmOjMwMDI4OTQ1MzgxNzkzMjo6MDo6&url=%2FUni-ball-Shalaku-M7-228-Mechanical-Pencil%2Fdp%2FB07T1LLL2X%2Fref%3Dsr_1_1_sspa%3Fadgrpid%3D1320515070110695%26dib%3DeyJ2IjoiMSJ9.tp2JNs9fXvO7xtMMlf9972Ml1ntQ98Hg7W2JnCD-v3xHOaDmQja_rXq42FCBxJ746UG4rA3cY8czDOk_DJfqlOsPBkI8qnP-79BYgd1WGoPY6WScz_0kK8Gztam_84xr-iT_C1Jaa6FS4H0j7lcFjRirSuS3N-_Q_CvmfF1i30cl86CttPPbr0IU1wueiAUoZssaNxseo963X-KLK3cfuSLp2XZB5YWgPO45-Y9Nb0OWJuAmMl_dQQ5n29OKSID7IKahY4pDI_0DXj76fOg7bxW-076-EwTd5aH_bIkfi-Q.t3PjYPIi9GksqO5G1wB0gznYs_ULJ4S8v7eYsutX2Yc%26dib_tag%3Dse%26hvadid%3D82532450897272%26hvbmt%3Dbp%26hvdev%3Dc%26hvlocphy%3D149021%26hvnetw%3Do%26hvqmt%3Dp%26hvtargid%3Dkwd-82533067977752%253Aloc-90%26hydadcr%3D1533_1970181%26keywords%3D7mm%2Bpencil%26mcid%3Da13707f6e1953c9cb8ff695644dbb5a3%26msclkid%3D69f3697bf82910b4e88900a847165f1d%26qid%3D1775484738%26sr%3D8-1-spons%26aref%3DJJdfCdnpdY%26sp_csd%3Dd2lkZ2V0TmFtZT1zcF9hdGY%26psc%3D1&aref=JJdfCdnpdY&sp_cr=ZAZ",
    "Complete Geometry Set": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300&h=300&fit=crop",
    "No-slip Stapler": "https://images.unsplash.com/photo-1527443060795-0402a18106b4?w=300&h=300&fit=crop",
    "Transparent Tape Roll": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop",
    "PVA Glue Stick Pack": "https://images.unsplash.com/photo-1614607242041-df196e5c3d14?w=300&h=300&fit=crop",
    "Hardcover Journal": "https://images.unsplash.com/photo-1455390582262-044cdead277a?w=300&h=300&fit=crop",
    "Fine Liners 12 Colors": "https://images.unsplash.com/photo-1560785496-3c9d27877182?w=300&h=300&fit=crop",
    "Wax Crayons 24 Pack": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop",
    "Artist Brush Set 10pc": "https://images.unsplash.com/photo-1598300042247-d088f8ab3a91?w=300&h=300&fit=crop",
    "Premium Watercolor Set": "https://images.unsplash.com/photo-1580428180098-24b353d7e9d9?w=300&h=300&fit=crop",
    "Copy Paper 500 Sheets": "https://images.unsplash.com/photo-1568667256549-094345857637?w=300&h=300&fit=crop",
    "Memo Pads Neon": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=300&h=300&fit=crop",
    "Metal Paper Clips 250pc": "https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=300&h=300&fit=crop",
    "Bamboo Desk Organizer": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=300&h=300&fit=crop",
    "Monthly Wall Planner": "https://images.unsplash.com/photo-1506784365847-bbad939e9335?w=300&h=300&fit=crop",
    "Dot Grid Bullet Journal": "https://images.unsplash.com/photo-1572726729207-a78d6feb18d7?w=300&h=300&fit=crop",
    "Professional Pencil Set": "https://images.unsplash.com/photo-1515378791036-0648a3ef77b2?w=300&h=300&fit=crop",
    "Luxury Gel Pen Set": "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=300&h=300&fit=crop&sat=30",
    "Executive Fountain Pen": "https://images.unsplash.com/photo-1478720568477-152d9b164e26?w=300&h=300&fit=crop",
    "Index Card Box 200pc": "https://images.unsplash.com/photo-1553729459-efe14ef6055d?w=300&h=300&fit=crop",
    "Binder Clips Large 12pc": "https://images.unsplash.com/photo-1618160702438-9b02ab6515c9?w=300&h=300&fit=crop&hue=180",
    "Correction Fluid White": "https://images.unsplash.com/photo-1527443060795-0402a18106b4?w=300&h=300&fit=crop&sat=-50",
    "Ruler 30cm Transparent": "https://images.unsplash.com/photo-1509228468518-180dd4864904?w=300&h=300&fit=crop&hue=60",
    "Scissors Stainless Steel": "https://images.unsplash.com/photo-1562564055-71e051d33c19?w=300&h=300&fit=crop",
    "Compass Drawing Set": "https://images.unsplash.com/photo-1509228627152-71e5b4d5bc4b?w=300&h=300&fit=crop",
    "A4 Sketch Book 50pg": "https://images.unsplash.com/photo-1544716278-ca5e3f4abd8c?w=300&h=300&fit=crop",
    "Pen Holder Ceramic": "https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=300&h=300&fit=crop",
    "Whiteboard Marker 4pc": "https://images.unsplash.com/photo-1596496050755-c923e73e42e1?w=300&h=300&fit=crop",
    "Sticky Notes 5x5 100pc": "https://images.unsplash.com/photo-1586281380349-632531db7ed4?w=300&h=300&fit=crop&hue=60",
    "Calligraphy Pen Set": "https://images.unsplash.com/photo-1593005510329-8a4035a7238f?w=300&h=300&fit=crop",
    "Pastel Chalk Set 24pc": "https://images.unsplash.com/photo-1513542789411-b6a5d4f31634?w=300&h=300&fit=crop&hue=30",
    "Sketch Pencil Set 12pc": "https://images.unsplash.com/photo-1508615039623-a25605d2b022?w=300&h=300&fit=crop",
    "Acrylic Paint Set 12pc": "https://images.unsplash.com/photo-1541961017774-22349e4a1262?w=300&h=300&fit=crop",
    "Canvas Board A4": "https://images.unsplash.com/photo-1607457561901-e6ec3a6d16cf?w=300&h=300&fit=crop",
    "Oil Pastel Set 36pc": "https://images.unsplash.com/photo-1615228402326-7bbd3b017ece?w=300&h=300&fit=crop",
    "Drawing Board A3": "https://images.unsplash.com/photo-1608501078713-8e445a709b39?w=300&h=300&fit=crop",
    "Craft Scissors Decorative": "https://images.unsplash.com/photo-1563861826100-9cb868fdbe1c?w=300&h=300&fit=crop",
    "Tape Dispenser Desktop": "https://images.unsplash.com/photo-1497366754035-f200968a6e72?w=300&h=300&fit=crop",
    "Letter Tray 3 Tier": "https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=300&h=300&fit=crop",
    "Stamp Pad Ink Blue": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop",
    # HOME APPLIANCES
    "Table Fan 3 Speed": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop",
    "Ceiling Fan 48inch": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=30",
    "Wall Fan 400mm": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=60",
    "Exhaust Fan Kitchen": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=90",
    "Air Cooler 20L": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop&hue=200",
    "Room Heater 2000W": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop",
    "Mixer Grinder 750W": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop",
    "Wet Grinder 2L": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=30",
    "Juicer Mixer 500W": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=300&fit=crop",
    "Hand Blender 300W": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=60",
    "Electric Kettle 1.5L": "https://images.unsplash.com/photo-1544787219-7f47ccb76574?w=300&h=300&fit=crop",
    "Sandwich Maker": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=300&h=300&fit=crop",
    "Induction Cooktop": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=120",
    "Gas Stove 2 Burner": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=150",
    "Pressure Cooker 5L": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=180",
    "Rice Cooker 1.8L": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=210",
    "Microwave 20L": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=300&h=300&fit=crop",
    "OTG Oven 28L": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=300&h=300&fit=crop&hue=30",
    "Air Fryer 4L": "https://images.unsplash.com/photo-1574269909862-7e1d70bb8078?w=300&h=300&fit=crop&hue=60",
    "Electric Iron 1000W": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=180",
    "Steam Iron 1600W": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=210",
    "Clothes Dryer": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=240",
    "Washing Machine 6kg": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=270",
    "Water Purifier RO": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=180",
    "Water Dispenser": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=200",
    "Refrigerator 190L": "https://images.unsplash.com/photo-1584568694244-14fbdf83bd30?w=300&h=300&fit=crop",
    "Vacuum Cleaner 1200W": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=300",
    "Chimney 60cm": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=240",
    "Dishwasher 8 Place": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=320",
    "Electric Grill": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=300&h=300&fit=crop&hue=30",
    "Coffee Maker 600W": "https://images.unsplash.com/photo-1495474472287-4d71bcdd2085?w=300&h=300&fit=crop",
    "Pop Up Toaster": "https://images.unsplash.com/photo-1528735602780-2552fd46c7af?w=300&h=300&fit=crop&hue=60",
    "Food Processor": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=270",
    "Hand Mixer 250W": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=300",
    "Roti Maker": "https://images.unsplash.com/photo-1556909114-f6e7ad7d3136?w=300&h=300&fit=crop&hue=330",
    "Egg Boiler": "https://images.unsplash.com/photo-1490645935967-10de6ba17061?w=300&h=300&fit=crop&hue=30",
    "Sewing Machine": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&sat=-30",
    "Iron Box Steam 2000W": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=150",
    "Mosquito Killer": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop&hue=30",
    "Room Freshener": "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop",
    "Extension Cord 5m": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop",
    "LED Bulb 12W Pack": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop&hue=60",
    "Ceiling Light": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop&hue=90",
    "Night Lamp": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop&hue=120",
    "Door Bell Wireless": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop&hue=30",
    "CCTV Camera": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=300&h=300&fit=crop",
    "Smart Switch WiFi": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop&hue=60",
    "Inverter Battery": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop&hue=90",
    "Solar Light Outdoor": "https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=300&h=300&fit=crop&hue=150",
    "Power Strip Surge": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop&hue=120",
    # MOBILES & LAPTOPS
    "Budget Smartphone 4G": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop",
    "Mid Range Phone 5G": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=30",
    "Premium Phone 5G": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=60",
    "Gaming Phone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=280",
    "Foldable Phone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=120",
    "Rugged Smartphone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&sat=-30",
    "Elderly Phone Large": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=150",
    "Kids Smartphone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=180",
    "Dual SIM Phone": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=200",
    "Camera Phone 108MP": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300&h=300&fit=crop",
    "Basic Laptop 15in": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop",
    "Student Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&hue=30",
    "Business Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&hue=60",
    "Gaming Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&hue=280",
    "Ultra Thin Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&sat=-20",
    "2-in-1 Laptop Tablet": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&hue=120",
    "MacBook Style Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&sat=-40",
    "Budget Laptop 14in": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&hue=150",
    "Laptop 17inch": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&hue=180",
    "Refurbished Laptop": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&hue=200",
    "Tablet 10inch": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300&h=300&fit=crop",
    "Tablet with Keyboard": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300&h=300&fit=crop&hue=30",
    "Kids Learning Tablet": "https://images.unsplash.com/photo-1544244015-0df4b3ffc6b0?w=300&h=300&fit=crop&hue=280",
    "Drawing Tablet Pro": "https://images.unsplash.com/photo-1561883088-039e53143d73?w=300&h=300&fit=crop",
    "Graphic Tablet": "https://images.unsplash.com/photo-1561883088-039e53143d73?w=300&h=300&fit=crop&hue=30",
    "Phone Screen Protector": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&sat=-60",
    "Phone Back Cover": "https://images.unsplash.com/photo-1511707171634-5f897ff02aa9?w=300&h=300&fit=crop&hue=240",
    "Phone Holder Car": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop",
    "Fast Charger 65W": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=300&h=300&fit=crop",
    "Wireless Charger 15W": "https://images.unsplash.com/photo-1614624532983-4ce03382d63d?w=300&h=300&fit=crop",
    "Power Bank 20000mAh": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=300&h=300&fit=crop&hue=30",
    "Data Cable Braided": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop",
    "OTG Adapter": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop&hue=30",
    "Memory Card 128GB": "https://images.unsplash.com/photo-1631643889786-4e7c9e744dc4?w=300&h=300&fit=crop",
    "SIM Card Ejector": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop&sat=-40",
    "Laptop Charger Universal": "https://images.unsplash.com/photo-1609091839311-d5365f9ff1c5?w=300&h=300&fit=crop&hue=60",
    "Laptop Cooling Fan": "https://images.unsplash.com/photo-1593642632559-0c6d3fc62b89?w=300&h=300&fit=crop",
    "Laptop RAM 8GB": "https://images.unsplash.com/photo-1631643889786-4e7c9e744dc4?w=300&h=300&fit=crop&hue=30",
    "SSD 256GB": "https://images.unsplash.com/photo-1597872200969-2b65d56bd16b?w=300&h=300&fit=crop",
    "Laptop Keyboard Cover": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop",
    "Mouse Wireless Laptop": "https://images.unsplash.com/photo-1527864550417-7fd91fc51a46?w=300&h=300&fit=crop",
    "Laptop Backpack Pro": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop",
    "Screen Cleaning Spray": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop",
    "USB-C Hub 6in1": "https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=300&h=300&fit=crop",
    "Bluetooth Adapter USB": "https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=300&h=300&fit=crop&hue=30",
    "WiFi Adapter USB": "https://images.unsplash.com/photo-1625895197185-efcec01cffe0?w=300&h=300&fit=crop&hue=60",
    "HDMI Adapter TypeC": "https://images.unsplash.com/photo-1588872657578-7efd1f1555ed?w=300&h=300&fit=crop&hue=60",
    "Laptop Stand Foldable": "https://images.unsplash.com/photo-1612831455543-a70a0e769a43?w=300&h=300&fit=crop",
    "Privacy Screen Filter": "https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=300&h=300&fit=crop&sat=-60",
    "Phone Sanitizer UV": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop&hue=280",
    # MEDICAL
    "Digital Thermometer": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop",
    "Blood Pressure Monitor": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop",
    "Pulse Oximeter": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=30",
    "Glucometer Kit": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=60",
    "Nebulizer Machine": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=30",
    "Heating Pad Electric": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=90",
    "Ice Bag Therapy": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=200",
    "First Aid Box": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=0",
    "Bandage Crepe 4in": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&sat=-20",
    "Cotton Roll 400g": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&sat=-40",
    "Surgical Gloves 50pc": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=120",
    "Face Mask N95 10pc": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=150",
    "Sanitizer 500ml": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=180",
    "Antiseptic Solution": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=210",
    "Digital BP Wrist": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=60",
    "Stethoscope": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=90",
    "Weighing Scale Body": "https://images.unsplash.com/photo-1543362906-acfc16c67564?w=300&h=300&fit=crop",
    "Baby Weighing Scale": "https://images.unsplash.com/photo-1543362906-acfc16c67564?w=300&h=300&fit=crop&hue=30",
    "Infrared Thermometer": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=240",
    "Glucose Test Strips": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=270",
    "BP Strips": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=300",
    "Medicine Organizer": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=330",
    "Pill Cutter": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&sat=20",
    "Syringe 5ml Pack": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&sat=40",
    "IV Stand": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=120",
    "Cervical Collar": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=150",
    "Knee Cap Support": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=180",
    "Ankle Support": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=200",
    "Wrist Support": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=220",
    "Back Support Belt": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=240",
    "Crutches Pair": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=260",
    "Walking Stick": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=280",
    "Wheelchair": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=300",
    "Air Bed Medical": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=320",
    "Bedpan Plastic": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&sat=60",
    "Urinal Bottle": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&sat=80",
    "Vaporizer Steam": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&sat=20",
    "Eye Wash Cup": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=30&sat=30",
    "Tongue Depressor": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=60&sat=30",
    "Dressing Scissors": "https://images.unsplash.com/photo-1562564055-71e051d33c19?w=300&h=300&fit=crop&hue=30",
    "Forceps Mosquito": "https://images.unsplash.com/photo-1562564055-71e051d33c19?w=300&h=300&fit=crop&hue=60",
    "Urine Test Cup": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=90&sat=30",
    "Hot Water Bag": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&sat=40",
    "Cold Pack Gel": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&sat=60&hue=200",
    "Compression Stockings": "https://images.unsplash.com/photo-1584735175315-9d5df23be4be?w=300&h=300&fit=crop",
    "Nasal Aspirator": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=120&sat=30",
    "Breast Pump Manual": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=150&sat=30",
    "Baby Monitor": "https://images.unsplash.com/photo-1587826080692-f439cd0b70da?w=300&h=300&fit=crop&hue=30",
    "Hearing Aid Basic": "https://images.unsplash.com/photo-1584308666744-24d5c474f2ae?w=300&h=300&fit=crop&hue=180&sat=30",
    "TENS Machine": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&sat=80",
    # FITNESS
    "Yoga Mat 6mm": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop",
    "Dumbbell Set 10kg": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop",
    "Resistance Bands Set": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=30",
    "Skipping Rope": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=60",
    "Pull Up Bar": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=90",
    "Push Up Board": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=120",
    "Ab Roller Wheel": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=150",
    "Kettlebell 8kg": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=180",
    "Barbell Set 20kg": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=200",
    "Weight Plates 5kg": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=220",
    "Exercise Cycle": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=240",
    "Treadmill Manual": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=260",
    "Rowing Machine": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=280",
    "Stepper Machine": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=300",
    "Elliptical Trainer": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=320",
    "Gym Gloves": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&sat=30",
    "Gym Belt": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&sat=50",
    "Knee Wraps": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&sat=70",
    "Wrist Wraps": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&sat=90",
    "Gym Bag": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=200",
    "Protein Shaker": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=60",
    "Water Bottle Sport": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=90",
    "Foam Roller": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=30",
    "Massage Ball": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=60",
    "Stretching Strap": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=90",
    "Balance Board": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=120",
    "Bosu Ball": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=150",
    "Battle Rope 10m": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&sat=-20",
    "Medicine Ball 3kg": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&sat=-40",
    "Suspension Trainer": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&sat=-60",
    "Gymnastics Mat": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=200",
    "Exercise Bench": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=30&sat=-20",
    "Squat Rack": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=60&sat=-20",
    "Pull Down Machine": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=90&sat=-20",
    "Dip Station": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=120&sat=-20",
    "Speed Bag": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=150&sat=-20",
    "Boxing Gloves": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=0&sat=30",
    "Jump Board": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=240",
    "Punching Bag 3ft": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=180&sat=-20",
    "Sports Shoes Running": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=30",
    "Compression Shorts": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=200&sat=-20",
    "Sports Bra": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=280",
    "Track Pants": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=220&sat=-20",
    "Sports T-shirt": "https://images.unsplash.com/photo-1571019614242-c5c5dee9f50b?w=300&h=300&fit=crop&hue=240&sat=-20",
    "Yoga Block Set": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=300",
    "Yoga Wheel": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=320",
    "Acupressure Mat": "https://images.unsplash.com/photo-1575052814086-f385e2e2ad1b?w=300&h=300&fit=crop&hue=340",
    "Posture Corrector": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=30",
    "Massage Gun": "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=300&h=300&fit=crop&hue=60",
    "Smart Scale BMI": "https://images.unsplash.com/photo-1543362906-acfc16c67564?w=300&h=300&fit=crop&hue=30",
    # KIDS
    "Building Blocks 100pc": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop",
    "Remote Control Car": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop",
    "Barbie Doll": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=320",
    "Action Figure Set": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=30",
    "Jigsaw Puzzle 500pc": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=30",
    "Board Game Family": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=60",
    "Card Game UNO": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=90",
    "Chess Set": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=120",
    "Ludo Board Game": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=150",
    "Carrom Board": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=180",
    "Badminton Set": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=60",
    "Cricket Set Kids": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=90",
    "Football Size 5": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=120",
    "Basketball": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=150",
    "Frisbee": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=180",
    "Kite Set": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=200",
    "Water Gun": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=220",
    "Nerf Gun": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=240",
    "Play Dough Set": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=200",
    "Kinetic Sand": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=220",
    "Slime Kit": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=240",
    "Art Craft Kit": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=260",
    "Coloring Book": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=280",
    "Sticker Book": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=300",
    "Clay Modeling Set": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=320",
    "Science Kit Kids": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=340",
    "Robot Toy": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=260",
    "Drone Mini Kids": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=280",
    "Telescope Kids": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=300",
    "Microscope Kids": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=320",
    "Musical Keyboard": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&sat=30",
    "Guitar Toy Mini": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&sat=50",
    "Drum Set Kids": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&sat=70",
    "Baby Walker": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&sat=-30",
    "Baby Rocker": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&sat=-50",
    "Baby Swing": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&sat=-70",
    "Stuffed Teddy Bear": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&sat=30",
    "Soft Toys Set": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&sat=50",
    "Puppet Set": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&sat=70",
    "Kids Tent": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&sat=-30",
    "Trampoline Mini": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&sat=-50",
    "Slide and Swing": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&sat=-70",
    "Tricycle": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&sat=-90",
    "Balance Bike": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=340",
    "Scooter Kids": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=0&sat=-30",
    "Roller Skates": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=20&sat=-30",
    "Helmet Kids": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=40&sat=-30",
    "Knee Pads Kids": "https://images.unsplash.com/photo-1566576912321-d58ddd7a6088?w=300&h=300&fit=crop&hue=60&sat=-30",
    "Magic Set Kids": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=0&sat=30",
    "Kaleidoscope": "https://images.unsplash.com/photo-1515488042361-ee00e0ddd4e4?w=300&h=300&fit=crop&hue=20&sat=30",
    # FASHION
    "Gold Plated Necklace": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop",
    "Silver Chain Necklace": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&sat=-50",
    "Pearl Necklace Set": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=30",
    "Mangalsutra Gold": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=60",
    "Temple Jewellery Set": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=90",
    "Diamond Pendant": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=120",
    "Choker Necklace": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=150",
    "Layered Necklace": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=180",
    "Gold Bangles Set": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=200",
    "Silver Bracelet": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=220&sat=-30",
    "Kada Bangle": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=240",
    "Beaded Bracelet": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=260",
    "Gold Earrings": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=280",
    "Silver Earrings": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=300&sat=-30",
    "Jhumka Earrings": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=320",
    "Hoop Earrings": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=340",
    "Stud Earrings CZ": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&sat=30",
    "Thread Earrings": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&sat=50",
    "Gold Ring": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&sat=70",
    "Silver Ring": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&sat=-70",
    "Stone Ring": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&sat=90",
    "Couple Ring Set": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=30&sat=30",
    "Nose Pin Gold": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=60&sat=30",
    "Maang Tikka": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=90&sat=30",
    "Hair Clips Set": "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop&hue=30",
    "Saree Pin Set": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=120&sat=30",
    "Bindis Pack": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=150&sat=30",
    "Bangles Glass Set": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=180&sat=30",
    "Anklet Payal": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=200&sat=30",
    "Toe Ring Set": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=220&sat=30",
    "Sunglasses Fashion": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&hue=30",
    "Hair Band Designer": "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop&hue=60",
    "Scarf Silk": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=300&h=300&fit=crop&hue=30",
    "Handbag Clutch": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=300",
    "Ladies Wallet": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&hue=300",
    "Wristlet Bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=320",
    "Belt Ladies": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=320",
    "Hat Sun Wide": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=300&h=300&fit=crop&hue=30",
    "Cap Trendy": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=300&h=300&fit=crop&hue=60",
    "Watch Ladies": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&hue=300",
    "Watch Men Casual": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&hue=320",
    "Perfume Women 50ml": "https://images.unsplash.com/photo-1541643600914-78b084683702?w=300&h=300&fit=crop",
    "Perfume Men 50ml": "https://images.unsplash.com/photo-1541643600914-78b084683702?w=300&h=300&fit=crop&hue=200",
    "Lipstick Set 6pc": "https://images.unsplash.com/photo-1586495777744-4e6232bf2177?w=300&h=300&fit=crop",
    "Kajal Black": "https://images.unsplash.com/photo-1586495777744-4e6232bf2177?w=300&h=300&fit=crop&hue=200",
    "Foundation Compact": "https://images.unsplash.com/photo-1586495777744-4e6232bf2177?w=300&h=300&fit=crop&hue=30",
    "Nail Polish Set": "https://images.unsplash.com/photo-1586495777744-4e6232bf2177?w=300&h=300&fit=crop&hue=60",
    "Mehendi Cone": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=240&sat=30",
    "Bindi Roll": "https://images.unsplash.com/photo-1515562141207-7a88fb7ce338?w=300&h=300&fit=crop&hue=260&sat=30",
    "Dupatta Chiffon": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=300&h=300&fit=crop&hue=60",
    # BAGS
    "Canvas School Bag": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop",
    "Neoprene Laptop Sleeve": "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop",
    "Hiking Daypack 25L": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop",
    "Rolling Trolley Bag": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop",
    "Gym Duffle Bag": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=120",
    "Tote Bag Canvas Large": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop",
    "Waterproof Dry Bag 10L": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&hue=200",
    "Laptop Backpack 30L": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop",
    "Mini Crossbody Bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop",
    "Travel Packing Cubes 4pc": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=-20",
    "Camera Bag Shoulder": "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&hue=30",
    "Tactical Backpack 45L": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=-50",
    "Fanny Pack Waist Bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=60",
    "College Backpack 20L": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&hue=30",
    "Diaper Bag Multifunction": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&hue=30",
    "Drawstring Bag Sport": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-30",
    "Leather Messenger Bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=30",
    "Foldable Shopping Bag": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=-40",
    "Hard Shell Suitcase 20in": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&hue=60",
    "Document Holder Bag": "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&sat=20",
    "String Backpack Mesh": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&sat=-40",
    "Laptop Sleeve 13inch": "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&hue=60",
    "Backpack Rain Cover": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&hue=120",
    "Lunch Bag Insulated": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=30",
    "Shoulder Bag Oxford": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=180",
    "Travel Neck Pouch": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&hue=60",
    "Kids School Bag": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=280",
    "Trekking Bag 60L": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=20",
    "Pouch Set 3pc": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=-20",
    "Tool Bag Canvas": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&hue=60",
    "Sports Backpack 35L": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=30",
    "Yoga Mat Bag": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&hue=120",
    "Drawstring Bag Printed": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&hue=180",
    "College Sling Bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=240",
    "Expandable Duffel 40L": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=20",
    "Anti-Theft Backpack": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&sat=20",
    "Leather Wallet Bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=40",
    "Book Bag with Handle": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=20",
    "Weekender Bag Duffel": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&hue=180",
    "Transparent PVC Bag": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-60",
    "Backpack Chest Strap": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=30",
    "Mini Backpack Cute": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&hue=320",
    "Eco Jute Bag": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=-20",
    "Garment Bag Travel": "https://images.unsplash.com/photo-1491637639811-60e2756cc1c7?w=300&h=300&fit=crop&hue=180",
    "Briefcase Laptop Bag": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&hue=120",
    "Compression Packing Bag": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=-40",
    "Bottle Holder Bag": "https://images.unsplash.com/photo-1581605405669-fcdf81165afa?w=300&h=300&fit=crop&sat=-20",
    "Shoe Bag Travel": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-20",
    "Pencil Case Large": "https://images.unsplash.com/photo-1544816565-aa8c1166648f?w=300&h=300&fit=crop&sat=40",
    "Pouch Waterproof Phone": "https://images.unsplash.com/photo-1548036328-c9fa89d128fa?w=300&h=300&fit=crop&sat=-40",
    # ACCESSORIES
    "Stainless Steel Water Bottle": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop",
    "Steel Lunch Box Compartment": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop",
    "Polarized UV Sunglasses": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop",
    "Genuine Leather Wallet": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop",
    "Canvas Web Belt": "https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=300&h=300&fit=crop&sat=-70",
    "Quartz Wrist Watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop",
    "Copper Water Bottle": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=30",
    "Titanium Metal Watch": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&sat=-30",
    "Polarized Sports Goggles": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&hue=180",
    "Card Holder Slim": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&sat=-20",
    "Travel Pillow Neck": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&hue=30",
    "Umbrella Auto Open": "https://images.unsplash.com/photo-1520923642038-b4259acecbd7?w=300&h=300&fit=crop",
    "Leather Keyholder": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&hue=30",
    "Insulated Flask 750ml": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&sat=-20",
    "Sports Wristband 2pc": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300&h=300&fit=crop",
    "Pocket Knife Swiss": "https://images.unsplash.com/photo-1562114808-b4b33cf6e7b5?w=300&h=300&fit=crop",
    "Silicone Watch Band": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&hue=120",
    "Carabiner Clip 4pc": "https://images.unsplash.com/photo-1622560480605-d83c853bc5c3?w=300&h=300&fit=crop&sat=-60",
    "Bamboo Sunglasses": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&sat=-20",
    "Coin Purse Leather": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&sat=30",
    "Phone Pop Socket": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop",
    "Magnetic Phone Mount": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop&hue=180",
    "Luggage Tag Leather": "https://images.unsplash.com/photo-1565026057447-bc90a3dceb87?w=300&h=300&fit=crop&sat=-60",
    "Passport Holder": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&hue=60",
    "Sunscreen Stick SPF50": "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop",
    "Watch Winder Single": "https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=300&h=300&fit=crop&hue=30",
    "Tie Clip Silver": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=300&h=300&fit=crop",
    "Cufflinks Formal": "https://images.unsplash.com/photo-1507679799987-c73779587ccf?w=300&h=300&fit=crop&sat=-30",
    "Hair Tie Set 20pc": "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop&hue=280",
    "Scrunchie Set 5pc": "https://images.unsplash.com/photo-1556228578-dd539282b964?w=300&h=300&fit=crop&hue=320",
    "Headband Sports": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300&h=300&fit=crop&hue=60",
    "Cooling Towel Sport": "https://images.unsplash.com/photo-1575311373937-040b8e1fd5b6?w=300&h=300&fit=crop&sat=20",
    "Bottle Opener Keychain": "https://images.unsplash.com/photo-1562114808-b4b33cf6e7b5?w=300&h=300&fit=crop&sat=-30",
    "Pen Knife Multi Tool": "https://images.unsplash.com/photo-1562114808-b4b33cf6e7b5?w=300&h=300&fit=crop&hue=60",
    "Slim Bifold Wallet": "https://images.unsplash.com/photo-1627123424574-724758594e93?w=300&h=300&fit=crop&hue=180",
    "Compression Socks 3pc": "https://images.unsplash.com/photo-1584735175315-9d5df23be4be?w=300&h=300&fit=crop",
    "Cap Baseball Cotton": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=300&h=300&fit=crop",
    "Beanie Woolen Cap": "https://images.unsplash.com/photo-1588850561407-ed78c282e89b?w=300&h=300&fit=crop&hue=60",
    "Scarf Soft Cotton": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=300&h=300&fit=crop",
    "Gloves Touch Screen": "https://images.unsplash.com/photo-1520903920243-00d872a2d1c9?w=300&h=300&fit=crop&hue=180",
    "Sunglasses Case Hard": "https://images.unsplash.com/photo-1572635196237-14b3f281503f?w=300&h=300&fit=crop&sat=-50",
    "Pen Organizer Leather": "https://images.unsplash.com/photo-1471107340929-a87cd0f5b5f3?w=300&h=300&fit=crop",
    "Phone Lanyard Neck": "https://images.unsplash.com/photo-1586953208448-b95a79798f07?w=300&h=300&fit=crop&sat=-20",
    "Wax Shoe Polish Kit": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-30",
    "Shoe Horn Long": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-60",
    "Travel Adapter Universal": "https://images.unsplash.com/photo-1558089687-f282ffcbc126?w=300&h=300&fit=crop&hue=120",
    "Silicone Cable Tie 10pc": "https://images.unsplash.com/photo-1558618666-fcd25c85cd64?w=300&h=300&fit=crop&sat=-30",
    "Microfiber Cloth 5pc": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop&sat=-40",
    "Lens Cleaning Pen": "https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=300&h=300&fit=crop&sat=-40",
    "Collapsible Water Cup": "https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=300&h=300&fit=crop&hue=120",
    "Portable Ashtray": "https://images.unsplash.com/photo-1585771724684-38269d6639fd?w=300&h=300&fit=crop&sat=-60",
    # FOOTWEAR
    "Running Sports Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop",
    "Foam Flip Flops": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop",
    "Leather Casual Shoes": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop",
    "Canvas Sneakers White": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop",
    "Trekking Sandals": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=30",
    "High Top Sneakers": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=200",
    "Formal Oxford Shoes": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&sat=-20",
    "Rain Boots Waterproof": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop",
    "Slippers Memory Foam": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=-30",
    "Sports Sandals": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=60",
    "Ankle Boots Chelsea": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=30",
    "Ballet Flats Women": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop",
    "Loafers Slip-on Men": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=30",
    "Platform Sneakers": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=60",
    "Moccasins Suede": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=60",
    "Sandals Flat Casual": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=120",
    "Trail Running Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=30",
    "Espadrilles Canvas": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&sat=-20",
    "Work Boots Steel Toe": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&sat=-30",
    "Gym Training Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=20",
    "Wedge Heels Women": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&hue=30",
    "Clogs Wooden Sole": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&sat=-40",
    "Boat Shoes Deck": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=120",
    "Sandals Kolhapuri": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=30",
    "Slip Resistant Kitchen": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-40",
    "Hiking Boots Mid": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=60",
    "Dress Sandals Heeled": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&hue=60",
    "Kids Sports Shoes": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=280",
    "Breathable Mesh Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-20",
    "Slip-on Vans Style": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&sat=20",
    "Formal Derby Shoes": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&sat=20",
    "Open Toe Heels": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&sat=20",
    "Snow Boots Warm": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&sat=20",
    "Casual Chukka Boots": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=120",
    "Pool Slides Comfort": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=-50",
    "Woven Flat Sandals": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=180",
    "Sneakers Chunky Sole": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&sat=40",
    "Driving Moccasins": "https://images.unsplash.com/photo-1449505278894-297fdb3edbc1?w=300&h=300&fit=crop&hue=180",
    "Toe Ring Sandals": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=240",
    "Faux Leather Boots": "https://images.unsplash.com/photo-1608256246200-53e635b5b65f?w=300&h=300&fit=crop&hue=180",
    "Jelly Sandals Kids": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=280",
    "Athleisure Shoes": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=60",
    "Platform Sandals": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&sat=30",
    "Lace-up Canvas Shoes": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=120",
    "Gum Sole Sneakers": "https://images.unsplash.com/photo-1525966222134-fcfa99b8ae77?w=300&h=300&fit=crop&hue=180",
    "Rubber Rain Sandals": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&sat=-20",
    "Toe Post Flip Flops": "https://images.unsplash.com/photo-1603487742131-4160ec999306?w=300&h=300&fit=crop&hue=320",
    "Walking Shoes Wide": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&hue=120",
    "Ankle Strap Heels": "https://images.unsplash.com/photo-1543163521-1bf539c55dd2?w=300&h=300&fit=crop&hue=120",
    "Barefoot Minimalist": "https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=300&h=300&fit=crop&sat=-60",
}

LIMITED_OFFER_CATEGORIES = {
    "electronic": {"label": "⚡ Flash Sale", "hours": 6},
    "mobile":     {"label": "📱 Limited Deal", "hours": 8},
    "footwear":   {"label": "👟 Weekend Deal", "hours": 24},
    "bag":        {"label": "🎒 Limited Stock", "hours": 12},
    "fitness":    {"label": "💪 Fitness Sale", "hours": 10},
    "fashion":    {"label": "👗 Style Sale", "hours": 18},
}

def get_image_url(name):
    return PRODUCT_IMAGES.get(name, "https://images.unsplash.com/photo-1585336261022-680e295ce3fe?w=300&h=300&fit=crop")

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
    orig = product.get('original_price', 0)
    price = product.get('price', 0)
    product['discount'] = round((1 - price / orig) * 100) if orig and orig > price else 0
    cur.execute("SELECT * FROM products WHERE category=? AND id!=? LIMIT 4", (product['category'], id))
    rec = enrich([dict(r) for r in cur.fetchall()])
    cur.execute("SELECT * FROM reviews WHERE product_id=? ORDER BY created_at DESC", (id,))
    reviews = [dict(r) for r in cur.fetchall()]
    avg_rating = round(sum(r['rating'] for r in reviews) / len(reviews), 1) if reviews else None
    conn.close()
    return render_template("product.html", product=product, rec=rec, cart_count=get_cart_count(), reviews=reviews, avg_rating=avg_rating)

@app.route("/search")
def search():
    q = request.args.get("q", "").strip()
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM products WHERE LOWER(name) LIKE LOWER(?)", ('%' + q + '%',))
    products = enrich([dict(p) for p in cur.fetchall()])
    rec = []
    if products:
        cur.execute("SELECT * FROM products WHERE category=? AND id!=? LIMIT 4", (products[0]["category"], products[0]["id"]))
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

@app.route("/checkout", methods=["GET", "POST"])
def checkout():
    conn = db()
    cur = conn.cursor()
    cur.execute("""
        SELECT cart.id, products.name, products.price, products.id as product_id
        FROM cart JOIN products ON cart.product_id = products.id
    """)
    items = [dict(i) for i in cur.fetchall()]
    for item in items:
        item['image_url'] = get_image_url(item['name'])
    total = sum(item["price"] for item in items)
    if not items:
        conn.close()
        return redirect("/cart")
    if request.method == "POST":
        name    = request.form.get("name", "").strip()
        phone   = request.form.get("phone", "").strip()
        address = request.form.get("address", "").strip()
        city    = request.form.get("city", "").strip()
        pincode = request.form.get("pincode", "").strip()
        if not all([name, phone, address, city, pincode]):
            conn.close()
            return render_template("checkout.html", items=items, total=total, cart_count=get_cart_count(), error="All fields required!")
        cur.execute("INSERT INTO orders(name,phone,address,city,pincode,total) VALUES(?,?,?,?,?,?)", (name, phone, address, city, pincode, total))
        order_id = cur.lastrowid
        for item in items:
            cur.execute("INSERT INTO order_items(order_id,product_name,product_price) VALUES(?,?,?)", (order_id, item["name"], item["price"]))
        cur.execute("DELETE FROM cart")
        conn.commit()
        conn.close()
        return redirect(f"/order-confirmed/{order_id}")
    conn.close()
    return render_template("checkout.html", items=items, total=total, cart_count=get_cart_count(), error=None)

@app.route("/order-confirmed/<int:order_id>")
def order_confirmed(order_id):
    conn = db()
    cur = conn.cursor()
    cur.execute("SELECT * FROM orders WHERE id=?", (order_id,))
    order = cur.fetchone()
    if not order:
        conn.close()
        return redirect("/")
    order = dict(order)
    cur.execute("SELECT * FROM order_items WHERE order_id=?", (order_id,))
    items = [dict(i) for i in cur.fetchall()]
    conn.close()
    return render_template("order_confirmed.html", order=order, items=items, cart_count=get_cart_count())

@app.route("/orders")
def orders():
    phone = request.args.get("phone", "").strip()
    conn = db()
    cur = conn.cursor()
    if phone:
        clean = phone.replace(" ", "").replace("-", "")
        cur.execute("SELECT * FROM orders WHERE REPLACE(REPLACE(phone,' ',''),'-','') LIKE ? ORDER BY created_at DESC", ('%' + clean + '%',))
        orders = [dict(o) for o in cur.fetchall()]
        for o in orders:
            cur.execute("SELECT * FROM order_items WHERE order_id=?", (o["id"],))
            o["items"] = [dict(i) for i in cur.fetchall()]
        conn.close()
        return render_template("orders.html", orders=orders, cart_count=get_cart_count(), searched_phone=phone)
    else:
        conn.close()
        return render_template("orders.html", orders=[], cart_count=get_cart_count(), searched_phone=None)

@app.route("/review/<int:product_id>", methods=["POST"])
def add_review(product_id):
    name    = request.form.get("reviewer_name", "").strip()
    phone   = request.form.get("phone", "").strip()
    rating  = request.form.get("rating", "5").strip()
    comment = request.form.get("comment", "").strip()
    if name and phone and comment and rating:
        conn = db()
        cur = conn.cursor()
        cur.execute("SELECT id FROM reviews WHERE product_id=? AND REPLACE(phone,' ','')=?", (product_id, phone.replace(" ","")))
        existing = cur.fetchone()
        if existing:
            cur.execute("UPDATE reviews SET rating=?, comment=?, reviewer_name=?, created_at=CURRENT_TIMESTAMP WHERE id=?", (int(rating), comment, name, existing["id"]))
        else:
            cur.execute("INSERT INTO reviews(product_id,reviewer_name,phone,rating,comment) VALUES(?,?,?,?,?)", (product_id, name, phone, int(rating), comment))
        conn.commit()
        conn.close()
    return redirect(f"/product/{product_id}")

@app.route("/admin")
def admin():
    return render_template("admin.html", cart_count=get_cart_count())

if __name__ == "__main__":
    app.run(debug=True)