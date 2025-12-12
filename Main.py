from tkinter import *
from tkinter import messagebox
from openai import OpenAI
from PIL import Image, ImageTk
import mysql.connector

client = OpenAI(api_key="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")#after 90 days it expired 

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="p",
    database="IndiaTourism"
)
cursor = conn.cursor()

cursor.execute("CREATE DATABASE IF NOT EXISTS IndiaTourism")
cursor.execute("USE IndiaTourism")
cursor.execute("DROP TABLE IF EXISTS tourist_places")
cursor.execute("DROP TABLE IF EXISTS states")
cursor.execute("""
CREATE TABLE states (
    state_id INT PRIMARY KEY AUTO_INCREMENT,
    state_name VARCHAR(100) NOT NULL UNIQUE,
    type ENUM('State', 'Union Territory') NOT NULL,
    culture TEXT,
    tradition TEXT,
    language VARCHAR(100)
)
""")
cursor.execute("""
CREATE TABLE tourist_places (
    place_id INT PRIMARY KEY AUTO_INCREMENT,
    state_id INT,
    place_name VARCHAR(255),
    FOREIGN KEY (state_id) REFERENCES states(state_id)
)
""")

states_data = [
    ('Andhra Pradesh', 'State', 'Kuchipudi dance, Sankranti festival', 'Temple architecture, Kalamkari art', 'Telugu'),
    ('Arunachal Pradesh', 'State', 'Tribal festivals (Losar, Dree)', 'Monpa wood craft, yak dances', 'English, Nyishi'),
    ('Assam', 'State', 'Bihu festival, Satriya dance', 'Silk weaving (Muga, Eri)', 'Assamese'),
    ('Bihar', 'State', 'Chhath Puja, Bhojpuri folk', 'Madhubani painting', 'Hindi, Bhojpuri'),
    ('Chhattisgarh', 'State', 'Bastar Dussehra, tribal dances', 'Bell-metal handicrafts', 'Chhattisgarhi, Hindi'),
    ('Goa', 'State', 'Carnival, Konkani folk music', 'Portuguese heritage houses', 'Konkani, Marathi'),
    ('Gujarat', 'State', 'Navratri Garba, folk arts', 'Bandhani textiles, Patola sarees', 'Gujarati'),
    ('Haryana', 'State', 'Teeyan, Ragini folk', 'Phulkari embroidery', 'Haryanvi, Hindi'),
    ('Himachal Pradesh', 'State', 'Kullu Dussehra, Pahari songs', 'Wool shawls, wood carving', 'Pahari, Hindi'),
    ('Jharkhand', 'State', 'Sarhul, Jhumair dance', 'Dokra metal craft', 'Hindi, Nagpuri'),
    ('Karnataka', 'State', 'Mysuru Dasara, Yakshagana', 'Sandalwood art, Mysore silk', 'Kannada'),
    ('Kerala', 'State', 'Onam, Kathakali', 'Backwaters, mural paintings', 'Malayalam'),
    ('Madhya Pradesh', 'State', 'Bhagoria festival, folk songs', 'Chanderi, Maheshwari sarees', 'Hindi'),
    ('Maharashtra', 'State', 'Ganeshotsav, Lavani dance', 'Warli painting, Paithani sarees', 'Marathi'),
    ('Manipur', 'State', 'Lai Haraoba, Manipuri dance', 'Handloom & bamboo crafts', 'Manipuri'),
    ('Meghalaya', 'State', 'Shad Suk Mynsiem, Wangala', 'Bamboo huts, wood carving', 'Khasi, Garo'),
    ('Mizoram', 'State', 'Chapchar Kut, Cheraw dance', 'Handloom, bamboo work', 'Mizo'),
    ('Nagaland', 'State', 'Hornbill Festival', 'Naga shawls, bead jewelry', 'English, Nagamese'),
    ('Odisha', 'State', 'Rath Yatra, Odissi dance', 'Pattachitra art, Sambalpuri sarees', 'Odia'),
    ('Punjab', 'State', 'Baisakhi, Bhangra', 'Phulkari embroidery, Giddha', 'Punjabi'),
    ('Rajasthan', 'State', 'Desert festival, Kalbeliya', 'Bandhej textiles, stone carving', 'Rajasthani, Hindi'),
    ('Sikkim', 'State', 'Losar, Mask dances', 'Handloom & Buddhist art', 'Nepali, English'),
    ('Tamil Nadu', 'State', 'Pongal, Bharatanatyam', 'Temple architecture, Kanchipuram silk', 'Tamil'),
    ('Telangana', 'State', 'Bonalu, Perini dance', 'Nirmal paintings, Pochampally sarees', 'Telugu'),
    ('Tripura', 'State', 'Garia Puja, tribal dance', 'Handloom, bamboo products', 'Kokborok, Bengali'),
    ('Uttar Pradesh', 'State', 'Holi (Mathura), Kathak', 'Chikankari embroidery, Awadhi cuisine', 'Hindi, Urdu'),
    ('Uttarakhand', 'State', 'Ganga Aarti, Kumaoni songs', 'Woolen shawls, wood craft', 'Hindi, Garhwali'),
    ('West Bengal', 'State', 'Durga Puja, Baul songs', 'Terracotta, Baluchari sarees', 'Bengali'),
    ('Andaman and Nicobar Islands', 'Union Territory', 'Beach festivals', 'Tribal arts, coconut craft', 'Hindi, English'),
    ('Chandigarh', 'Union Territory', 'Modern Punjabi culture', 'Urban handicrafts', 'Punjabi, Hindi'),
    ('Dadra and Nagar Haveli and Daman and Diu', 'Union Territory', 'Beach festivals', 'Portuguese influence', 'Gujarati, Hindi'),
    ('Delhi', 'Union Territory', 'Blend of Mughal and modern', 'Mughal architecture, street food', 'Hindi, English'),
    ('Jammu and Kashmir', 'Union Territory', 'Tulip festival, Sufi songs', 'Kashmiri shawls, Wazwan cuisine', 'Kashmiri, Urdu'),
    ('Ladakh', 'Union Territory', 'Hemis festival, folk songs', 'Thangka paintings, apricot wood', 'Ladakhi, Hindi'),
    ('Lakshadweep', 'Union Territory', 'Island fairs, folk dance', 'Coir craft, coconut art', 'Malayalam, Jeseri'),
    ('Puducherry', 'Union Territory', 'French and Tamil blend', 'French colonial houses, Tamil crafts', 'Tamil, French, English')
]

