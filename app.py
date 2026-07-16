from flask import Flask, render_template, request, redirect, url_for
import requests

app = Flask(__name__)

# ფუნქცია ვალუტის კურსების რეალურ დროში წამოსაღებად ჩეხური კრონის (CZK) მიმართ
def get_exchange_rates():
    try:
        url = "https://open.er-api.com/v6/latest/CZK"
        response = requests.get(url, timeout=5)
        data = response.json()
        if data and "rates" in data:
            return {
                "GEL": data["rates"].get("GEL", 0.12),
                "USD": data["rates"].get("USD", 0.043),
                "EUR": data["rates"].get("EUR", 0.040)
            }
    except Exception as e:
        print(f"ვალუტის კურსის წამოღების შეცდომა: {e}")
    return {"GEL": 0.12, "USD": 0.043, "EUR": 0.040}

# დინამიკური ლოკაციების ბაზა (ორენოვანი)
LOCATIONS = [
    # --- სანახაობები ---
    {
        "title": "Charles Bridge",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "პრაღის ყველაზე ცნობილი და საკულტო ისტორიული ხიდი. საუკეთესო დრო სანახავად არის დილის 6-7 საათი, სანამ ბევრი ტურისტი მოვა.",
        "description_en": "Prague's most famous iconic historic bridge. Best time to visit is early morning around 6-7 AM before crowds arrive.",
        "location": "Karlův most, Prague 1",
        "price_czk": 0,
        "price_text": "0 CZK",
        "working_hours": "24/7",
        "image": "https://images.unsplash.com/photo-1519671482749-fd09be7ccebf?auto=format&fit=crop&w=800&q=80",
        "map_query": "Charles Bridge, Prague 1"
    },
    {
        "title": "Prague Castle",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "მსოფლიოში უდიდესი უძველესი ციხესიმაგრის კომპლექსი, სადაც მდებარეობს მეფეთა სასახლეები, საოცარი წმინდა ვიტის გოთიკური ტაძარი და ოქროს ქუჩა.",
        "description_en": "The largest ancient castle complex in the world, featuring royal palaces, the magnificent St. Vitus Cathedral, and Golden Lane.",
        "location": "Hradčany, Prague 1",
        "price_czk": 250,
        "price_text": "250 CZK",
        "working_hours": "06:00 - 22:00",
        "image": "https://images.unsplash.com/photo-1541849546-216549ae216d?auto=format&fit=crop&w=800&q=80",
        "map_query": "Prague Castle, Prague 1"
    },
    {
        "title": "Prague Astronomical Clock",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "მსოფლიოში უძველესი დღემდე მოქმედი ასტრონომიული საათი ძველი ქალაქის მოედანზე.",
        "description_en": "The world's oldest operating astronomical clock in Old Town Square.",
        "location": "Staroměstské náměstí 1, Prague 1",
        "price_czk": 250,
        "price_text": "250 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1563805042-7684c019e1cb?auto=format&fit=crop&w=800&q=80",
        "map_query": "Prague Astronomical Clock, Prague 1"
    },
    {
        "title": "Prague Zoo",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "მსოფლიოში ერთ-ერთი საუკეთესო ზოოპარკი. პრაღა 1-დან მისასვლელად: მეტრო C-თი Nádraží Holešovice-მდე -> #112 ავტობუსი (20-25 წთ). ბილეთი: 30-40 CZK.",
        "description_en": "One of the world's best zoos. From Prague 1: Metro C to Nádraží Holešovice -> Bus #112 (20-25 min). Ticket: 30-40 CZK.",
        "location": "U Trojského zámku 120/3, Prague 7",
        "price_czk": 330,
        "price_text": "330 CZK",
        "working_hours": "09:00 - 18:00",
        "image": "https://images.unsplash.com/photo-1534567153574-2b12153a87f0?auto=format&fit=crop&w=800&q=80",
        "map_query": "Prague Zoo, Prague 7"
    },

    # --- რესტორნები ---
    {
        "title": "Havelská Koruna",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "საუკეთესო ბიუჯეტური არჩევანი ibis Praha Old Town-თან ახლოს. თვითმომსახურების ტრადიციული ჩეხური სასადილო.",
        "description_en": "Best budget choice near ibis Praha Old Town. Self-service traditional Czech canteen.",
        "location": "Havelská 21, Prague 1",
        "price_czk": 250,
        "price_text": "200-350 CZK",
        "working_hours": "10:00 - 20:00",
        "image": "https://images.unsplash.com/photo-1555396273-367ea4eb4db5?auto=format&fit=crop&w=800&q=80",
        "map_query": "Havelska Koruna, Prague 1"
    },
    {
        "title": "Lokál Dlouhááá",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "ცნობილია ტანკიდან პირდაპირ ჩამოცხელებული Pilsner Urquell-ის ლუდითა და ავთენტური კერძებით.",
        "description_en": "Famous for fresh tank Pilsner Urquell beer and authentic dishes.",
        "location": "Dlouhá 33, Prague 1",
        "price_czk": 350,
        "price_text": "250-450 CZK",
        "working_hours": "11:00 - 00:00",
        "image": "https://images.unsplash.com/photo-1538488881022-47576f71d5a8?auto=format&fit=crop&w=800&q=80",
        "map_query": "Lokal Dlouhaa, Prague 1"
    },
    {
        "title": "Loď Pivovar",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "უნიკალური მცურავი ლუდსახარში და რესტორანი მდინარე ვლტავაზე, საიდანაც პრაღის ულამაზესი ხედები იშლება.",
        "description_en": "Unique brewery boat on the Vltava river, offering great house-brewed beer and river views.",
        "location": "Dvořákovo nábř. Štefánikův most, Prague 1",
        "price_czk": 380,
        "price_text": "380 CZK",
        "working_hours": "11:30 - 23:00",
        "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=800&q=80",
        "map_query": "Lod Pivovar, Prague 1"
    },

    # --- შოპინგი ---
    {
        "title": "Palladium",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "პრაღის ცენტრში მდებარე ყველაზე ცნობილი სავაჭრო ცენტრი 200-ზე მეტი მაღაზიით.",
        "description_en": "Prague's most famous central shopping mall featuring over 200 stores.",
        "location": "Náměstí Republiky 1, Prague 1",
        "price_czk": 1500,
        "price_text": "1500 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1567449303078-57ad995bd301?auto=format&fit=crop&w=800&q=80",
        "map_query": "Palladium, Namesti Republiky, Prague 1"
    }
]

@app.route('/')
def home():
    rates = get_exchange_rates()
    return render_template('index.html', locations=LOCATIONS, rates=rates)

@app.route('/itinerary')
def itinerary():
    rates = get_exchange_rates()
    return render_template('itinerary.html', rates=rates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
