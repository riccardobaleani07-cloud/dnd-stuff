import json
from collections import defaultdict

def build_transitions(names):
    #Build a letter-transition map with probabilities from a list of names.
    transitions = defaultdict(lambda: defaultdict(int))

    # Count transitions
    for name in names:
        name = "/" + name.lower() + "$"
        for i in range(len(name) - 1):
            current_letter = name[i]
            next_letter = name[i + 1]
            transitions[current_letter][next_letter] += 1
        # Boost ending probability for last letter
        last_letter = name[-2]
        transitions[last_letter]["$"] += 1  # extra weight to end the name

    # Convert counts to probabilities
    prob_map = {}
    for current, next_letters in transitions.items():
        total = sum(next_letters.values())
        prob_map[current] = [[letter, count / total] for letter, count in next_letters.items()]

    return prob_map

def train_element_styles(element_styles):
    #Given a dict of {style_name: list_of_names}, return a dict of transition maps.
    transition_data = {}
    for style, elements in element_styles.items():
        transition_data[style] = build_transitions(elements)
    return transition_data

def save_to_json(data, filename=r"NPC generator/npc_static_data/names_transition.json"):
    with open(filename, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4)

if __name__ == "__main__":
    # name styles: sample names per style, the more the names hte better. it counts spaces and every other symbol except / and & wich are reserved logic (act as start or end of a name)
    name_styles = {
        "Human": [
            "Alaric", "Brianne", "Cedric", "Donna", "Elara", "Felix", "Gerald", "Helena", "Ismaele", "Jason", "Kevin",
            "Lalatina", "Marco", "Noah", "Ofelia", "Persefone", "Quantin", "Riccardo", "Selene", "Thomas", "Ulisse", "Valentina",
            "Xeno", "Yemen", "Zarina", "Gaia", "Maverik", "Enrico", "Diana", "Floreano", "Francesco", "Ruben", "Ester", "Iris",
            "Omar", "Giallo", "Martina", "Lorenzo", "Anna", "Tristano", "Alexandra", "Walter", "Lea", "Nico", "Enrico", "Paolo",
            "O'Brian", "Barac", "O'Diren", "Noemi", "Chiara", "Laura", "Angela", "Checco", "Gherti", "Shaggy", "Amy", "Hawkeye", "Alex"],
        "Fairy": [
            "Ael", "Indra", "Caelith", "Eryndor", "Lúthien", "Sylvar", "Thali", "Faelwen", "Naeris", "Olorin", "Van", "Yarin",
            "Rory", "Ashelith", "Nofryl", "Elan", "Drin", "Agathay", "Salawen", "Mòvethin", "Drieden", "Co", "Hosly", "Phens", "Hole",
            "Anàsin", "Sylphiet", "Seraph", "Floy", "Gresh", "Theve", "Snyl", "Bish", "Lesil", "Shugar", "Murphy", "Sàforien",
            "Olemif", "Noòl", "Meth", "Ilàmai", "Rufòniel", "Aisbowe", "Púth", "Ien", "Weona", "Iseth", "Loafàir", "Vusmiel", "Therònoe",
            "Iel", "Ifix", "Exohalme", "Sylvan", "Zelenfesh", "Yuna", "Runa", "Fenril", "Shin", "Tori", "Lútrha", "Vent", "Hril", "Nomoe",
            "Heliarin", "Taviel", "Valesin", "Firael", "Nethira", "Calenor", "Virel", "Eriath", "Belanor", "Khae", "Len",
            "Hirwen", "Aethira", "Lorien", "Nivael", "Thir"],
        "Dwarvish": [
            "Balgrim", "Dorin", "Thaldrun", "Gruntha", "Kragni", "Borim", "Marduk", "Rundal", "Storn", "Vold", "Rik",
            "Bralda", "Helg", "Rin", "Durval", "Thorek", "Gilda", "Nornik", "Tor", "Dra", "Khel", "Den", "Bromir", "Gundra",
            "Faldan", "Drorim", "Ulgrim", "Kar", "Neth", "Begin", "Thurma", "Dorun", "Mag", "Roldra", "Kharn",
            "Thogil", "Grundeth", "Molra", "Varnin", "Duga", "Bral", "Dir", "Khurim", "Tagnar", "Helda", "Droven"],
        "Draconic": [
            "Dravon", "Thraz", "Gul", "Sarth", "Urion", "Oroxion", "Vira", "Athar", "Kraenor", "Zauriel", "Qyveran", "Shald", "Rith",
            "Azhur", "Iel", "Vorthan", "Xarnoth", "Kaelzor", "Rhazir", "Thornax", "Zerathul", "Saviir", "Kraveth", "Morath", "Draziel",
            "Shyrix", "Velkar", "Qorion", "Tharzul", "Rhaegal", "Sith", "Rix", "Azrakel", "Vaelorn", "Dravix", "Kurnash",
            "Xivren", "Zhaqor", "Othraen", "Varnath", "Quoril", "Thalvash", "Rhazaan", "Serith", "Kyrion", "Drakmar"],
        "Wildermagic": [
            "Bodrik", "Drooga", "Glippa", "Trubbit", "Plimbo", "Gribna", "Dablik", "Moglin", "Froble", "Baludo",
            "Klanka", "Palli", "Lomper", "Drubbik", "Nogba", "Thoblin", "Groota", "Wigbel", "Lumpo", "Plonka",
            "Druffi", "Glimmera", "Bunli", "Flooba", "Tirrka", "Nokra", "Grunka", "Blortik", "Bubnel", "Trunbo",
            "Ziblik", "Kloben", "Vlimbi", "Chibli", "Mimsi", "Toblen", "Pallo", "Rugbit", "Gorba", "Dronli",
            "Booga", "Klinka", "Stribble", "Lumba", "Fobrin", "Muggo"], # Goblinoids, Mushroomfolks and similar
        "Celestial": [
            "Aelion", "Seraphía", "Luméthiel", "Vaënor", "Caelus", "Erión", "Thalëa", "Aurévan",
            "Ílthar", "Rhaëlos", "Vaelír", "Émthion", "Solvár", "Naëra", "Elúvien", "Tirál",
            "Orrën", "Laëric", "Vionára", "Caerûn", "Elyón", "Arvëa", "Thuríel", "Maëlith",
            "Oráien", "Liorën", "Sávir", "Eshál", "Núren", "Auvéris", "Rhéon", "Taliaën",
            "Velúr", "Eärion", "Islíth", "Anórien", "Caësha", "Rúthiel", "Elnár", "Aethíra",
            "Vaërith", "Solën", "Ilúvra", "Árieth", "Thavón", "Eonár", "Naëlir", "Vuréa",
            "Saéris", "Ilmáth", "Élaren", "Rhúvien", "Cálith", "Urëna", "Thalíon", "Eliára",
            "Aurën", "Rávenor", "Isóth", "Elnëa", "Vuráiel", "Laëris", "Itháel", "Súvra"],
        "Fiendish": [
            "Azrakul", "Vrethex", "Naazira", "Tzerrath", "Khaziel", "Uthraen", "Zarvok", "Maelgoth",
            "Xulneth", "Dravira", "Ozhrael", "Lethrix", "Kaavun", "Tzelek", "Ravhira", "Vorneth",
            "Grashael", "Izhraal", "Belvok", "Khezzar", "Thraxis", "Vaelra", "Nozriel", "Eshkar",
            "Vruzzeth", "Aazhoth", "Nirvul", "Khariel", "Zevalon", "Tzunra", "Morveth", "Ithral",
            "Zhalgor", "Ozrivak", "Kravael", "Rhezoth", "Draalith", "Velzikar", "Xanvoth", "Thraal",
            "Malzith", "Aevriss", "Zhuriel", "Kaelzoth", "Ravkul", "Vethra", "Tzelkor", "Uzhraen",
            "Nazhira", "Kholveth", "Vaerzul", "Drezakh", "Xulra", "Lazveth", "Throgar", "Mezzial",
            "Rhazun", "Azvra", "Khraleth", "Zorneth", "Vulzar", "Nirvak", "Zhalith", "Ithraen"],
        "Shadowy": [
            "Vareth", "Nýthra", "Sàvel", "Dravon", "Mòrwen", "Thalric", "Rhuven", "Esmorà",
            "Velraith", "Nyssra", "Thren", "Auvrik", "Serath", "Morvyn", "Ylra", "Zorathiel",
            "Ravèn", "Dusmir", "Vhaelor", "Lunthra", "Eldryn", "Shaviel", "Noctra", "Valenrith",
            "Cyrath", "Ulmira", "Thauven", "Irvath", "Rhosyn", "Marvèl", "Draenith", "Fynra",
            "Shùren", "Obryn", "Velmòr", "Isreth", "Graven", "Sàthiel", "Thynra", "Vorèl",
            "Umbriel", "Zirath", "Nolwen", "Drùvis", "Veshra", "Raèn", "Malthyr", "Othvel",
            "Serèn", "Nyris", "Valsha", "Thùriel", "Aresh", "Corvyn", "Sòlen", "Velisth",
            "Ravòra", "Dryneth", "Mùriel", "Ysrath", "Vorniel", "Thaesh", "Eshryn", "Mòrion"],
        "Marine": [
            "Neriel", "Coralyn", "Thalune", "Vareli", "Ondora", "Mareis", "Sevath", "Lunara",
            "Pelion", "Nimue", "Vaelus", "Orsha", "Kelaren", "Sirona", "Mithal", "Oceara",
            "Rilune", "Tavora", "Nalyn", "Sùvren", "Delora", "Aqualis", "Mereth", "Nèthir",
            "Thalira", "Corven", "Ulmar", "Vaylen", "Selura", "Orren", "Lumeris", "Nèira",
            "Marlith", "Eshara", "Koral", "Valune", "Therai", "Ondrel", "Marèn", "Sòlivan",
            "Pelura", "Aenor", "Tirasha", "Luvien", "Orralis", "Velmar", "Suviel", "Narion",
            "Thèlen", "Mareva", "Oshyn", "Selvra", "Dùmiel", "Kalora", "Nàlven", "Riveth",
            "Sirenna", "Morail", "Olivar", "Vaën", "Thèlune", "Muriel", "Loryn", "Nòvera",
            "Corvash", "Elarun", "Pelvra", "Othalen", "Sevrin", "Vaelith", "Thorian", "Luméra"]
    }

    # i'm wondering if i should add a separate generation for surnames...
    # surname_styles = {
    #     "Human": ["Blackwood", "Hartfield", "Kingsley", "Montclair", "Redford", "Stormridge", "Whitlock", "Fairborne", "Ashvale",
    #               "Thornhill", "Rossi", "Bianchi", "Strappato", "Raucci", "Baleani", "McDonald", "Whashington", "Belaire", "Cogno",
    #               "Shabani", "Serpi", "Caporali", "Andrei", "Folk", "Trembolin", "Piligrim", "Scotto", "Lock", "Done", "Milton",
    #               "Black", "Cicogna", "Efesti", "Zettori", "Marx", "Oppenheimer", "Smith", "McCollins", "Shade", "Boudelaire",
    #               "Portoland", "Big", "King", "Re", "Yemen", "Jonka", "De Felice", "D'Onofrio", "De Jesus", "D'Agnese", "E Diodati"],
    #     "Fairy": ["Moonshadow", "Starwhisper", "Silverleaf", "Dawntracker", "Windwalker", "Leafsong", "Nightbreeze", "Sunstrider", "Mistglen", "Starfall"],
    #     "Dwarvish": ["Ironfist", "Stonebeard", "Goldhammer", "Forgefire", "Deepdelve", "Rockshield", "Thunderaxe", "Hammerfall", "Flintfoot", "Anvilforge"],
    #     "Draconic": ["Flamescale", "Emberwing", "Nightfang", "Dragonheart", "Firebrand", "Stormclaw", "Skybreath", "Ironscale", "Ashdrake", "Brighttalon"],
    #     "Wildermagic": ["Bogfoot", "Mosswhistle", "Fungalroot", "Mudspinner", "Thornsnout", "Guttercap", "Tanglefoot", "Sporebloom", "Grimble", "Nettleback"], # Goblinoids, Mushroomfolks and similar
    #     "Celestial": ["Lightbringer", "Starfall", "Sunwarden", "Dawnshard", "Skyborne", "Moonveil", "Brightmantle", "Silverwing", "Radiantheart", "Cloudspire"],
    #     "Fiendish": ["Hellfire", "Dreadbane", "Nightflame", "Ashveil", "Shadowfang", "Bloodthorn", "Doomspire", "Flameheart", "Cinderclaw", "Darkscale"],
    #     "Shadowy": ["Darkwhisper", "Nightveil", "Shadowmoor", "Gloomspire", "Mistborn", "Silentfang", "Duskfall", "Blackveil", "Moonshade", "Ashgrove"],
    #     "Marine": ["Wavecrest", "Coralfin", "Tidewalker", "Stormsinger", "Deepcurrent", "Seaborn", "Saltwind", "Shellbreeze", "Moonwave", "Oceanveil"]
    # }

    transition_data_names = train_element_styles(name_styles)
    save_to_json(transition_data_names)
    print("JSON saved successfully!")