cursor.executemany("""
INSERT IGNORE INTO states (state_name, type, culture, tradition, language)
VALUES (%s, %s, %s, %s, %s)
""", states_data)
conn.commit()
cursor.execute("SELECT state_id, state_name FROM states")
state_ids = {name: id for (id, name) in cursor.fetchall()}

places_data = [
    (state_ids['Andhra Pradesh'], 'Tirupati'),
    (state_ids['Andhra Pradesh'], 'Araku Valley'),
    (state_ids['Arunachal Pradesh'],'Tawang Monastery'),
    (state_ids['Assam'],'Kaziranga National Park'),
    (state_ids['Assam'],'Kamakhya Temple'),
    (state_ids['Bihar'],'Bodh Gaya'),
    (state_ids['Chhattisgarh'],'Bastar'),
    (state_ids['Goa'], 'Calangute Beach'),
    (state_ids['Goa'], 'Dudhsagar Falls'),
    (state_ids['Gujarat'],'Kutch'),
    (state_ids['Haryana'],'Chandigarh'),
    (state_ids['Himachal Pradesh'],'Manali'),
    (state_ids['Himachal Pradesh'],'Shimla'),
    (state_ids['Jharkhand'],'Betla National Park'),
    (state_ids['Karnataka'],'Coorg'),
    (state_ids['Kerala'], 'Munnar'),
    (state_ids['Kerala'], 'Alleppey'),
    (state_ids['Madhya Pradesh'],'Bhopal'),
    (state_ids['Maharashtra'],'Lonavala'),
    (state_ids['Maharashtra'],'Gateway of India'),
    (state_ids['Manipur'],'Loktak Lake'),
    (state_ids['Meghalaya'],'Cherrapunjee'),
    (state_ids['Mizoram'],'Lunglei'),
    (state_ids['Nagaland'],'Monochung'),
    (state_ids['Odisha'],'Puri'),
    (state_ids['Odisha'],'Konark Sun Temple'),
    (state_ids['Punjab'],'Golden Temple'),
    (state_ids['Rajasthan'], 'Jaipur'),
    (state_ids['Rajasthan'], 'Udaipur'),
    (state_ids['Sikkim'],'Tsomgo Lake'),
    (state_ids['Tamil Nadu'], 'Ooty'),
    (state_ids['Tamil Nadu'], 'Rameswaram'),
    (state_ids['Telangana'],'Hyderabad'),
    (state_ids['Tripura'],'Ujjayanta Palace'),
    (state_ids['Uttar Pradesh'], 'Taj Mahal'),
    (state_ids['Uttar Pradesh'], 'Varanasi Ghats'),
    (state_ids['Uttarakhand'],'Rishikesh'),
    (state_ids['West Bengal'],'Darjeeling'),
    (state_ids['Andaman and Nicobar Islands'],'Havelock Island'),
    (state_ids['Chandigarh'],'Rock Garden'),
    (state_ids['Dadra and Nagar Haveli and Daman and Diu'],'Vanganga Lake Garden'),
    (state_ids['Delhi'], 'Red Fort'),
    (state_ids['Delhi'], 'India Gate'),
    (state_ids['Jammu and Kashmir'], 'Gulmarg'),
    (state_ids['Jammu and Kashmir'], 'Vaishno Devi'),
    (state_ids['Ladakh'], 'Pangong Lake'),
    (state_ids['Ladakh'], 'Leh Palace'),
    (state_ids['Lakshadweep'],'Bangaram island'),
    (state_ids['Puducherry'],'Auroville')
    ]

