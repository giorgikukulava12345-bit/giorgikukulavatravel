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
        print(f"ვალუტის კურსის შეცდომა: {e}")
    return {"GEL": 0.12, "USD": 0.043, "EUR": 0.040}

# დინამიკური ლოკაციების სრული ბაზა (ლოკალური ფაილებით static საქაღალდიდან)
LOCATIONS = [
    # =========================================================
    # --- სანახაობები (static/ საქაღალდის ფაილები) ---
    # =========================================================
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
        "image": "/static/Charles Bridge.png",
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
        "image": "/static/prague castle.png",
        "map_query": "Prague Castle, Prague 1"
    },
    {
        "title": "Prague Astronomical Clock",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "მსოფლიოში უძველესი დღემდე მოქმედი ასტრონომიული საათი ძველი ქალაქის მოედანზე. ყოველ საათში აქ იწყება მოციქულთა მსვლელობის წარმოდგენა.",
        "description_en": "The world's oldest operating astronomical clock in Old Town Square. Every hour features a mechanical show of the Twelve Apostles.",
        "location": "Staroměstské náměstí 1, Prague 1",
        "price_czk": 250,
        "price_text": "250 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "/static/prague astronomical clock.png",
        "map_query": "Prague Astronomical Clock, Prague 1"
    },
    {
        "title": "Old Town Square",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "პრაღის ისტორიული გული, გარშემორტყმული გოთიკური და ბაროკოს სტილის არქიტექტურით, კაფეებითა და ტინ ტაძრის შპილებით.",
        "description_en": "Prague's historic heart, surrounded by gothic and baroque architecture, cafes, and the twin spires of Týn Church.",
        "location": "Staroměstské náměstí, Prague 1",
        "price_czk": 0,
        "price_text": "0 CZK",
        "working_hours": "24/7",
        "image": "/static/old town square.png",
        "map_query": "Old Town Square, Prague 1"
    },
    {
        "title": "Lennon Wall",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "თავისუფლებისა და მშვიდობის სიმბოლო მალა სტრანაში, რომელიც დაფარულია ჯონ ლენონის, ბითლზის ლირიკისა და გრაფიტის ფერადი ნახატებით.",
        "description_en": "Symbol of freedom and peace in Malá Strana, covered in colorful John Lennon graffiti, Beatles lyrics, and political art.",
        "location": "Velkopřevorské náměstí, Prague 1",
        "price_czk": 0,
        "price_text": "0 CZK",
        "working_hours": "24/7",
        "image": "/static/Lennon Wall.png",
        "map_query": "John Lennon Wall, Prague 1"
    },
    {
        "title": "Wenceslas Square",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "პრაღის მთავარი ბულვარი და ისტორიული მოედანი, სადაც მდებარეობს ეროვნული მუზეუმი და წმინდა ვაცლავის ქანდაკება.",
        "description_en": "Prague's main boulevard and cultural center, dominated by the National Museum and St. Wenceslas statue.",
        "location": "Václavské náměstí, Prague 1",
        "price_czk": 0,
        "price_text": "0 CZK",
        "working_hours": "24/7",
        "image": "/static/Prague Wenceslas Square.png",
        "map_query": "Wenceslas Square, Prague 1"
    },
    {
        "title": "Dancing House",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "ფრენკ გერის მიერ დაპროექტებული ავანგარდული არქიტექტურული შედევრი მდინარე ვლტავას ნაპირზე, რომელსაც ცეკვის ფორმა აქვს.",
        "description_en": "Frank Gehry's avant-garde architectural masterpiece on the Vltava riverbank, resembling a dancing couple.",
        "location": "Jiráskovo náměstí 6, Prague 2",
        "price_czk": 0,
        "price_text": "0 CZK",
        "working_hours": "10:00 - 22:00",
        "image": "/static/Prague Dancing House.png",
        "map_query": "Dancing House, Prague 2"
    },
    {
        "title": "Vyšehrad Fortress",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "X საუკუნის ისტორიული ციხესიმაგრე ბორცვზე. აქიდან იშლება პრაღისა და მდინარე ვლტავას საოცარი პანორამული ხედები.",
        "description_en": "X century historic fort on a hill, offering panoramic views of Prague, the Vltava River, and peaceful gardens.",
        "location": "V Pevnosti 159/5b, Prague 2",
        "price_czk": 0,
        "price_text": "0 CZK",
        "working_hours": "09:00 - 18:00",
        "image": "/static/Vyšehrad Fortress.png",
        "map_query": "Vysehrad, Prague 2"
    },
    {
        "title": "Petřín Lookout Tower",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "პარიზის ეიფელის კოშკის მინიატურული ჩეხური ვერსია პეტრინის ბორცვზე. კოშკიდან მთელი პრაღის ულამაზესი ხედი იშლება.",
        "description_en": "Miniature Czech version of Paris' Eiffel Tower atop Petřín Hill, providing sweeping panoramic views over Prague.",
        "location": "Petřínské sady 633, Prague 5",
        "price_czk": 150,
        "price_text": "150 CZK",
        "working_hours": "10:00 - 20:00",
        "image": "/static/Petřín Tower.png",
        "map_query": "Petrin Tower, Prague 5"
    },
    {
        "title": "Letná Park & Metronome",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "პრაღის ერთ-ერთი საუკეთესო პარკი ბორცვზე გიგანტური მეტრონომით, ცნობილი ლუდის ბაღითა და ხიდების პანორამული ხედით.",
        "description_en": "Hilltop park featuring a giant functioning metronome, popular beer garden, and best viewpoint over Prague's bridges.",
        "location": "Letenské sady, Prague 7",
        "price_czk": 0,
        "price_text": "0 CZK",
        "working_hours": "24/7",
        "image": "https://images.unsplash.com/photo-1513581166391-887a96ddeafd?auto=format&fit=crop&w=800&q=80",
        "map_query": "Letna Park, Prague 7"
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
    {
        "title": "Sedlec Ossuary",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "უნიკალური მისტიკური სამლოცველო კუტნა ჰორაში, გაფორმებული 40,000-ზე მეტი ადამიანის ძვლით.",
        "description_en": "Unique chapel in Kutná Hora, artisticly decorated with bones of over 40,000 human skeletons.",
        "location": "Zámecká, Kutná Hora",
        "price_czk": 180,
        "price_text": "180 CZK",
        "working_hours": "09:00 - 17:00",
        "image": "/static/Sedlec Ossuary.png",
        "map_query": "Sedlec Ossuary, Kutna Hora"
    },
    {
        "title": "Český Krumlov Castle",
        "category": "სანახაობა",
        "category_en": "Sightseeing",
        "description_ka": "ზღაპრული შუა საუკუნეების ციხესიმაგრე და ქალაქი სამხრეთ ბოჰემიაში. ჩეხეთის სიდიდით მეორე ციხესიმაგრე UNESCO-ს სიიდან.",
        "description_en": "Fairy-tale medieval castle complex in South Bohemia. Czechia's second-largest castle, listed by UNESCO.",
        "location": "Zámek 59, Český Krumlov",
        "price_czk": 150,
        "price_text": "150 CZK",
        "working_hours": "09:00 - 17:00",
        "image": "/static/Český Krumlov Castle.png",
        "map_query": "State Castle Český Krumlov"
    },

    # =========================================================
    # --- რესტორნები ---
    # =========================================================
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
        "description_ka": "პოპულარული ჩეხური რესტორანი ძველ ქალაქში. ცნობილია ტანკიდან პირდაპირ ჩამოცხელებული Pilsner Urquell-ის ლუდითა და ავთენტური კერძებით.",
        "description_en": "Famous Czech restaurant in Old Town. Known for fresh tank Pilsner Urquell beer and authentic dishes.",
        "location": "Dlouhá 33, Prague 1",
        "price_czk": 350,
        "price_text": "250-450 CZK",
        "working_hours": "11:00 - 00:00",
        "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=800&q=80",
        "map_query": "Lokal Dlouhaa, Prague 1"
    },
    {
        "title": "Pizza Nuova",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "უგემრიელესი პიცა და პასტა. შესანიშნავი ადგილმდებარეობა და იდეალური არჩევანია ბავშვებთან ერთად ვახშმობისთვის.",
        "description_en": "Delicious pizza and pasta. Great location and ideal choice when dining with kids.",
        "location": "Revoluční 1, Prague 1",
        "price_czk": 350,
        "price_text": "350 CZK",
        "working_hours": "11:30 - 23:00",
        "image": "https://images.unsplash.com/photo-1513104890138-7c749659a591?auto=format&fit=crop&w=800&q=80",
        "map_query": "Pizza Nuova, Prague 1"
    },
    {
        "title": "Café Imperial",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "ულამაზესი ისტორიული ინტერიერი, არტ-დეკოს სტილი და გემრიელი ჩეხური/ევროპული სამზარეულო.",
        "description_en": "Beautiful historic art-deco interior and delicious Czech/European cuisine.",
        "location": "Na Poříčí 15, Prague 1",
        "price_czk": 450,
        "price_text": "450 CZK",
        "working_hours": "07:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1517248135467-4c7edcad34c4?auto=format&fit=crop&w=800&q=80",
        "map_query": "Cafe Imperial, Prague 1"
    },
    {
        "title": "Staroměstský pivovar U Supa",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "პრაღის ერთ-ერთი უძველესი ლუდსახარში ძველი ქალაქის ცენტრში (ibis-დან 5-7 წუთი). გამოირჩევა გამჭვირვალე ავზებითა და ნახევრად მუქი ლუდით.",
        "description_en": "One of Prague's oldest breweries in Old Town (5-7 min from ibis). Features visible brew kettles and signature semi-dark beer.",
        "location": "Celetná 563/22, Prague 1",
        "price_czk": 420,
        "price_text": "420 CZK",
        "working_hours": "11:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1436076863939-06870fe779c2?auto=format&fit=crop&w=800&q=80",
        "map_query": "U Supa, Celetna, Prague 1"
    },
    {
        "title": "U Kunštátů",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "მყუდრო ეზო ძველ ქალაქში და ჩეხური კრაფტ-ლუდების უზარმაზარი, მრავალფეროვანი არჩევანი.",
        "description_en": "Cozy courtyard in Old Town featuring a huge selection of Czech craft beers.",
        "location": "Řetězová 3, Prague 1",
        "price_czk": 300,
        "price_text": "300 CZK",
        "working_hours": "14:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1572116469696-31de0f17cc34?auto=format&fit=crop&w=800&q=80",
        "map_query": "U Kunstatu, Prague 1"
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
        "image": "https://images.unsplash.com/photo-1543007630-9710e4a00a20?auto=format&fit=crop&w=800&q=80",
        "map_query": "Lod Pivovar, Prague 1"
    },
    {
        "title": "U Fleků",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "პრაღის ყველაზე ძველი მოქმედი ლუდსახარში (1499 წლიდან). ცნობილია თავისი უნიკალური მუქი ლუდით (Dark Lager) და ტრადიციული კერძებით.",
        "description_en": "Prague's oldest operating brewery (since 1499). Famous for its unique dark lager and traditional dishes.",
        "location": "Křemencova 11, Prague 1",
        "price_czk": 400,
        "price_text": "400 CZK",
        "working_hours": "10:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1518176258769-f227c798150e?auto=format&fit=crop&w=800&q=80",
        "map_query": "U Fleku, Kremencova, Prague 1"
    },
    {
        "title": "Strahov Monastery Brewery",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "XVII საუკუნის ისტორიული სამონასტრო ლუდსახარში პრაღის ციხესიმაგრესთან ახლოს. ცნობილია საფირმო 'St. Norbert' ლუდითა და უგემრიელესი სამზარეულოთი.",
        "description_en": "Historic XVII century monastic brewery near Prague Castle. Famous for its signature 'St. Norbert' beer and delicious cuisine.",
        "location": "Strahovské nádvoří 301, Prague 1",
        "price_czk": 450,
        "price_text": "450 CZK",
        "working_hours": "10:00 - 22:00",
        "image": "https://images.unsplash.com/photo-1584225065152-4a1454aa3d4e?auto=format&fit=crop&w=800&q=80",
        "map_query": "Strahov Monastery Brewery, Prague 1"
    },
    {
        "title": "Lokál U Bílé kuželky",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "პოპულარული ჩეხური პაბი კარლის ხიდთან ახლოს. გამოირჩევა უახლესი Pilsner Urquell-ის ავზის ლუდითა და კლასიკური ჩეხური წასახემსებლებით.",
        "description_en": "Popular Czech pub near Charles Bridge. Features fresh Pilsner Urquell tank beer and classic Czech snacks.",
        "location": "Míšeňská 12, Prague 1",
        "price_czk": 350,
        "price_text": "350 CZK",
        "working_hours": "11:00 - 00:00",
        "image": "https://images.unsplash.com/photo-1538488881022-47576f71d5a8?auto=format&fit=crop&w=800&q=80",
        "map_query": "Lokal U Bile kuzelky, Prague 1"
    },
    {
        "title": "U Zlatého tygra",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "ლეგენდარული ისტორიული პაბი ძველ ქალაქში. აქ იყრიდნენ თავს ცნობილი მწერლები და პოლიტიკოსები უმაღლესი ხარისხის ჩეხური ლუდის დასალევად.",
        "description_en": "Legendary historic pub in Old Town. Famous writers and politicians gathered here to enjoy top-quality Czech beer.",
        "location": "Husova 228/17, Prague 1",
        "price_czk": 300,
        "price_text": "300 CZK",
        "working_hours": "15:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1514933651103-005eec06c04b?auto=format&fit=crop&w=800&q=80",
        "map_query": "U Zlateho tygra, Husova, Prague 1"
    },
    {
        "title": "Pivovar U Medvídků",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "XV საუკუნის ისტორიული ლუდსახარში და ტრადიციული რესტორანი. ცნობილია თავისი ძლიერი საფირმო მუქი ლუდით 'X33' და ავთენტური გარემოთი.",
        "description_en": "XV century historic brewery and traditional restaurant. Famous for its strong signature dark beer 'X33' and authentic ambiance.",
        "location": "Na Perštýně 345/7, Prague 1",
        "price_czk": 380,
        "price_text": "380 CZK",
        "working_hours": "11:30 - 23:00",
        "image": "https://images.unsplash.com/photo-1608270586620-248524c67de9?auto=format&fit=crop&w=800&q=80",
        "map_query": "U Medvidku, Prague 1"
    },
    {
        "title": "Pivovar Národní",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "ეროვნულ თეატრთან ახლოს მდებარე მიკრო-ლუდსახარში, რომელსაც აქვს დიდი შიდა ეზო/ბაღი და სთავაზობს სტუმრებს ადგილზე მოხარშულ 'Czech Lion' ლუდს.",
        "description_en": "Microbrewery near the National Theatre featuring a large beer garden and house-brewed 'Czech Lion' beer.",
        "location": "Národní 8, Prague 1",
        "price_czk": 370,
        "price_text": "370 CZK",
        "working_hours": "11:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1575444758702-4a6b9222336e?auto=format&fit=crop&w=800&q=80",
        "map_query": "Pivovar Narodni, Prague 1"
    },
    {
        "title": "Pivovarský dům Benedict",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "ცნობილი რესტორანი თავისი მიკრო-ლუდსახარშით, სადაც ტრადიციულ ლუდთან ერთად შეგიძლიათ გასინჯოთ სხვადასხვა ექსპერიმენტული არომატებიც.",
        "description_en": "Renowned restaurant with a microbrewery, offering traditional brews along with unique experimental flavors.",
        "location": "Ječná 511/16, Prague 2",
        "price_czk": 360,
        "price_text": "360 CZK",
        "working_hours": "11:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1567620905732-2d1ec7ab7445?auto=format&fit=crop&w=800&q=80",
        "map_query": "Pivovarsky dum Benedict, Prague 2"
    },
    {
        "title": "Dva kohouti",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "პოპულარული კრაფტ-ლუდსახარში და თაფრუმი კარლინის ტრენდულ უბანში. შესანიშნავი ადგილია როგორც კლასიკური ჩეხური ლაგერების, ასევე ინოვაციური ელების დასაგემოვნებლად.",
        "description_en": "Popular craft microbrewery and taproom in trendy Karlín. Great place to enjoy classic Czech lagers and innovative ales.",
        "location": "Sokolovská 81/55, Prague 8",
        "price_czk": 320,
        "price_text": "320 CZK",
        "working_hours": "15:00 - 01:00",
        "image": "https://images.unsplash.com/photo-1511527661048-7fe73d85e9a4?auto=format&fit=crop&w=800&q=80",
        "map_query": "Dva kohouti, Prague 8"
    },
    {
        "title": "Vinohradský pivovar",
        "category": "რესტორანი",
        "category_en": "Restaurant",
        "description_ka": "თანამედროვე მიკრო-ლუდსახარში ვინოჰრადის რაიონში. გთავაზობთ ადგილზე მოხარშულ გაუფილტრავ ლუდსა და უგემრიელეს ტრადიციულ სამზარეულოს.",
        "description_en": "Modern microbrewery in the Vinohrady district. Offers locally brewed unfiltered beer and delicious traditional food.",
        "location": "Korunní 2506/106, Prague 10",
        "price_czk": 350,
        "price_text": "350 CZK",
        "working_hours": "11:00 - 23:00",
        "image": "https://images.unsplash.com/photo-1532635241-17e820acc59f?auto=format&fit=crop&w=800&q=80",
        "map_query": "Vinohradsky pivovar, Prague 10"
    },

    # =========================================================
    # --- შოპინგი ---
    # =========================================================
    {
        "title": "Palladium",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "პრაღის ცენტრში მდებარე ყველაზე ცნობილი და უდიდესი სავაჭრო ცენტრი 200-ზე მეტი მაღაზიითა და უამრავი რესტორნით.",
        "description_en": "Prague's most famous central shopping mall featuring over 200 stores, cafes, and restaurants.",
        "location": "Náměstí Republiky 1, Prague 1",
        "price_czk": 1500,
        "price_text": "1500 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1567449303078-57ad995bd301?auto=format&fit=crop&w=800&q=80",
        "map_query": "Palladium, Namesti Republiky, Prague 1"
    },
    {
        "title": "Myslbek Shopping Gallery",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "ელეგანტური სავაჭრო პასაჟი პრაღის მთავარ საფეხმავლო ქუჩაზე. იდეალურია ცნობილი ბრენდების მშვიდი შოპინგისთვის.",
        "description_en": "Elegant shopping passage on Prague's main pedestrian street. Perfect for quiet shopping for popular brands.",
        "location": "Na Příkopě 19-21, Prague 1",
        "price_czk": 1100,
        "price_text": "1100 CZK",
        "working_hours": "09:00 - 20:00",
        "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=800&q=80",
        "map_query": "Myslbek Shopping Gallery, Prague 1"
    },
    {
        "title": "Slovanský Dům",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "ისტორიული სავაჭრო კომპლექსი პრაღა 1-ში, პრემიუმ მაღაზიებით, კინოთეატრითა და ულამაზესი შიდა ბაღით.",
        "description_en": "Historic shopping complex in Prague 1 featuring premium stores, a cinema, and a beautiful courtyard garden.",
        "location": "Na Příkopě 22, Prague 1",
        "price_czk": 1400,
        "price_text": "1400 CZK",
        "working_hours": "10:00 - 22:00",
        "image": "https://images.unsplash.com/photo-1555529669-e69e7aa0ba9a?auto=format&fit=crop&w=800&q=80",
        "map_query": "Slovansky Dum, Prague 1"
    },
    {
        "title": "Černá Růže",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "ისტორიული სავაჭრო პასაჟი ძველ ქალაქში, ცნობილი ბუტიკებით, ჩეხური მინისა და ბროლის ექსკლუზიური მაღაზიებით.",
        "description_en": "Historic shopping arcade in Old Town, famous for boutiques and exclusive Czech glass and crystal shops.",
        "location": "Na Příkopě 12, Prague 1",
        "price_czk": 1300,
        "price_text": "1300 CZK",
        "working_hours": "10:00 - 20:00",
        "image": "https://images.unsplash.com/photo-1513151233558-d860c5398176?auto=format&fit=crop&w=800&q=80",
        "map_query": "Cerna Ruze, Prague 1"
    },
    {
        "title": "Quadrio",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "თანამედროვე სავაჭრო ცენტრი მეტრო Národní Třída-სთან უშუალოდ, ფრანც კაფკას მოძრავი თავის ქანდაკების გვერდით.",
        "description_en": "Modern shopping center directly above Národní Třída metro station, next to the kinetic Franz Kafka head sculpture.",
        "location": "Spálená 2121/22, Prague 1",
        "price_czk": 1200,
        "price_text": "1200 CZK",
        "working_hours": "08:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1519567241046-7f570eee3ce6?auto=format&fit=crop&w=800&q=80",
        "map_query": "Quadrio Shopping Station, Prague 1"
    },
    {
        "title": "Vinohradská Pavilon",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "დიზაინერული და ინტერიერის ავეჯის პრემიუმ სავაჭრო ცენტრი, განთავსებული ვინოჰრადის ისტორიულ ბაზრის შენობაში.",
        "description_en": "Premium design and interior shopping center housed in a historic Vinohrady market hall.",
        "location": "Vinohradská 1200/50, Prague 2",
        "price_czk": 1800,
        "price_text": "1800 CZK",
        "working_hours": "10:00 - 19:30",
        "image": "https://images.unsplash.com/photo-1581417478175-a9ef18f210c2?auto=format&fit=crop&w=800&q=80",
        "map_query": "Vinohradsky Pavilon, Prague 2"
    },
    {
        "title": "Atrium Flora",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "პოპულარული 4-სართულიანი სავაჭრო ცენტრი 130-ზე მეტი მაღაზიითა და ერთადერთი IMAX 3D კინოთეატრით პრაღაში.",
        "description_en": "Popular 4-story shopping mall with over 130 stores and Prague's only IMAX 3D cinema.",
        "location": "Vinohradská 151, Prague 3",
        "price_czk": 1200,
        "price_text": "1200 CZK",
        "working_hours": "08:00 - 00:00",
        "image": "https://images.unsplash.com/photo-1567449303078-57ad995bd301?auto=format&fit=crop&w=800&q=80",
        "map_query": "Atrium Flora, Prague 3"
    },
    {
        "title": "Nový Smíchov",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "ძალიან პოპულარული და დიდი სამსართულიანი მოლი მეტრო Anděl-თან. იდეალური ადგილია შოპინგისა და გასართობად.",
        "description_en": "Highly popular 3-story mall directly at Anděl metro station. Excellent spot for shopping and entertainment.",
        "location": "Plzeňská 8, Prague 5",
        "price_czk": 1200,
        "price_text": "1200 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1519567241046-7f570eee3ce6?auto=format&fit=crop&w=800&q=80",
        "map_query": "OC Novy Smichov, Prague 5"
    },
    {
        "title": "Galerie Harfa",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "დიდი სავაჭრო ცენტრი O2 არენას გვერდით, ცნობილი სახურავზე განთავსებული დინოზავრების პარკითა და ყინულის მოედნით.",
        "description_en": "Large shopping center next to O2 Arena, famous for its rooftop DinoPark and ice-skating rink.",
        "location": "Českomoravská 2420/15a, Prague 9",
        "price_czk": 1100,
        "price_text": "1100 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1567449303078-57ad995bd301?auto=format&fit=crop&w=800&q=80",
        "map_query": "Galerie Harfa, Prague 9"
    },
    {
        "title": "OC Eden",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "მოსახერხებელი საოჯახო სავაჭრო ცენტრი ვრშოვიცეს რაიონში, დიდი ჰიპერმარკეტითა და ყოველდღიური მაღაზიებით.",
        "description_en": "Convenient family shopping center in Vršovice with a large hypermarket and daily retail stores.",
        "location": "U Slavie 1527, Prague 10",
        "price_czk": 900,
        "price_text": "900 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1513151233558-d860c5398176?auto=format&fit=crop&w=800&q=80",
        "map_query": "NC Eden, Prague 10"
    },
    {
        "title": "Fashion Arena Prague Outlet",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "პრაღის ყველაზე დიდი აუტლეტ-ცენტრი, სადაც მსოფლიო ბრენდების ტანსაცმელი იყიდება 30%-დან 70%-მდე ფასდაკლებით.",
        "description_en": "Prague's largest outlet center offering global designer brands at 30% to 70% discounts year-round.",
        "location": "Zamenhofova 440, Prague 10",
        "price_czk": 1600,
        "price_text": "1600 CZK",
        "working_hours": "10:00 - 20:00",
        "image": "https://images.unsplash.com/photo-1441986300917-64674bd600d8?auto=format&fit=crop&w=800&q=80",
        "map_query": "Fashion Arena Prague Outlet, Prague 10"
    },
    {
        "title": "Westfield Chodov",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "ჩეხეთის ყველაზე დიდი სავაჭრო ცენტრი 300-ზე მეტი მაღაზიით, მსოფლიო ბრენდებითა და უზარმაზარი კინოთეატრით.",
        "description_en": "Czech Republic's largest shopping center featuring over 300 stores, global fashion brands, and a massive cinema.",
        "location": "Roztylská 2321/19, Prague 11",
        "price_czk": 2000,
        "price_text": "2000 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1519567241046-7f570eee3ce6?auto=format&fit=crop&w=800&q=80",
        "map_query": "Westfield Chodov, Prague 11"
    },
    {
        "title": "Centrum Černý Most",
        "category": "შოპინგი",
        "category_en": "Shopping",
        "description_ka": "თანამედროვე და ვრცელი სავაჭრო ცენტრი პრაღის აღმოსავლეთით, დიდი მაღაზიებით, კინოთეატრითა და საბავშვო ზონებით.",
        "description_en": "Modern and spacious shopping mall in eastern Prague with flagship stores, cinema, and kids' zones.",
        "location": "Chlumecká 765/6, Prague 14",
        "price_czk": 1000,
        "price_text": "1000 CZK",
        "working_hours": "09:00 - 21:00",
        "image": "https://images.unsplash.com/photo-1567449303078-57ad995bd301?auto=format&fit=crop&w=800&q=80",
        "map_query": "Centrum Cerny Most, Prague 14"
    }
]

@app.route('/')
def home():
    rates = get_exchange_rates()
    return render_template('index.html', locations=LOCATIONS, rates=rates)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