cursor.executemany("INSERT INTO tourist_places (state_id, place_name) VALUES (%s, %s)", places_data)
conn.commit()
print("✅ Tourist places inserted.")

cursor.close()
conn.close()

conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="p",
    database="IndiaTourism"
)
cursor = conn.cursor()

indian_cuisines={
'Andhra Pradesh':['Hyderabadi biryani','Pesarattu'],
'Arunachal Pradesh':['Thukpa','Apong'],
'Assam':['Masor Tenga(Fish curry)'],
'Bihar':['Litti Chokha'],
'Chhattisgarh':['Chila'],
'Goa':['Goan fish curry','Bebinca'],
'Gujarat':['Dhokla'],
'Haryana':['Kadhi Pakoda'],
'Himachal Pradesh':['Chana Madra','Dham'],
'Jharkhand':['Rugra'],
'Karnataka':['Mysore Masala Dosa','Bisi Bele Bath'],
'Kerala':['Appam with stew'],
'Madhya Pradesh':['Dal Bafla','Bhutte Ka Kees'],
'Maharashtra':['Vada Pav','Misal Pav'],
'Manipur':['Eromba'],
'Meghalaya':['Jadoh'],
'Mizoram':['Bai'],
'Nagaland':['Smoked Pork with Bamboo Stick'],
'Odisha':['Dalma','Chenna Poda'],
'Punjab':['Makki Di Roti and Sarson Da Saag','Butter Chicken'],
'Rajasthan':['Dal Baati Churma'],
'Sikkim':['Momos','Thukpa'],
'Tamil Nadu':['Pongal'],
'Telangana':['Hyderabadi Biryani'],
'Tripura':['Berma','Mui Borok'],
'Uttar Pradesh':['Biryani','Tunde Ke Kebabs'],
'Uttarakhand':['Bhatt Ki Churkani','Dham'],
'West Bengal':['Kosha Mangshi','Maacher Jhol'],
'Andaman and Nicobar Island':['Coconut Prawn Curry','Tandoori Fish'],
'Chandigarh':['Chole Kulche','Butter Chicken'],
'Dadar and Nagar Haveli and Daman and Diu':['Seafood Curry'],
'Delhi':['Chhole Bhature','Butter Chicken'],
'Jammu and Kashmir':['Rogan Josh','Yakhni'],
'Ladakh':['Skyu','Thukpa'],
'Puducherry':['Meen Puyabaisse'],
'Lakshadweep':['Mas Podichathu']
} 
best_time_to_visit = {
    "Jammu and Kashmir": "April–October (Kashmir Valley), December–February (Gulmarg snow)",
    "Ladakh": "June–September",
    "Himachal Pradesh": "March–June, September–November",
    "Punjab": "October–March",
    "Haryana": "October–March",
    "Uttarakhand": "March–June, September–November",
    "Delhi": "October–March",
    "Rajasthan": "October–March",
    "Gujarat": "November–February",
    "Maharashtra": "October–February, June–September (monsoon treks)",
    "Goa": "November–February",
    "Dadra and Nagar Haveli and Daman and Diu": "October–March", 
    "Madhya Pradesh": "October–March",
    "Chhattisgarh": "October–February", 
    "West Bengal": "October–March",
    "Odisha": "November–February",
    "Bihar": "October–March",
    "Jharkhand": "October–March", 
    "Assam": "October–April",
    "Arunachal Pradesh": "October–April",
    "Nagaland": "October–May",
    "Manipur": "October–April",
    "Mizoram": "October–March",
    "Tripura": "October–March",
    "Meghalaya": "October–April, June–September (for monsoon beauty)",
    "Sikkim": "March–June, September–November", 
    "Kerala": "October–March, June–August (Ayurveda monsoon season)",
    "Tamil Nadu": "November–March",
    "Karnataka": "October–March",
    "Andhra Pradesh": "October–March",
    "Telangana": "October–March",
    "Puducherry": "October–March",
    "Lakshadweep": "October–March",
    "Andaman and Nicobar Islands": "October–May",
    "Uttar Pradesh":"October–March",
    "Chandigarh":"October–June"
}
historical_monuments = {
    "Jammu and Kashmir": [
        "Shankaracharya Temple",
        "Martand Sun Temple",
        "Hari Parbat Fort",
        "Mubarak Mandi Palace"
    ],
    "Ladakh": [
        "Leh Palace",
        "Hemis Monastery",
        "Thiksey Monastery",
        "Shey Palace"
    ],
    "Himachal Pradesh": [
        "Kangra Fort",
        "Bhimakali Temple",
        "Tabo Monastery",
        "Naggar Castle"
    ],
    "Punjab": [
        "Golden Temple (Amritsar)",
        "Jallianwala Bagh",
        "Sheesh Mahal (Patiala)",
        "Qila Mubarak"
    ],
    "Haryana": [
        "Star Monument (Bhiwani)",
        "Tomb of Sheikh Chilli (Thanesar)",
        "Panipat Battlefield",
        "Firoz Shah Palace Complex (Hisar)"
    ],
    "Uttarakhand": [
        "Katarmal Sun Temple",
        "Baleshwar Temple",
        "Jageshwar Temples",
        "Landour Clock Tower"
    ],
    "Delhi": [
        "Red Fort",
        "Qutub Minar",
        "Humayun’s Tomb",
        "India Gate"
    ],
 
    "Rajasthan": [
        "Amber Fort (Jaipur)",
        "Mehrangarh Fort (Jodhpur)",
        "City Palace (Udaipur)",
        "Jaisalmer Fort"
    ],
    "Gujarat": [
        "Rani ki Vav (Patan)",
        "Sabarmati Ashram (Ahmedabad)",
        "Champaner-Pavagadh Forts",
        "Sun Temple (Modhera)"
    ],
    "Maharashtra": [
        "Ajanta Caves",
        "Ellora Caves",
        "Gateway of India (Mumbai)",
        "Shaniwar Wada (Pune)"
    ],
    "Goa": [
        "Basilica of Bom Jesus",
        "Se Cathedral",
        "Fort Aguada",
        "Chapora Fort"
    ],
    "Dadra and Nagar Haveli and Daman and Diu": [
        "Diu Fort",
        "St. Paul’s Church",
        "Church of Our Lady of Remedios",
        "Tribal Museum (Silvassa)"
    ],
 
    "Madhya Pradesh": [
        "Khajuraho Temples",
        "Sanchi Stupa",
        "Gwalior Fort",
        "Mandu Fort"
    ],
    "Chhattisgarh": [
        "Sirpur Laxman Temple",
        "Rajim Temples",
        "Ratanpur Fort",
        "Madku Dweep"
    ],
 
    "West Bengal": [
        "Victoria Memorial (Kolkata)",
        "Howrah Bridge",
        "Hazarduari Palace (Murshidabad)",
        "Bishnupur Terracotta Temples"
    ],
    "Odisha": [
        "Konark Sun Temple",
        "Jagannath Temple (Puri)",
        "Lingaraja Temple (Bhubaneswar)",
        "Udayagiri and Khandagiri Caves"
    ],
    "Bihar": [
        "Mahabodhi Temple (Bodh Gaya)",
        "Nalanda University Ruins",
        "Vikramshila Monastery",
        "Golghar (Patna)"
    ],
    "Jharkhand": [
        "Jagannath Temple (Ranchi)",
        "Rajrappa Temple",
        "Maluti Temples",
        "Navratangarh Fort"
    ],
 
    "Assam": [
        "Kareng Ghar (Sivasagar)",
        "Rang Ghar",
        "Talatal Ghar",
        "Kamakhya Temple"
    ],
    "Arunachal Pradesh": [
        "Ita Fort",
        "Tawang Monastery",
        "Bomdila Monastery",
        "Bhismaknagar Fort"
    ],
    "Nagaland": [
        "Kachari Ruins (Dimapur)",
        "Triple Falls (Dimapur)",
        "Dzükou Valley (cultural importance)",
        "Chumukedima Ruins"
    ],
    "Manipur": [
        "Kangla Fort",
        "Govindajee Temple",
        "Shaheed Minar (Imphal)",
        "INA Memorial (Moirang)"
    ],
    "Mizoram": [
        "Khawnglung Wildlife Heritage Site",
        "Vantawng Falls (heritage significance)",
        "Tomb of Vanhimailian",
        "Chhingpuii Memorial"
    ],
    "Tripura": [
        "Ujjayanta Palace",
        "Neermahal Palace",
        "Tripura Sundari Temple",
        "Unakoti Rock Carvings"
    ],
    "Meghalaya": [
        "Nartiang Monoliths",
        "Mawphlang Sacred Grove",
        "David Scott Trail (heritage route)",
        "Iewduh Market (Shillong)"
    ],
    "Sikkim": [
        "Rumtek Monastery",
        "Pemayangtse Monastery",
        "Rabdentse Ruins",
        "Tashiding Monastery"
    ],
 
    "Kerala": [
        "Mattancherry Palace",
        "Bekal Fort",
        "Padmanabhapuram Palace",
        "St. Francis Church (Kochi)"
    ],
    "Tamil Nadu": [
        "Brihadeeswarar Temple (Thanjavur)",
        "Meenakshi Temple (Madurai)",
        "Mahabalipuram Temples",
        "Fort St. George (Chennai)"
    ],
    "Karnataka": [
        "Hampi Ruins",
        "Mysore Palace",
        "Gol Gumbaz (Bijapur)",
        "Halebidu Temples"
    ],
    "Andhra Pradesh": [
        "Charminar (Hyderabad, historical)",
        "Golconda Fort",
        "Lepakshi Temple",
        "Undavalli Caves"
    ],
    "Telangana": [
        "Charminar",
        "Golconda Fort",
        "Chowmahalla Palace",
        "Warangal Fort"
    ],
    "Puducherry": [
        "French War Memorial",
        "Basilica of the Sacred Heart of Jesus",
        "Aayi Mandapam",
        "Romain Rolland Library"
    ],
    "Lakshadweep": [
        "Kavaratti Mosque",
        "Juma Masjid (Andrott)",
        "Ancient Tombs of Kalpeni",
        "Marine Museum (Kavaratti)"
    ],
    "Andaman and Nicobar Islands": [
        "Cellular Jail (Port Blair)",
        "Ross Island Ruins",
        "Japanese Bunkers (Ross Island)",
        "Chatham Saw Mill (oldest in Asia)"
    ],
    "Uttar Pradesh":["Taj Mahal ","Agra Fort ","Ayodhya "],
    "Chandigarh":["Sukhna Lake", "Zakir Hussain"," Rose Garden"," Butterfly Park"]
}
adventure_data = {
    "Andhra Pradesh": ["Water Sports in Rushikonda Beach", "Trekking in Araku Valley", "Caving in Borra Caves"],
    "Arunachal Pradesh": ["River Rafting in Siang", "Trekking to Talle Valley", "Camping in Ziro Valley"],
    "Assam": ["Wildlife Safari in Kaziranga", "River Cruise on Brahmaputra", "Trekking in Haflong"],
    "Bihar": ["Rock Climbing in Rajgir Hills", "Exploring Caves in Barabar Hills", "Cycling in Bodh Gaya"],
    "Chhattisgarh": ["Caving in Kotumsar", "Trekking in Kanger Valley", "Boating in Chitrakote Falls"],
    "Goa": ["Scuba Diving in Grande Island", "Jet Skiing in Baga Beach", "Parasailing in Calangute"],
    "Gujarat": ["Desert Safari in Rann of Kutch", "Paragliding in Saputara", "Trekking in Polo Forest"],
    "Haryana": ["Adventure Park in Gurgaon", "Hot Air Ballooning in Damdama", "Rock Climbing in Morni Hills"],
    "Himachal Pradesh": ["Paragliding in Bir Billing", "Trekking in Manali", "Camping in Spiti Valley"],
    "Jharkhand": ["Rock Climbing in Netarhat", "Boating in Patratu Valley", "Waterfalls Trek in Ranchi"],
    "Karnataka": ["River Rafting in Dandeli", "Scuba Diving in Netrani Island", "Trekking in Kudremukh"],
    "Kerala": ["Kayaking in Alleppey", "Trekking in Wayanad", "Paragliding in Vagamon"],
    "Madhya Pradesh": ["Wildlife Safari in Kanha", "Trekking in Pachmarhi", "Rock Climbing in Bhimbetka"],
    "Maharashtra": ["Trekking in Sahyadris", "Scuba Diving in Tarkarli", "Paragliding in Kamshet"],
    "Manipur": ["Boating in Loktak Lake", "Trekking in Dzuko Valley", "Caving in Tharon"],
    "Meghalaya": ["Caving in Mawsmai", "Trekking to Living Root Bridges", "Kayaking in Dawki River"],
    "Mizoram": ["Trekking in Blue Mountain", "Camping in Hmuifang", "Paragliding in Serchhip"],
    "Nagaland": ["Trekking in Dzukou Valley", "Camping at Kisama", "Rock Climbing in Japfu Peak"],
    "Odisha": ["Surfing in Puri", "Trekking in Gandhamardan Hills", "Boating in Chilika Lake"],
    "Punjab": ["ATV Rides in Jalandhar", "Skydiving near Patiala (seasonal)", "Camping near Kikar Lodge"],
    "Rajasthan": ["Desert Safari in Jaisalmer", "Hot Air Ballooning in Jaipur", "Camel Riding in Pushkar"],
    "Sikkim": ["Trekking to Goechala", "River Rafting in Teesta", "Yak Safari near Tsomgo Lake"],
    "Tamil Nadu": ["Surfing in Mahabalipuram", "Scuba Diving in Covelong", "Trekking in Nilgiris"],
    "Telangana": ["Trekking in Ananthagiri Hills", "Boating in Hussain Sagar", "Rock Climbing in Bhongir Fort"],
    "Tripura": ["Trekking to Jampui Hills", "Boating in Dumboor Lake", "Exploring Caves in Unakoti"],
    "Uttar Pradesh": ["Paragliding in Varanasi", "Boating in Naini Lake", "Trekking in Chitrakoot"],
    "Uttarakhand": ["River Rafting in Rishikesh", "Trekking to Valley of Flowers", "Bungee Jumping in Rishikesh"],
    "West Bengal": ["Trekking in Sandakphu", "Rafting in Teesta River", "Paragliding in Kalimpong"],
    "Andaman and Nicobar Islands": ["Scuba Diving in Havelock", "Snorkeling in Neil Island", "Sea Walking in North Bay"],
    "Chandigarh": ["Boating in Sukhna Lake", "Rock Climbing in Rock Garden", "Cycling in Leisure Valley"],
    "Dadra and Nagar Haveli and Daman and Diu": ["Parasailing in Diu", "Jet Skiing in Devka Beach", "Camping near Dudhni Lake"],
    "Delhi": ["Hot Air Ballooning near Gurgaon", "Cycling in India Gate Circuit", "Paintball Adventure in Dwarka"],
    "Jammu and Kashmir": ["Skiing in Gulmarg", "Trekking in Ladakh", "River Rafting in Zanskar"],
    "Ladakh": ["Motorbiking to Khardung La", "Camel Safari in Nubra Valley", "Trekking to Chadar"],
    "Lakshadweep": ["Scuba Diving in Kavaratti", "Snorkeling in Agatti", "Kayaking in Minicoy Lagoon"],
    "Puducherry": ["Scuba Diving in Temple Reef", "Surfing in Serenity Beach", "Kayaking in Paradise Beach"]
}

def show_warning():
    messagebox.showwarning("Warning", "Please write correct State or UT!")



def open_ai():
    root = Tk()
    root.title("AI MILI - Tourist Guide")
    root.geometry("1100x1000")
    root.configure(bg="#FFF8EB") 
    chat_box = Text(root,wrap=WORD)
    chat_box.pack()
    entry = Entry(root)
    entry.pack()
    def send_message():
        user_input = entry.get().strip()
        if user_input == "":
            return
        chat_box.insert(END, f"You: {user_input}\n",)
        entry.delete(0, END)   
        try:
            response = client.chat.completions.create(
            model="gpt-4o-mini",messages=[
            {"role": "system", "content": "You are an intelligent AI tourist guide for India. You help visitors find routes, directions, tourist attractions and related travel information,food,religion, culture, community and etc. Your name is AI MILI. You must reply 'Sorry, I can only answer India tourist-related questions.' if the question is unrelated.If user give Greeting give Greeting and tell about yourself"},
            {"role": "user", "content": user_input}
            ]
            )
            reply = response.choices[0].message.content.strip()
            chat_box.insert(END, f"AI MILI: {reply}\n\n")
            chat_box.see(END)
        except :
                chat_box.insert(END, "AI MILI: No Internet Connection.\n\n")
    Button(root, text="Send", command=send_message, font=("Arial", 12), bg="maroon", fg="white").pack()
    Button(root, text="close", command=root.destroy, font=("Arial", 12), bg="maroon", fg="white").pack()
    chat_box.insert(END, "AI MILI: Hello! I’m AI MILI, your intelligent tourist guide for India.\nHow can I assist you with your travel plans today?\n\n")
    root.mainloop()

def open_page(state_name):
    new_window = Toplevel(root1)
    new_window.title(state_name)
    new_window.geometry("1100x1400")
    new_window.configure(bg="lightpink")     
    cursor.execute("SELECT type, culture, tradition, language FROM states WHERE state_name = %s", (state_name,))
    details = cursor.fetchone()
    if details:
        Label(new_window, text=f" {state_name}", bg='lightpink',fg='darkblue',font=("Arial", 18, "bold")).pack(pady=5)
        Label(new_window, text=f"Type: {details[0]}\n",bg='lightpink',fg='black', font=("Arial", 12)).pack()
        Label(new_window, text=f"Culture: {details[1]}\n",bg='lightpink',fg='red', wraplength=350, justify=LEFT).pack()
        Label(new_window, text=f"Tradition: {details[2]}\n",bg='lightpink',fg='red', wraplength=350, justify=LEFT).pack()
        Label(new_window, text=f"Language: {details[3]}\n", bg='lightpink',fg='red',wraplength=350, justify=LEFT).pack()        
        cursor.execute("SELECT place_name FROM tourist_places WHERE state_id = (SELECT state_id FROM states WHERE state_name = %s)", (state_name,))
        places = cursor.fetchall()
        if places:
            Label(new_window, text="Tourist Places:",bg='lightpink',fg='red', font=("Arial", 12, "bold")).pack(pady=5)
            for place in places:
                Label(new_window, text=f"• {place[0]}",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()
        else:
            Label(new_window, text="No Tourist Places Available.",bg='lightpink',fg='red', font=("Arial", 11)).pack(pady=5)
    else:
        Label(new_window, text="No Data Found.",bg='lightpink',fg='red', font=("Arial", 12)).pack()
    found = False
    if state_name in indian_cuisines:
        found = True        
        Label(new_window, text=f"\nFAMOUS CUISINES:",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()
        for dish in indian_cuisines[state_name]:
            Label(new_window, text=f"• {dish}",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()
    if state_name in best_time_to_visit:
        found = True
        Label(new_window, text=f" \nBEST TIME TO VISIT",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()
        Label(new_window, text=f"• {best_time_to_visit[state_name]}",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()            
    if state_name in historical_monuments:
        found = True
        Label(new_window, text=f"\nHISTORICAL MONUMENTS:",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()       
        for monument in historical_monuments[state_name]:
            Label(new_window, text=f"• {monument}",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()
    if state_name in adventure_data:
        found = True
        Label(new_window, text=f"\nADVENTURE ACTIVITIES:",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()       
        for adv in adventure_data[state_name]:
            Label(new_window, text=f"• {adv}",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack() 
    if not found:
        Label(new_window, text=f"\nNo data found for this state/UT.",bg='lightpink',fg='red', font=("Arial", 11), anchor="w").pack()        
    Button(new_window, text="close", command=new_window.destroy, font=("Arial", 12), bg="mediumorchid", fg="white").pack()    
def on_click(event):
    x, y = event.x, event.y
    if 350 <= x <= 390 and 265 <= y <= 305:
        open_page("Ladakh")
    elif 270 <= x <= 310 and 300 <= y <= 330:
        open_page("Jammu and Kashmir")
    elif 340 <= x <= 375 and 360 <= y <= 390:
        open_page("Himachal Pradesh")
    elif 300 <= x <= 330 and 390 <= y <= 420:
        open_page("Punjab")
    elif 430 <= x <= 460 and 410 <= y <= 445:
        open_page("Uttarakhand")
    elif 320 <= x <= 350 and 445 <= y <= 470:
        open_page("Haryana")
    elif 240 <= x <= 270 and 520 <= y <= 560:
        open_page("Rajasthan")
    elif 460 <= x <= 500 and 520 <= y <= 560:
        open_page("Uttar Pradesh")
    elif 400 <= x <= 440 and 650 <= y <= 690:
        open_page("Madhya Pradesh")
    elif 160 <= x <= 200 and 650 <= y <= 690:
        open_page("Gujarat")
    elif 290 <= x <= 320 and 760 <= y <= 800:
        open_page("Maharashtra")
    elif 610 <= x <= 640 and 570 <= y <= 610:
        open_page("Bihar")
    elif 670 <= x <= 710 and 650 <= y <= 690:
        open_page("West Bengal")
    elif 590 <= x <= 620 and 630 <= y <= 670:
        open_page("Jharkhand")
    elif 490 <= x <= 530 and 700 <= y <= 740:
        open_page("Chhattisgarh")
    elif 580 <= x <= 620 and 740 <= y <= 780:
        open_page("Odisha")
    elif 390 <= x <= 420 and 830 <= y <= 870:
        open_page("Telangana")
    elif 400 <= x <= 440 and 910 <= y <= 950:
        open_page("Andhra Pradesh")
    elif 290 <= x <= 330 and 950 <= y <= 990:
        open_page("Karnataka")
    elif 380 <= x <= 420 and 1060 <= y <= 1100:
        open_page("Tamil Nadu")
    elif 310 <= x <= 340 and 1060 <= y <= 1100:
        open_page("Kerala")
    elif 230 <= x <= 260 and 910 <= y <= 950:
        open_page("Goa")
    elif 690 <= x <= 730 and 500 <= y <= 540:
        open_page("Sikkim")
    elif 780 <= x <= 820 and 560 <= y <= 600:
        open_page("Meghalaya")
    elif 830 <= x <= 870 and 520 <= y <= 560:
        open_page("Assam")
    elif 870 <= x <= 910 and 460 <= y <= 500:
        open_page("Arunachal Pradesh")
    elif 790 <= x <= 830 and 620 <= y <= 660:
        open_page("Tripura")
    elif 830 <= x <= 870 and 640 <= y <= 680:
        open_page("Mizoram")
    elif 860 <= x <= 900 and 590 <= y <= 630:
        open_page("Manipur")
    elif 880 <= x <= 920 and 550 <= y <= 590:
        open_page("Nagaland")
    elif 430 <= x <= 460 and 1030 <= y <= 1070:
        open_page("Puducherry")
    elif 850 <= x <= 880 and 1020 <= y <= 1060:
        open_page("Andaman and Nicobar Islands")
    elif 210 <= x <= 240 and 1080 <= y <= 1120:
        open_page("Lakshadweep")
    elif 340 <= x <= 370 and 470 <= y <= 500:
        open_page("Delhi")
    elif 340 <= x <= 370 and 400 <= y <= 440:
        open_page("Chandigarh")
    elif 140 <= x <= 170 and 720 <= y <= 760:
        open_page("Dadra and Nagar Haveli and Daman and Diu")
    elif 215 <= x <= 235 and 750 <= y <= 770:
        open_page("Dadra and Nagar Haveli and Daman and Diu")

root1 = Tk()
root1.title("India Map Tourism Explorer")
root1.configure(bg="#FFF8EB")
Label(root1, text="《INDIAN TOURIST GUIDER》", bg='#FFF8EB',fg='darkblue',font=("Arial", 30, "bold")).pack(pady=5) 
def select_item(event):
    if listbox.curselection():
        selected = listbox.get(listbox.curselection())
        entry1.delete(0, END)
        entry1.insert(0, selected)
        listbox.delete(0, END)
def search(event):
    typed = entry1.get().title()
    listbox.delete(0, END)
    for s in indian_cuisines:
        if s.startswith(typed):
            listbox.insert(END, s)
entry1 = Entry(root1)
entry1.pack()
entry1.bind("<KeyRelease>", search)
listbox = Listbox(root1, font=("Arial", 12), height=5)
listbox.pack()
listbox.bind("<<ListboxSelect>>", select_item)
def send_message1():
    user_input1 = entry1.get().strip()
    a=user_input1.title()
    if a not in indian_cuisines:
        show_warning()
        return
    if user_input1 == "": 
        return
    open_page(a) 
    entry1.delete(0, END)  
Button(root1, text="Send", command=send_message1,
       font=("Arial", 12), bg="black", fg="white").pack()

image_path = "map1.jpg"
img = Image.open(image_path)
photo = ImageTk.PhotoImage(img)
image_width, image_height = img.size
canvas = Canvas(root1, width=image_width, height=image_height)
canvas.pack()
canvas.create_image(0, 0, anchor=NW, image=photo)
canvas.create_text(368, 285, text="Ladakh", fill="red", font=("Arial", 5))
canvas.create_text(289, 311, text="Jammu\n& Kashmir", fill="red", font=("Arial", 5))
canvas.create_text(357, 375, text="Himachal \npradesh", fill="blue", font=("Arial", 5))
canvas.create_text(310, 406, text="Punjab", fill="blue", font=("Arial", 5))
canvas.create_text(431, 427, text="Uttarakhand", fill="blue", font=("Arial", 5))
canvas.create_text(327, 456, text="Haryana", fill="blue", font=("Arial", 5))
canvas.create_text(243, 539, text="Rajasthan", fill="blue", font=("Arial", 5))
canvas.create_text(464, 540, text="Uttar\nPradesh", fill="blue", font=("Arial", 5))
canvas.create_text(408, 668, text="Madhya\npradesh", fill="blue", font=("Arial", 5))
canvas.create_text(179, 667, text="Gujarat", fill="blue", font=("Arial", 5))
canvas.create_text(297, 782, text="Maharashtra", fill="blue", font=("Arial", 5))
canvas.create_text(616, 592, text="Bihar", fill="blue", font=("Arial", 5))
canvas.create_text(680, 668, text="West\nbangal", fill="blue", font=("Arial", 5))
canvas.create_text(602, 649, text="Jharkhand", fill="blue", font=("Arial", 5))
canvas.create_text(498, 722, text="Chattisgarh", fill="blue", font=("Arial", 5))
canvas.create_text(586, 762, text="Odissa", fill="blue", font=("Arial", 5))
canvas.create_text(399, 856, text="Telangana", fill="blue", font=("Arial", 5))
canvas.create_text(405, 933, text="Andhra\npradesh", fill="blue", font=("Arial", 5))
canvas.create_text(301, 971, text="karnataka", fill="blue", font=("Arial", 5))
canvas.create_text(391, 1091, text="Tamil\nnadu", fill="blue", font=("Arial", 5))
canvas.create_text(315, 1097, text="Kerala", fill="blue", font=("Arial", 5))
canvas.create_text(241, 926, text="Goa", fill="blue", font=("Arial", 5))
canvas.create_text(697, 517, text="Sikkim", fill="blue", font=("Arial", 5))
canvas.create_text(786, 581, text="Meghalaya", fill="blue", font=("Arial", 5))
canvas.create_text(844, 549, text="Assam", fill="blue", font=("Arial", 5))
canvas.create_text(878, 490, text="Arunachal\npradesh", fill="blue", font=("Arial", 5))
canvas.create_text(797, 639, text="Tripura", fill="blue", font=("Arial", 5))
canvas.create_text(841, 663, text="Mizoram", fill="blue", font=("Arial", 5))
canvas.create_text(863, 606, text="Manipur", fill="blue", font=("Arial", 5))
canvas.create_text(883, 563, text="Nagaland", fill="blue", font=("Arial", 5))
canvas.create_text(434, 1051, text="Puducherry", fill="red", font=("Arial", 5))
canvas.create_text(857, 1037, text="Andaman &\nNicobar island", fill="red", font=("Arial", 5))
canvas.create_text(222, 1100, text="Lakshadweep", fill="red", font=("Arial", 5))
canvas.create_text(351, 483, text="Delhi", fill="red", font=("Arial", 5))
canvas.create_text(348, 414, text="Chandigarh", fill="red", font=("Arial", 5))
canvas.create_text(151, 740, text="Daman\n&Diu", fill="red", font=("Arial", 5))
canvas.create_text(223, 765, text="Dadarnagar\n& Haveli", fill="red", font=("Arial", 5))
canvas.bind("<Button-1>", on_click)
        
Button(root1, text="AI help for travel", command=open_ai,bg='black',fg='white').place(x=10, rely=1.0, anchor='sw')

root1.mainloop()
