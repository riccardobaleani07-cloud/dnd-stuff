#NPC generator, yay

#imports
import random
import json
from faker import Faker
import pandas as pd

#variables initializations
fake = Faker()


#classes
class NPC:
    def __init__(self, name, gender, race, subtype, language, occupation, age_category, age, alignment, partnership, personality_traits, offsprings, reputation, wealth, backstory_seed, social_level, backstory):

        self.name = name
        self.gender = gender
        self.race = race
        if subtype != None:
            self.subtype = subtype
        else:
            self.subtype = ""
        self.language = language
        self.age_category = age_category
        self.age = age
        self.occupation = occupation
        self.alignment = alignment
        self.partnership = partnership
        self.personality_traits = personality_traits
        self.offsprings = offsprings
        self.reputation = reputation
        self.wealth = wealth
        self.backstory_seed = backstory_seed
        self.social_level = social_level
        self.backstory = backstory

    def __str__(self):
        return (
            f"--- NPC Profile ---\n"
            f"Name and Surname: {self.name}\n"
            f"Gender: {self.gender}\n"
            f"Race and Eventual Subtype: {self.race} {self.subtype}\n"
            f"Language: {self.language}\n\n"
            f"Social Level: {self.social_level}\n"
            f"Occupation: {self.occupation}\n\n"
            f"Age: {self.age} ({self.age_category})\n"
            f"alignment: {self.alignment}\n"
            f"Partnership Status: {self.partnership}\n"
            f"Number of Descendants: {self.offsprings}\n\n"
            f"Personality Traits: {', '.join(self.personality_traits)}\n"
            f"Reputation: {self.reputation}\n"
            f"Wealth: {self.wealth}\n\n"
            f"Backstory Seed: {self.backstory_seed}\n"
            f"-----Backstory-----\n{self.backstory}\n"
            f"-------------------"
        )
    



class NPCGenerator:

    # I define class-level constants just before a function needs them
    # From this point on i handle the generation of stats tied to the roleplay

    # Those are needed for the backstory: oaths, fallen_cities, war_events and disasters are just lists, while the other ones contain the "building material"
    backstory_seeds = [
        "Lost heir", "Exiled noble", "Former soldier", "Wandering scholar", "Cursed individual",
        "Plague survivor", "Refugee from the North/South/East/West", "Escaped experiment", "Disgraced knight", "Amnesiac drifter",
        "Former slave", "Treasure hunter", "Fugitive from the law", "Dream-chaser", "Wandering artist",
        "Apostle of a Witch of Sin or Angel of Virtue", "Former pirate", "Marked by the gods", "Bearer of a forbidden gift",
        "Cursed bloodline", "Chosen vessel", "Oathbreaker", "Former apprentice", "Forgotten inventor",
        "Forbidden scholar", "Disillusioned hero", "Arcane researcher", "Street prophet", "Fallen priest/priestess",
        "Exiled seer", "Defector spy", "Witch-kin outcast", "Mercenary idealist", "Reluctant hero",
        "Traitor turned savior", "Doom-bound wanderer", "Revolution's spark",
        "Runaway noble child", "Monster in humanoid form", "Survivor of a fallen city", "Bearer of ancestral guilt",
        "Last of their order", "Haunted war veteran", "Reformed cultist", "Seeker of the First Flame"]
    backstory_flavour = {
        "Lost heir": "Social Class Origin",
        "Exiled noble": "Social Class Origin",
        "Disgraced knight": "Social Class Origin",
        "Traitor turned savior": "Social Class Origin",
        "Runaway noble child": "Social Class Origin",
        "Bearer of ancestral guilt": "Social Class Origin",
        "Fallen priest/priestess": "Social Class Origin",
        "Oathbreaker": "Social Class Origin",
        "Former soldier": "Conflict Survivor",
        "Mercenary idealist": "Conflict Survivor",
        "Reluctant hero": "Conflict Survivor",
        "Doom-bound wanderer": "Conflict Survivor",
        "Revolution's spark": "Conflict Survivor",
        "Survivor of a fallen city": "Conflict Survivor",
        "Haunted war veteran": "Conflict Survivor",
        "Wandering scholar": "Academic Origin",
        "Former apprentice": "Academic Origin",
        "Forgotten inventor": "Academic Origin",
        "Forbidden scholar": "Academic Origin",
        "Arcane researcher": "Academic Origin",
        "Cursed individual": "Cursed Origin",
        "Marked by the gods": "Cursed Origin",
        "Bearer of a forbidden gift": "Cursed Origin",
        "Cursed bloodline": "Cursed Origin",
        "Chosen vessel": "Cursed Origin",
        "Apostle of a Witch of Sin or Angel of Virtue": "Cursed Origin",
        "Seeker of the First Flame": "Cursed Origin",
        "Plague survivor": "Outcast/Survivor",
        "Refugee from the North/South/East/West": "Outcast/Survivor",
        "Escaped experiment": "Outcast/Survivor",
        "Exiled seer": "Outcast/Survivor",
        "Defector spy": "Outcast/Survivor",
        "Witch-kin outcast": "Outcast/Survivor",
        "Monster in humanoid form": "Outcast/Survivor",
        "Last of their order": "Outcast/Survivor",
        "Former slave": "Outcast/Survivor",
        "Fugitive from the law": "Outcast/Survivor",
        "Amnesiac drifter": "Wanderer Origin",
        "Treasure hunter": "Wanderer Origin",
        "Dream-chaser": "Wanderer Origin",
        "Wandering artist": "Wanderer Origin",
        "Former pirate": "Wanderer Origin",
        "Disillusioned hero": "Wanderer Origin",
        "Street prophet": "Wanderer Origin",
        "Reformed cultist": "Wanderer Origin",
    }
    bc_flavour_to_templates = {
        "Social Class Origin": [
            "{name}, a {age_category} {race}, was once {origin}. After {catalyst}, they abandoned/lost all ties to their family name and/or social order. Now they {drive}.",
            "Born among silk and betrayal, {name}—a {age_category} {race}—was {origin}. One day their fate turned: {catalyst}. They now {drive}."],
        "Conflict Survivor": [
            "{name}, a {age_category} {race}, served once as {origin}. When {catalyst}, something within them broke. Now they {drive}, haunted by echoes of an old fight.",
            "Forged in the fires of conflict, {name} was {origin}. Ever since {catalyst}, they {drive}, though the old battlefield never truly leaves them."],
        "Academic Origin": [
            "Once {origin}, {name}—a {age_category} {race}—dedicated their life to understanding the unknown. After {catalyst}, their research took a darker path. Now they {drive}.",
            "{name} was once {origin}, until {catalyst}. Since then, the pursuit of forbidden truths consumes them: they {drive}, no matter the cost."],
        "Cursed Origin": [
            "{name}, a {age_category} {race}, carries an unspeakable doom: when {catalyst}, their mortal life was forever changed and they become {origin}. Now they {drive}, bound by powers beyond their control.",
            "Once ordinary, {name} became {origin} after {catalyst}. Now they {drive}, their fate woven into the will of ancient forces."],
        "Outcast/Survivor": [
            "{name}, a {age_category} {race}, was {origin}. They endured a lot: {catalyst}, surviving where countless others would have fallen. Now they {drive}, carrying the weight of their past.",
            "Cast away and forgotten, {name}—a {age_category} {race}—was {origin}. After {catalyst}, they {drive}, driven by stubborn will and the memory of what was endured."],
        "Wanderer Origin": [
            "{name}, a {age_category} {race}, has always been {origin}. When {catalyst}, they left everything behind. Now they {drive}, chasing whispers of purpose on the open road.",
            "The world never seemed enough for {name}, the {age_category} {race} who was once {origin}. After {catalyst}, they {drive}, guided by dreams brighter than reason."],
    }
    disasters = [
        "the Great Flood",
        "the Shattering of the Sky",
        "a wildfire that devoured three kingdoms",
        "the Sundering Storm",
        "the Red Plague",
        "a volcanic winter",
        "the Drowning of the West",
        "the Blight of Silent Fields",
        "the Night of Falling Stars",
        "the Collapse of the Silver Spire",
        "the Famine Years",
        "a cursed drought that lasted a generation",
        "the Tides of Ash",
        "the Great Quake",
        "a wandering plague",
        "the Storm of Glass",
        "the Eclipse that lasted seven days",
        "the Burning of the World Tree",
        "the Whispering Pestilence",
        "the Day the Sun Wept"
    ]
    oaths = [
        "an oath",
        "the Oath of Vengeance",
        "the Blood Oath of Kin",
        "the Silent Oath",
        "the Oath of the Bound Flame",
        "a sacred vow",
        "the Oath of Iron and Ash",
        "the Oath of the Last Watch",
        "the Wanderer’s Oath",
        "a deathbed promise",
        "the Oath of Redemption",
        "the Covenant of Shadows",
        "the Oath of the Fallen Banner",
        "the Pact of Still Waters",
        "an oath sworn under moonlight",
        "the Oath of Broken Blades",
        "the Oath of the Twin Suns",
        "a vow of silence",
        "the Oath of the Crimson Dawn",
        "the Eternal Vow"
    ]
    fallen_cities = [
        "a fallen city",
        "the fallen city of Atlantis",
        "the fallen city of Pequalora",
        "the ruins of Keth’Ra",
        "the fallen city of Mirehaven",
        "the drowned city of Uldan",
        "the lost city of Vael-Tir",
        "the fallen city of Korintha",
        "the shattered city of Erelith",
        "the cursed city of Damaris",
        "the fallen city of Avenreach",
        "the buried city of Tor-Mira",
        "the fallen city of Calithorn",
        "the ghost city of Nel’Thar",
        "the fallen city of Rivenmark",
        "the sunken city of Halor",
        "the fallen city of Drelen",
        "the silent city beneath the sands",
        "the fallen city of Yorelan",
        "the forgotten city of Lysmere"
    ]
    war_event = [
        "a war",
        "a siege",
        "a rebellion",
        "the Battle of Red Fields",
        "the capture of Pequalora",
        "the revolt of the Fishermen",
        "the War of Broken Crowns",
        "the Siege of Greywatch",
        "the fall of the Iron Bastion",
        "the rebellion of the Five Lords",
        "the Northern Crusade",
        "the War of the Shattered Banner",
        "the March of Ash and Snow",
        "the burning of Avenreach",
        "the uprising of the Bound",
        "the War of Two Dawns",
        "the last stand at Frostgate",
        "the conquest of the Drowned Coast",
        "the revolt of the Harvest Blades",
        "the Siege of Emberhold"
    ]
    seed_global_data = {
        "Lost heir": {
            "origin": [
                "the rightful heir to a once-mighty dynasty",
                "a scion of an ancient bloodline steeped in glory"
            ],
            "catalyst": [
                "their house fell to betrayal and blades in the darkness of a foggy night",
                "their claim was stolen by kin with sharper smiles"
            ],
            "drive": [
                "seek to reclaim their birthright from the shadows",
                "wander in secret, watching those who sit on their throne, resigned to defeat"
            ],
        },
        "Exiled noble": {
            "origin": [
                "a noble of fine title and finer arrogance",
                "an esteemed courtier in lands now lost to them"
            ],
            "catalyst": [
                "they crossed the wrong allies and were cast into the wilds",
                "their name was struck from every record by decree of the crown"
            ],
            "drive": [
                "dream of redemption through deeds, not lineage",
                "plot a quiet return to the court that cast them out"
            ],
        },
        "Disgraced knight": {
            "origin": [
                "a sworn sword of the old code",
                "a bannered champion hailed for honor and valor"
            ],
            "catalyst": [
                "they broke their {oath} in the hour of truth",
                "their blade was turned against their own will and command"
            ],
            "drive": [
                "desperately tries to atone, but ends up committing immoral acts",
                "refuse to wear another crest until honor is earned again"
            ],
        },
        "Traitor turned savior": {
            "origin": [
                "a loyal retainer who rejected their own cause",
                "an agent who played both sides of a dying empire during {a_war_event}"
            ],
            "catalyst": [
                "their betrayal saved more lives than loyalty ever could",
                "the truth was revealed, they betrayed everyone seeking personal gain"
            ],
            "drive": [
                "walk the fine line between guilt and redemption",
                "fight for the peace they once endangered"
            ],
        },
        "Runaway noble child": {
            "origin": [
                "a sheltered heir born into endless expectation",
                "the youngest child of a house obsessed with prestige"
            ],
            "catalyst": [
                "they disappeared under the moonlight, kidnapped and sold by criminals",
                "a scandal forced them to vanish before their coming-of-age"
            ],
            "drive": [
                "search for their lost titles and family",
                "hide their lineage beneath common clothes"
            ],
        },
        "Bearer of ancestral guilt": {
            "origin": [
                "the descendant of a family cursed by ancient crimes",
                "an inheritor of sins no longer remembered by the world"
            ],
            "catalyst": [
                "omens began to follow them wherever they went, affecting everyone around them",
                "they uncovered the truth of their family's dark legacy"
            ],
            "drive": [
                "seek to end the guilt that haunts their bloodline",
                "bear their family's shame in silence, hoping to balance the scales"
            ],
        },
        "Fallen priest/priestess": {
            "origin": [
                "a devoted servant of a radiant temple",
                "a revered priest/priestess whose voice carried the word of gods"
            ],
            "catalyst": [
                "they witnessed a miracle turn to blasphemy",
                "their faith crumbled when their god refused to answer their prayers"
            ],
            "drive": [
                "wander seeking divine truth beyond doctrine and religious orders",
                "preach a new gospel born of doubt and loss, built form the ashes of a once-strong faith"
            ],
        },
        "Oathbreaker": {
            "origin": [
                "a bound servant of sacred vows",
                "a sworn guardian whose {oath} defined them"
            ],
            "catalyst": [
                "they shattered their own word to save another's life from {a_disaster}",
                "their promise was broken when loyalty clashed with conscience"
            ],
            "drive": [
                "carry the weight of their broken vow like a spiked crown around their forhead",
                "roam seeking a cause worthy of new promises, in hope to heal from their scars"
            ],
        },

        "Former soldier": {
            "origin": [
                "a disciplined infantry fighter in a crumbling empire",
                "a loyal guardsman sworn to defend their homeland's border"
            ],
            "catalyst": [
                "their comrades fell in a hopeless siege",
                "they witnessed the empire burn from within"
            ],
            "drive": [
                "seek a peaceful life beyond the sword",
                "honor an {oath} sworn to the dead"
            ],
        },
        "Mercenary idealist": {
            "origin": [
                "a sword-for-hire chasing glory and fame across foreign lands",
                "an adventurer who believed coin could buy justice"
            ],
            "catalyst": [
                "they got obligated to submit a contract that went against their conscience",
                "they broke their vow to follow a personal moral code"
            ],
            "drive": [
                "fight only for causes worth dying for, sometimes careless of the low payments",
                "want to reclaim the honor they sold for gold by helping unfortunate people"
            ],
        },
        "Reluctant hero": {
            "origin": [
                "a quiet villager who never sought greatness",
                "a scholar recruited unwillingly into war"
            ],
            "catalyst": [
                "they saved lives from {a_disaster} while dooming others",
                "circumstance forced them to kill ruthlessly to survive"
            ],
            "drive": [
                "atone for what they've done even if they were considered an hero",
                "avoid fame but uphold a meaningful {oath}"
            ],
        },
        "Doom-bound wanderer": {
            "origin": [
                "a conscript who escaped the misery following {a_war_event}",
                "a deserter marked by a cursed victory"
            ],
            "catalyst": [
                "they were the sole survivor of a doomed regiment",
                "they discovered the war itself was a lie"
            ],
            "drive": [
                "walk the land seeking redemption before fate claims them",
                "wander in search of meaning before the curse consumes them"
            ],
        },
        "Revolution's spark": {
            "origin": [
                "a rebel leader who rose from the ashes of oppression",
                "a commoner turned insurgent against tyranny"
            ],
            "catalyst": [
                "their uprising succeeded but at the cost of too many lives",
                "their revolution was crushed under a rain of fire"
            ],
            "drive": [
                "are rebuilding what was lost and keep the dream alive",
                "try to protect others from repeating their same errors"
            ],
        },
        "Survivor of a fallen city": {
            "origin": [
                "a citizen of {fallen_city}, once a jewel of the continent",
                "a watchman who saw their city crumble to ruin"
            ],
            "catalyst": [
                "they watched their home devoured by flames and monsters",
                "their loved ones died horrendously in the chaos of {a_war_event}"
            ],
            "drive": [
                "are searching others who escaped the fall",
                "uncover who or what truly caused that disaster"
            ],
        },
        "Haunted war veteran": {
            "origin": [
                "a battlefield commander whose victories were celebrated for years",
                "a champion who led too many to their deaths"
            ],
            "catalyst": [
                "they fought in {a_war_event} that doomed their friends",
                "they saw hunting unnatural visions rise from the corpses"
            ],
            "drive": [
                "seek forgiveness in impossible deeds, trying to wash their unbareable guilt",
                "fight the nightmares that still stalk their dreams and stain their mind"
            ],
        },

        "Wandering scholar": {
            "origin": [
                "a nomadic sage who studied in every library from coast to coast",
                "a self-taught wanderer collecting scraps of lost spells"
            ],
            "catalyst": [
                "they uncovered a manuscript no one else could read or decypher, helding ancient visions",
                "a close friend vanished after entrusting them with a sealed tome, an encryption of new discoveries"
            ],
            "drive": [
                "seek the final piece of a theory that could reshape magic itself",
                "want to retrace the path of knowledge lost after {fallen_city}, a place of forgotten wisdom that could lead to priceless truths"
            ],
        },
        "Former apprentice": {
            "origin": [
                "an eager pupil under a master of the arcane arts",
                "a devoted student in the service of a renowned magus"
            ],
            "catalyst": [
                "their master perished in an experiment gone wrong",
                "they betrayed their teacher to claim a secret spell"
            ],
            "drive": [
                "want to prove they've surpassed their master's legacy",
                "want to rebuild a forbidden ritual to rebuild the friendship that was lost, even if it's an insane attempt"
            ],
        },
        "Forgotten inventor": {
            "origin": [
                "a visionary tinkerer obsessed with merging science and sorcery, amused by many for their genius",
                "an engineer whose creations once amazed courts and guilds alike"
            ],
            "catalyst": [
                "their inventions were seized and their name erased from history",
                "a failed machine opened a rift that consumed their workshop and scarring them for life"
            ],
            "drive": [
                "seek to recreate their magnum opus before memory itself betrays them",
                "aim to invent something powerful enough to reclaim their lost reputation"
            ],
        },
        "Forbidden scholar": {
            "origin": [
                "a university researcher specializing in proscribed magical theory",
                "a philosopher of the unseen laws that bind the soul"
            ],
            "catalyst": [
                "they read a book written in their own hand centuries ago",
                "they uncovered evidence that the gods themselves can be studied"
            ],
            "drive": [
                "will spend their life to decipher the last untranslatable sigil, a truth that can't be unfolded",
                "bear to uncover truths that even the Angels fear to name"
            ],
        },
        "Arcane researcher": {
            "origin": [
                "a meticulous scientist exploring the boundaries of mana flow",
                "a scholar at a famous sorcery university"
            ],
            "catalyst": [
                "they discovered a resonance pattern linking magic to emotion, through an experiment that accidentally created a cursed chimera",
                "their experiment bled energy from another plane, scarring them for life and opening a distructive portal in their laboratory"
            ],
            "drive": [
                "have to study and contain the anomaly they unleashed",
                "seek to map the hidden architecture the new magical discovery"
            ],
        },

        "Cursed individual": {
            "origin": [
                "the bearer of a curse that feeds on their own soul",
                "bound to a parasitic spirit whispering in their mind"
            ],
            "catalyst": [
                "they angered a forgotten deity beneath {fallen_city}",
                "a dying witch-kin granted them her final breath and her curse"
            ],
            "drive": [
                "seek a cure before the curse consumes their last memories",
                "turn their curse into a weapon against those who wronged them"
            ],
        },
        "Marked by the gods": {
            "origin": [
                "a mortal chosen and branded by celestial powers",
                "marked at birth by a symbol that glows beneath their skin"
            ],
            "catalyst": [
                "the heavens split open and a voice spoke their true name",
                "they survived {a_disaster} (no mortal could have endured it without facing death or madness)"
            ],
            "drive": [
                "fulfil the divine command that haunts their dreams",
                "plot to defy the gods who claimed ownership of their fate"
            ],
        },
        "Bearer of a forbidden gift": {
            "origin": [
                "a vessel of arcane energy that mortals were never meant to wield",
                "a host for a slumbering entity older than the stars"
            ],
            "catalyst": [
                "their body became the key to an ancient seal",
                "they accepted a power offered by something that was not human"
            ],
            "drive": [
                "learn to master the gift before it masters them",
                "use their burden to uncover the truth behind its creation"
            ],
        },
        "Cursed bloodline": {
            "origin": [
                "the last heir of a family whose name is spoken only in whispers",
                "born into a lineage bound to an ancient punishment"
            ],
            "catalyst": [
                "their ancestor broke an {oath} sworn to a divine being",
                "they witnessed the curse pass from parent to child before their eyes"
            ],
            "drive": [
                "seek redemption for the sins of their ancestors",
                "want to break the cycle of doom even if it will costs their life"
            ],
        },
        "Chosen vessel": {
            "origin": [
                "the living container of a god's fragmented will",
                "a mortal shell housing a divine spark"
            ],
            "catalyst": [
                "a ritual meant for another went terribly right",
                "they were chosen as host during a celestial convergence"
            ],
            "drive": [
                "resist the will of the being inside them",
                "carry out the god's purpose before their body collapses"
            ],
        },
        "Apostle of a Witch of Sin or Angel of Virtue": {
            "origin": [
                "a mortal handpicked by an Angel of Virtue to be their new apostle",
                "a chosen servant of a Witch of Sin, receptacle for enormous power"
            ],
            "catalyst": [
                "they were marked during a vision of fire and light",
                "a dying deity's will fused with their own"
            ],
            "drive": [
                "spread the will of their patron across mortal lands",
                "ignore the duty of being an Apostle, waiting for a final judgement of death"
            ],
        },
        "Seeker of the First Flame": {
            "origin": [
                "a pilgrim drawn to the myth of the First Flame that birthed all magic",
                "the last devotee of an order sworn to rekindle creation itself"
            ],
            "catalyst": [
                "they witnessed {a_disaster} that dimmed the world's last embers in a vision",
                "a vision showed them the dying flame beneath the earth"
            ],
            "drive": [
                "seek the First Flame and restore the age of light",
                "protect the secret of the First Flame from those who would extinguish it"
            ],
        },


        "Plague survivor": {
            "origin": [
                "one of the few who endured a wasting sickness that erased entire towns",
                "scarred by the fever that turned neighbors into corpses overnight"
            ],
            "catalyst": [
                "they watched their family perish while they alone drew breath",
                "the plague swept through their village, leaving only silence and smoke"
            ],
            "drive": [
                "search for the cure that could prevent such horror again",
                "carry the memory of the dead, helping people to heal from similar sicknesses"
            ],
        },
        "Refugee from the North/South/East/West": {
            "origin": [
                "a wanderer driven from their homeland by war and ruin",
                "a displaced soul who lost their nation to the flames of {a_war_event}"
            ],
            "catalyst": [
                "their homeland was swallowed by invasion and fire",
                "they fled across the wastes as their city crumbled behind them"
            ],
            "drive": [
                "seek a new home that will not reject them for their accent or scars",
                "are rebuilding what was lost, stone by stone, dream by dream"
            ],
        },
        "Escaped experiment": {
            "origin": [
                "a subject in a forbidden experiment meant to reshape life itself",
                "a creation built from pain, molded by alchemic cruelty"
            ],
            "catalyst": [
                "they broke free from the laboratory that held them in chains",
                "they escaped the laboratory killing and consuming their creator"
            ],
            "drive": [
                "wander around, seeking who they were before the experiment began",
                "destroy, in madness, every trace and everything that resembles something of the project that made them what they are"
            ],
        },
        "Exiled seer": {
            "origin": [
                "a prophet whose visions revealed truths too dangerous to be spoken",
                "an oracle once revered, now feared for foretelling a king's doom"
            ],
            "catalyst": [
                "their prophecy came true, and they were cast out by fearful people",
                "they revealed an {oath} broken by the powerful and paid the price"
            ],
            "drive": [
                "seek a place where their sight will not bring death to those around them",
                "bear the final vision that will explain the curse of their foresight"
            ],
        },
        "Defector spy": {
            "origin": [
                "a spy who once served a nation now sworn against them",
                "a master of masks who betrayed their own for a greater cause"
            ],
            "catalyst": [
                "they blown their cover after a failed mission, they got imprisoned and tortured",
                "they saw the truth of the war they once fought and could serve no more and betrayed everyone"
            ],
            "drive": [
                "are outrunning both their old masters and the guilt that haunts them",
                "want to please their wounds by ensuring no one else does their same error"
            ],
        },
        "Witch-kin outcast": {
            "origin": [
                "descendant from those who once served primordial shadowy creatures",
                "born with the taint of forbidden power running through their veins"
            ],
            "catalyst": [
                "they uncountiously manifested their hidden magic in front of terrified townsfolk, they got imprisoned and then escaped",
                "they refused to renounce their bloodline when the purge began"
            ],
            "drive": [
                "want to prove everyone they knew that their heritage does not define their soul",
                "seek others like them, to build a place where Witch-kin can live free"
            ],
        },
        "Monster in humanoid form": {
            "origin": [
                "a creature cursed to wear the guise of a mortal",
                "a beast who learned to mimic humanity's fragile kindness and body"
            ],
            "catalyst": [
                "they were discovered by those they once called friends, enduring shame and hate",
                "they manifested their monstrous nature during a night of blood and fear, exposing their nature to the hate of townfolk"
            ],
            "drive": [
                "cling to the last shreds of humanity left within them, to not show again their hidden side",
                "bear to prove that real monsters are made by cruelty, not by birth"
            ],
        },
        "Last of their order": {
            "origin": [
                "the final survivor of an ancient brotherhood devoted to peace",
                "the last disciple of a sacred order lost to time and flame"
            ],
            "catalyst": [
                "their temple was destroyed during {a_disaster}; they went through loosing everything they knew",
                "they awoke amidst the ashes of their fallen comrades, during {a_war_event}"
            ],
            "drive": [
                "aims to rebuild their order's teachings in secret",
                "guard the final relic of their creed until death takes them"
            ],
        },
        "Former slave": {
            "origin": [
                "a soul once bound in chains, treated as property by the cruel",
                "a worker born in bondage beneath a tyrant's shadow"
            ],
            "catalyst": [
                "they seized their freedom during a revolt drenched in fire and blood",
                "their master fell to ruin; they were left to forge a life anew from nothing"
            ],
            "drive": [
                "dedicate themself to free others from the chains they once bore",
                "swore to never again bow to any who would call themselves master and won't grant human condition to their servants"
            ],
        },
        "Fugitive from the law": {
            "origin": [
                "a wanderer pursued for crimes both real and imagined",
                "a rogue who fled justice after being framed by powerful enemies"
            ],
            "catalyst": [
                "a betrayal turned allies into hunters; they were obligated to hide, on the verge of death",
                "a deal gone wrong exposed them to the watchful eyes of the crown leading to a bloody hunt, but they vanished into the shadows"
            ],
            "drive": [
                "work to clear their name before time or bounty hunters catch them",
                "live freely, no matter the price of defiance, far from the places that haunted them"
            ],
        },

        "Amnesiac drifter": {
            "origin": [
                "a nameless soul with no memory of home or kin",
                "a traveler who woke one day with their past erased by strange magic"
            ],
            "catalyst": [
                "visions of a life that may never have been began haunting their dreams",
                "they found a token engraved with a name they didn't recognize"
            ],
            "drive": [
                "wander from town to town, seeking fragments of their lost self",
                "pursue the echo of a forgotten identity"
            ]
        },
        "Treasure hunter": {
            "origin": [
                "a restless adventurer obsessed with legends of hidden relics",
                "a scavenger raised among tomb raiders and map thieves"
            ],
            "catalyst": [
                "a cursed map gave them visions of past horrors",
                "they stumbled on a half-truth whispered by a dying explorer"
            ],
            "drive": [
                "chase every rumor of ancient gold and forbidden ruins to unfold the truth",
                "seek the treasure said to reveal one's true past"
            ]
        },
        "Dream-chaser": {
            "origin": [
                "an idealist who believed dreams could reshape reality",
                "a visionary whose head was forever lost in stars and stories"
            ],
            "catalyst": [
                "they glimpsed something divine in their sleep",
                "their hometown mocked their visions until they fled"
            ],
            "drive": [
                "journey toward the horizon they once saw in a dream",
                "work to prove that the impossible dream can, in fact, be reached"
            ]
        },
        "Wandering artist": {
            "origin": [
                "a poet who worked on commission in a workshop",
                "a painter once bound to a court that demanded beauty without meaning"
            ],
            "catalyst": [
                "their greatest work was destroyed before their eyes",
                "they realized art confined to walls and by people was not alive"
            ],
            "drive": [
                "travel the world capturing fleeting beauty",
                "wander for the inspiration to create something that outlives the artist"
            ]
        },
        "Former pirate": {
            "origin": [
                "a sailor who once plundered trade routes under a black flag",
                "a corsair whose ship ruled the western seas"
            ],
            "catalyst": [
                "their crew was scattered by storm and betrayal",
                "they watched their captain drown clutching cursed gold"
            ],
            "drive": [
                "seek redemption for their past crimes on calmer tides and an honest life",
                "sail again in search of true freedom, not fortune"
            ]
        },
        "Disillusioned hero": {
            "origin": [
                "a champion once praised in songs and lies",
                "a soldier, an hero who fought for a cause that rotted from within"
            ],
            "catalyst": [
                "they saw their comrades slaughter innocents in the name of peace",
                "their victory turned to ash when the truth of their patron was revealed"
            ],
            "drive": [
                "wander seeking a cause worth believing in, knowing well that there is none",
                "wander without a reason or meaning, seeking only the momentary adrenaline of cursed actions"
            ]
        },
        "Street prophet": {
            "origin": [
                "a beggar who heard divine whispers in gutter water",
                "a wanderer who claimed to see omens in every shadow"
            ],
            "catalyst": [
                "a voice from the void told them to speak or be forgotten",
                "they survived a fever that burned away all doubt"
            ],
            "drive": [
                "preach strange truths to anyone who will listen",
                "follow the cryptic visions toward an unknown salvation"
            ]
        },
        "Reformed cultist": {
            "origin": [
                "a zealot once devoted to an unspeakable god",
                "a child raised in candlelight and blood rites"
            ],
            "catalyst": [
                "they witnessed the false divinity consume their brethren",
                "Their faith wavered when they saw actions carried out even if condemned by their god"
            ],
            "drive": [
                "seek penance by fighting what their cult began",
                "walk the land warning others of blind devotion"
            ]
        }
    }

    def generate_backstory(self, seed, name, age_category, race):
        flavour = self.backstory_flavour.get(seed)
        if flavour is None:
            raise ValueError(f"No backstory flavour found for seed '{seed}'")

        templates = self.bc_flavour_to_templates.get(flavour)
        if not templates:
            raise ValueError(f"No templates found for backstory flavour '{flavour}'")
        template = random.choice(templates)

        seed_data = self.seed_global_data.get(seed)
        if seed_data is None:
            raise ValueError(f"No origin data found for backstory seed '{seed}'")

        origin = random.choice(seed_data.get("origin", ["an unknown past"]))
        catalyst = random.choice(seed_data.get("catalyst", ["a mysterious event"]))
        drive = random.choice(seed_data.get("drive", ["continue their journey"]))

        story = template.format(
            name=name,
            age_category=age_category,
            race=race,
            origin=origin,
            catalyst=catalyst,
            drive=drive
        )

        # Handle the optional placeholders
        if "{oath}" in story:
            story = story.replace("{oath}", random.choice(self.oaths))
        if "{fallen_city}" in story:
            story = story.replace("{fallen_city}", random.choice(self.fallen_cities))
        if "{war_event}" in story:
            story = story.replace("{war_event}", random.choice(self.war_event))
        if "{disaster}" in story:
            story = story.replace("{disaster}", random.choice(self.disasters))

        return story.strip()

    personality_traits_count = 3

    # Map
    races = [
        ("Polar Human", 0.0157),
        ("Quarryan Human", 0.0315),
        ("South Herian Human", 0.0472),     
        ("North Herian Human", 0.0472),     
        ("Plains Dorojan Human", 0.0629),   
        ("Mountains Dorojan Human", 0.0393),
        ("Common Elf", 0.0315),
        ("Dwarf", 0.0708),
        ("Dragonborn", 0.0787),
        ("Beastfolk", 0.0787),
        ("Gnome", 0.0472),
        ("Ogre", 0.0079),
        ("Half-Elf", 0.0551),
        ("Lost Goblin", 0.0016),
        ("Dark Elf", 0.0236),
        ("Aarakocra", 0.0024),
        ("Tabaxi", 0.0110),
        ("Kenku", 0.0110),
        ("Goliath", 0.0003),
        ("Celestial", 0.0002),
        ("Half-Ogre", 0.0157),
        ("Pixie", 0.0031),
        ("Turtoid", 0.0236),
        ("Triton", 0.0110),
        ("Mermaid", 0.0016),
        ("Half-Dragon", 0.0079),
        ("Insectoid", 0.0011),
        ("Lycantropus", 0.0006),
        ("Grung", 0.0008),
        ("Kling", 0.0005),
        ("Fairy", 0.0024),
        ("Satyr", 0.0005),
        ("Halfling", 0.0110),
        ("Orc", 0.0016),
        ("Tiefling", 0.0629),
        ("Yuan-Ti", 0.0031),
        ("Kobold", 0.0006),
        ("Lizardfolk", 0.0011),
        ("Aasimar", 0.0003),
        ("Firbolg", 0.0006),
        ("Bugbear", 0.0003),
        ("Hobgoblin", 0.0016),
        ("Sentient Undead", 0.0016),
        ("Moonling", 0.0079),
        ("Starborn", 0.0002),
        ("Voidling", 0.0016),
        ("Firefly", 0.0009),
        ("Shadowkin", 0.0008),
        ("Crystalborn", 0.0006),
        ("Deep-Elf", 0.0031),
        ("Wood Elf", 0.0126),
        ("Mushroomfolk", 0.0063),
        ("Sentient Construct", 0.0008),
        ("Elementalfolk", 0.0157),
        ("Plantfolk", 0.0024),
        ("True Dragon", 0.0002),
        ("Giant", 0.0002),
        ("Demon", 0.0002),
        ("Angel", 0.0002),
        ("Plasmoid", 0.0006),
        ("Demonoid", 0.0047),
        ("Spirit", 0.0013),
        ("Sylph", 0.0024),
        ("Salamanderman", 0.0041),
        ("Oni", 0.0136),
        ("Kijin", 0.0024),
        ("Majin", 0.0002),
        ("Strix", 0.0002),
        ("Changeling", 0.0016),
        ("Dryad", 0.0016),
        ("Nymph", 0.0013),
        ("Lost Sea Goblin", 0.0008),
        ("Gooba", 0.0005),
        ("True Vampire", 0.0002),
        ("Pale Knight", 0.0063),
        ("Lopunnie", 0.0325),
        ("Nightmare", 0.0002),
        ("Wisp", 0.0002),
        ("Moonskin Elf", 0.0246),
        ("Spectre", 0.0003),
        ("Banshee", 0.0002),
        ("Wolfang", 0.0031),
        ("Foxling", 0.0024),
        ("Common Birdling", 0.0071),
        ("Hybrid", 0.0036),
        ("Other", 0.0126)
        ]

    # Methods to generate specific attributes
    def choose_social_level(self, social_levels):
        names = [s[0] for s in social_levels]
        weights = [s[1] for s in social_levels]
        # Normalize weights to sum to 1
        total = sum(weights)
        weights = [w/total for w in weights]
        return random.choices(names, weights=weights, k=1)[0]
        
    def choose_race(self, races):
        names = [r[0] for r in races]
        weights = [r[1] for r in races]
        # Normalize weights to sum to 1
        total = sum(weights)
        weights = [w/total for w in weights]
        return random.choices(names, weights=weights, k=1)[0]
    
    beastfolk_subtypes = [("Beebesner", 0.15),
                          ("Dawg", 0.15),
                          ("Crimson Devil", 0.15),
                          ("Light Blue Devils", 0.1),
                          ("Jaguarfolk", 0.1),
                          ("Onicronimb", 0.1),
                          ("Octolen", 0.5),
                          ("Browish", 0.1),
                          ("Skullywag", 0.05),
                          ("Other", 0.05)]
    insectoid_subtypes = [("Flying Mantis", 0.2),
                          ("Hornet", 0.2),
                          ("Bumblebee", 0.1),
                          ("Fly", 0.2),
                          ("Cockroacher", 0.08),
                          ("Antsyote", 0.1),
                          ("Ladybudger", 0.05),
                          ("Mothyel", 0.05),
                          ("Other", 0.02)]
    elementalfolk_subtypes = [("Fire", 0.1),
                              ("Water", 0.1),
                              ("Earth", 0.1),
                              ("Air", 0.1),
                              ("Mud", 0.1),
                              ("Lava", 0.1),
                              ("Ice", 0.1),
                              ("Smoke", 0.1),
                              ("Steam", 0.1),
                              ("Dust", 0.1)]
    demonoid_subtypes = [("Cerberian", 0.35),
                         ("Blood Beat", 0.25),
                         ("Wither", 0.4)]
    sentient_undead_subtypes = [("Zombie", 0.2),
                                ("Skeleton", 0.35),
                                ("Ghost", 0.45)]
    celestial_subtypes = [("Shell", 0.25),
                          ("Lush", 0.4),
                          ("Grace", 0.35)]
    available_subtypes = [("Insectoid", insectoid_subtypes),
                          ("Beastfolk", beastfolk_subtypes),
                          ("Elementalfolk", elementalfolk_subtypes),
                          ("Demonoid", demonoid_subtypes),
                          ("Sentient Undead", sentient_undead_subtypes),
                          ("Celestial", celestial_subtypes)]

    def conditional_choose_subtype (self, available_subtypes, race):
        # Chooses a subtype if applicable
        for ar in available_subtypes:
            if ar[0] == race:
                names = [sr[0] for sr in ar[1]]
                weights = [sr[1] for sr in ar[1]]
                # Normalize weights to sum to 1
                total = sum(weights)
                weights = [w/total for w in weights]
                return random.choices(names, weights=weights, k=1)[0]
            return None
        

    genders = ["Male", "Female", "Lost", "Androgine"]

    def choose_gender(self, genders, race):
        # Chooses a gender, crafting a pool based on race
        # Default gender pool and weights
        # The default pool is used as a baseline: rare genders are added, and default genders are removed if necessary
        default_pool = genders
        default_weights = [10000, 10000, 1, 5] # order:Male, Female, Lost, Androgine
        # weights do not need to sum to 1; random.choices normalizes them
        
        # Rare genders mapped to applicable species (placeholder example)
        # Map
        species_gender_map = {
            # Genders that are in the default pool (adding a race here removes that gender from the default pool)
            "Male": ["Nymph", "Dryad", "Plasmoid", "Shadowkin", "Voidling", "Starborn", "Pixie", "Mermaid", "Lycantropus"],
            "Female": ["Strix", "Nymph", "Dryad", "Plasmoid", "True Dragon", "Mushroomfolk", "Shadowkin", "Voidling","Starborn", "Firefly", "Pixie", "Mermaid", "Lycantropus", "Lost Goblin", "Lost Sea Goblin", "Hobgoblin"],
            "Androgine": ["Strix","True Vampire", "Dryad", "Plasmoid", "Shadowkin", "Voidling", "Aarakocra", "Lizardfolk", "Starborn", "Turtoid","Triton","Mermaid", "Lycantropus", "Grung", "Kling", "Fairy", "Satyr", "Lost Goblin", "Lost Sea Goblin", "Hobgoblin"],
            "Lost": ["True Vampire", "Nymph", "Plasmoid", "Celestial"],
            # Genders that are not in the default pool (adding a race here adds that gender to the pool)
            "Hermaphroditic": ["Other", "Hybrid", "Nightmare", "Dryad", "Plantfolk", "Triton", "Insectoid", "Kling", "Starborn"],
            "Parthenogenic": ["Strix", "Other", "Hybrid", "Plasmoid", "True Dragon", "Plantfolk", "Mushroomfolk", "Aarakocra", "Turtoid", "Mermaid", "Insectoid", "Lizardfolk", "Firefly"],
            "Seasonally Dimorphic": ["Other", "Hybrid", "Nymph", "Plantfolk", "Pixie", "Insectoid", "Grung", "Fairy", "Voidling"],
        }

        # Build the gender pool
        pool = list(default_pool)

        for gender, species_list in species_gender_map.items():
            if race in species_list:
                if gender in pool:
                    pool.remove(gender)   # remove default
                else:
                    pool.append(gender)   # add rare gender
        # The design intentionally allows for a pool with only rare genders
        # The design is not meant to flow equally among all genders: some are always added while others are alwaysremoved


        # Assign default weights for the current pool
        # Rare genders can get fixed weights or proportional scaling
        weights = []
        for g in pool:
            if g in ["Male", "Female", "Lost", "Androgine"]:
                weights.append(default_weights[default_pool.index(g)])
            else:
                # Assign a small fixed weight for rare genders
                weights.append(9000)  # shared weight by rare genders

        # Pick a gender
        return random.choices(pool, weights=weights, k=1)[0]

    def generate_age_and_category(self, race):
        # Return (age_category, age) based on race-specific distributions
        # Map
        race_age_ranges = {
            "Polar Human": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "Quarryan Human": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "South Herian Human": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "North Herian Human": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "Plains Dorojan Human": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "Mountains Dorojan Human": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "Common Elf": {"child": (0, 10), "teen": (11, 100), "adult": (101, 8000), "middle-aged": (8001, 18000), "elderly": (18001, 20000)},
            "Dwarf": {"child": (0, 20), "teen": (21, 40), "adult": (41, 150), "middle-aged": (151, 280), "elderly": (281, 500)},
            "Dragonborn": {"child": (0, 10), "teen": (11, 20), "adult": (21, 80), "middle-aged": (81, 120), "elderly": (121, 150)},
            "Beastfolk": {"child": (0, 8), "teen": (9, 15), "adult": (16, 60), "middle-aged": (61, 90), "elderly": (91, 120)},
            "Gnome": {"child": (0, 40), "teen": (41, 80), "adult": (81, 200), "middle-aged": (201, 300), "elderly": (301, 500)},
            "Ogre": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 50), "elderly": (51, 70)},
            "Half-Elf": {"child": (0, 10), "teen": (11, 19), "adult": (20, 200), "middle-aged": (201, 400), "elderly": (401, 600)},
            "Lost Goblin": {"child": (0, 4), "teen": (5, 9), "adult": (10, 20), "middle-aged": (21, 40), "elderly": (41, 55)},
            "Dark Elf": {"child": (0, 50), "teen": (51, 140), "adult": (141, 400), "middle-aged": (401, 550), "elderly": (551, 800)},
            "Aarakocra": {"child": (0, 3), "teen": (4, 6), "adult": (7, 20), "middle-aged": (21, 30), "elderly": (31, 40)},
            "Tabaxi": {"child": (0, 3), "teen": (5, 9), "adult": (10, 30), "middle-aged": (31, 50), "elderly": (51, 65)},
            "Kenku": {"child": (0, 3), "teen": (4, 6), "adult": (7, 25), "middle-aged": (26, 40), "elderly": (41, 50)},
            "Goliath": {"child": (0, 4), "teen": (5, 8), "adult": (9, 30), "middle-aged": (31, 45), "elderly": (46, 60)},
            "Celestial": {"child": (0, 1), "teen": (2, 3), "adult": (4, 1101), "middle-aged": (11000, 16001), "elderly": (16000, 20000)},
            "Half-Ogre": {"child": (0, 5), "teen": (6, 13), "adult": (14, 40), "middle-aged": (41, 60), "elderly": (61, 80)},
            "Pixie": {"child": (0, 2), "teen": (3, 4), "adult": (5, 20), "middle-aged": (21, 35), "elderly": (36, 45)},
            "Turtoid": {"child": (0, 3), "teen": (4, 10), "adult": (11, 120), "middle-aged": (121, 150), "elderly": (151, 270)},
            "Triton": {"child": (0, 5), "teen": (6, 10), "adult": (11, 40), "middle-aged": (41, 60), "elderly": (61, 80)},
            "Mermaid": {"child": (0, 15), "teen": (16, 35), "adult": (36, 15000), "middle-aged": (15000, 19000), "elderly": (19999, 20000)},
            "Half-Dragon": {"child": (0, 5), "teen": (6, 23), "adult": (23, 50), "middle-aged": (51, 80), "elderly": (81, 110)},
            "Insectoid": {"child": (0, 1), "teen": (2, 3), "adult": (4, 9), "middle-aged": (10, 14), "elderly": (15, 20)},
            "Lycantropus": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Grung": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Kling": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Fairy": {"child": (0, 100), "teen": (101, 180), "adult": (181, 200), "middle-aged": (201, 220), "elderly": (221, 235)},
            "Satyr": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Halfling": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "Orc": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 50), "elderly": (51, 70)},
            "Tiefling": {"child": (0, 10), "teen": (11, 19), "adult": (20, 70), "middle-aged": (71, 100), "elderly": (101, 120)},
            "Yuan-Ti": {"child": (0, 5), "teen": (6, 10), "adult": (11, 40), "middle-aged": (41, 60), "elderly": (61, 80)},
            "Kobold": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Lizardfolk": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Aasimar": {"child": (0, 1), "teen": (2, 3), "adult": (4, 100), "middle-aged": (101, 120), "elderly": (120, 1000)},
            "Firbolg": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 50), "elderly": (51, 70)},
            "Bugbear": {"child": (0, 5), "teen": (6, 10), "adult": (11, 35), "middle-aged": (36, 55), "elderly": (56, 80)},
            "Hobgoblin": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 50), "elderly": (51, 70)},
            "Sentient Undead": {"child": (0, 500), "teen": (501, 510), "adult": (511, 530), "middle-aged": (531, 550), "elderly": (551, 750)},
            "Moonling": {"child": (0, 5), "teen": (6, 10), "adult": (11, 40), "middle-aged": (41, 60), "elderly": (61, 80)},
            "Starborn": {"child": (0, 10), "teen": (11, 19), "adult": (20, 40), "middle-aged": (41, 65), "elderly": (66, 90)},
            "Voidling": {"child": (0, 5), "teen": (6, 10), "adult": (11, 25), "middle-aged": (26, 40), "elderly": (41, 60)},
            "Firefly": {"child": (0, 1), "teen": (2, 3), "adult": (4, 10), "middle-aged": (11, 15), "elderly": (16, 20)},
            "Shadowkin": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Crystalborn": {"child": (0, 3), "teen": (4, 5), "adult": (6, 17), "middle-aged": (18, 25), "elderly": (26, 33)},
            "Deep-Elf": {"child": (0, 14), "teen": (15, 200), "adult": (201, 7000), "middle-aged": (7001, 14000), "elderly": (14001, 20000)},
            "Wood Elf": {"child": (0, 50), "teen": (51, 150), "adult": (151, 3000), "middle-aged": (3001, 4000), "elderly": (4001, 7500)},
            "Mushroomfolk": {"child": (0, 10), "teen": (11, 20), "adult": (21, 80), "middle-aged": (81, 120), "elderly": (121, 150)},
            "Sentient Construct": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 500), "elderly": (501, 20000)},
            "Elementalfolk": {"child": (0, 16), "teen": (17, 200), "adult": (201, 8000), "middle-aged": (8001, 12000), "elderly": (12001, 15000)},
            "Plantfolk": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "True Dragon": {"child": (0, 110), "teen": (111, 300), "adult": (301, 800), "middle-aged": (801, 1200), "elderly": (1201, 3500)},
            "Giant": {"child": (0, 10), "teen": (11, 20), "adult": (21, 100), "middle-aged": (101, 200), "elderly": (201, 300)},
            "Demon": {"child": (0, 1200), "teen": (1201, 1800), "adult": (1801, 16500), "middle-aged": (16501, 18000), "elderly": (18001, 20000)},
            "Angel": {"child": (0, 1200), "teen": (1201, 1800), "adult": (1801, 16500), "middle-aged": (16501, 18000), "elderly": (18001, 20000)},
            "Plasmoid": {"child": (0, 2), "teen": (3, 4), "adult": (5, 29), "middle-aged": (30, 35), "elderly": (36, 45)},
            "Demonoid": {"child": (0, 12), "teen": (13, 109), "adult": (110, 150), "middle-aged": (151, 200), "elderly": (201, 250)},
            "Spirit": {"child": (0, 2000), "teen": (2001, 5000), "adult": (5001, 10000), "middle-aged": (10001, 15000), "elderly": (15001, 20000)},
            "Sylph": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Salamanderman": {"child": (0, 3), "teen": (4, 6), "adult": (7, 20), "middle-aged": (21, 33), "elderly": (34, 46)},
            "Oni": {"child": (0, 5), "teen": (6, 10), "adult": (11, 40), "middle-aged": (41, 60), "elderly": (61, 80)},
            "Kijin": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "Majin": {"child": (0, 1), "teen": (2, 3), "adult": (4, 10), "middle-aged": (11, 15), "elderly": (16, 20)},
            "Strix": {"child": (0, 1), "teen": (2, 3), "adult": (4, 10), "middle-aged": (11, 15), "elderly": (16, 20)},
            "Changeling": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 50), "elderly": (51, 70)},
            "Dryad": {"child": (0, 5), "teen": (6, 10), "adult": (11, 40), "middle-aged": (46, 50), "elderly": (51, 58)},
            "Nymph": {"child": (0, 20), "teen": (20, 100), "adult": (101, 400), "middle-aged": (406, 500), "elderly": (501, 508)},
            "Lost Sea Goblin": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 50), "elderly": (51, 70)},
            "Gooba": {"child": (0, 2), "teen": (3, 4), "adult": (5, 15), "middle-aged": (16, 25), "elderly": (26, 35)},
            "True Vampire": {"child": (0, 1), "teen": (2, 3), "adult": (4, 50), "middle-aged": (51, 2000), "elderly": (2001, 2600)},
            "Pale Knight": {"child": (0, 19), "teen": (20, 40), "adult": (41, 130), "middle-aged": (131, 150), "elderly": (151, 200)},
            "Lopunnie": {"child": (0, 5), "teen": (6, 10), "adult": (11, 40), "middle-aged": (41, 60), "elderly": (61, 80)},
            "Nightmare": {"child": (0, 5), "teen": (6, 7), "adult": (8, 16), "middle-aged": (17, 18), "elderly": (19, 20)},
            "Wisp": {"child": (0, 9), "teen": (10, 11), "adult": (12, 20), "middle-aged": (21, 25), "elderly": (26, 30)},
            "Moonskin Elf": {"child": (0, 18), "teen": (19, 100), "adult": (101, 500), "middle-aged": (501, 800), "elderly": (801, 1050)},
            "Spectre": {"child": (0, 5), "teen": (6, 10), "adult": (11, 30), "middle-aged": (31, 50), "elderly": (51, 70)},
            "Banshee": {"child": (0, 1), "teen": (2, 3), "adult": (4, 10), "middle-aged": (11, 15), "elderly": (16, 20)},
            "Wolfang": {"child": (0, 5), "teen": (6, 10), "adult": (11, 35), "middle-aged": (36, 45), "elderly": (46, 70)},
            "Foxling": {"child": (0, 5), "teen": (6, 10), "adult": (11, 40), "middle-aged": (41, 60), "elderly": (61, 80)},
            "Common Birdling": {"child": (0, 3), "teen": (4, 6), "adult": (7, 20), "middle-aged": (21, 30), "elderly": (31, 40)},
            "Hybrid": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)},
            "Other": {"child": (0, 10), "teen": (11, 19), "adult": (20, 50), "middle-aged": (51, 60), "elderly": (61, 100)}
        }
        age_category = random.choices(
            population=list(race_age_ranges[race].keys()),
            weights=[3, 2, 3, 2, 1],  # Probabilities to favour certain age groups
            k=1
        )[0]
        age_min, age_max = race_age_ranges[race][age_category]
        age = random.randint(age_min, age_max)
        return age_category, age

    def generate_partnership(self, age_category):
        options_by_age = {
            "child": {"Unattached": 1.0},
            "teen": {"Content Single": 0.45, "Looking": 0.25, "In a Relationship": 0.25, "Engaged": 0.05},
            "adult": {"Content Single": 0.25, "Looking": 0.2, "In a Relationship": 0.2,
                    "Engaged": 0.15, "Soon-to-be Married": 0.05,
                    "Newlywed": 0.1, "Married (Bronze Marriage)": 0.05},
            "middle-aged": {"Content Single": 0.1, "Looking": 0.1, "In a Relationship": 0.15,
                            "Married (Bronze Marriage)": 0.15, "Married (Silver Marriage)": 0.2,
                            "Lifelong Partner": 0.15, "Widowed": 0.15},
            "elderly": {"Content Single": 0.1, "Widowed": 0.5,
                        "Lifelong Partner": 0.3, "Companionship (Non-Marital)": 0.1}
        }

        choices = list(options_by_age[age_category].keys())
        weights = list(options_by_age[age_category].values())
        return random.choices(choices, weights=weights, k=1)[0]

    def generate_num_descendants(self, age_category, partnership):

        modifier = 1.0

        options_by_age = {
            # Distribution settings, negative values allowed for low end to simulate no descendants
            "child": (0, 0, 0),
            "teen": (-19, 1, -9),
            "adult": (-2, 4, 1),
            "middle-aged": (-4, 6, 2),
            "elderly": (-1, 10, 3)
        }

        low, high, mode = options_by_age[age_category]
        base_descendants = random.triangular(low, high, mode)

        #hack to prevent negative descendants
        if base_descendants <= 0:
            base_descendants = 0

        # Modify by partnership
        if partnership:
            if "Married" in partnership or "Engaged" in partnership:
                if age_category != "teen":
                    modifier = 1.5
            elif "Widow" or "Lifelong Partner" in partnership:
                modifier = 1.4
            else:
                modifier = 0.6
        
        base_descendants = int(round(base_descendants * modifier))
        return base_descendants

    def generate_occupation(self, social_level, age_category):

        # Dictionary of occupations by social level with their selection probabilities
        # Map2
        occupations_by_social = {
            "Royal": {"Monarch": 0.05, "Prince/Princess": 0.1, "High Diplomat": 0.25, "Chancelor": 0.05, "Chamberlain": 0.05, "General": 0.15, "High Priest": 0.05, "Royal Advisor": 0.2, "Exotic": 0.1},
            "Noble": {"Lord/Lady": 0.05, "Knight": 0.06, "Merchant Lord": 0.12, "Politician": 0.02, "Judge": 0.02, "Guildmaster": 0.05, "Cleric/Bishop": 0.01, "Temple Keeper": 0.01, "Archmage": 0.01, "Architect": 0.06, "Engineer": 0.06, "Historian": 0.05, "Cartographer": 0.03, "Explorer": 0.04, "Entrepreneur": 0.08, "Ship Captain/Admiral": 0.02, "Banker": 0.06, "Noble Hunter/Falconer": 0.01, "Artist": 0.02, "Patron of the Arts": 0.06, "Specialised Doctor": 0.06, "Exotic": 0.1},
            "Commoner": {"Farmer": 0.065, "Blacksmith": 0.025, "Healer": 0.005, "Soldier": 0.08, "Merchant": 0.08, "Bard": 0.005, "Builder/Site Manager": 0.09, "Tailor/Leatherworker": 0.03, "Innkeeper": 0.04, "Cook": 0.02, "Brewer": 0.005, "Apothecary": 0.025, "Priest/Monk": 0.01, "Bard/Entertainer": 0.02, "Fisher": 0.08, "Sailor": 0.02, "Dockworker": 0.02, "Miner": 0.02, "Librarian": 0.01, "Hunter": 0.05, "Teacher/Tutor": 0.03, "Adventurer/Mercenary": 0.08, "Beggar/Vagrant": 0.03, "Artist": 0.01, "Explorer": 0.05, "Cartographer": 0.01, "Mage": 0.005, "Courier": 0.015, "Waiter": 0.05, "Doctor": 0.04, "Nurse": 0.01, "Exotic": 0.08},
            "Peasant": {"Farmer/Field Worker": 0.8, "Shepherd": 0.08, "Laborer": 0.05, "Fisher": 0.1, "Servant/Housemaid": 0.05, "Peddler": 0.04, "Tinker": 0.02, "Stablehand": 0.01, "Nurse": 0.06, "Soldier": 0.1, "Monk": 0.07, "Beggar/Vagrant": 0.03, "Dockworker": 0.01, "Miner": 0.08, "Performer": 0.05, "Sailor": 0.05, "Hunter": 0.02, "Waiter": 0.04, "Exotic": 0.05},
            "Slave": {"Laborer": 0.15, "Domestic Servant": 0.15, "Field Worker": 0.3, "Pleasure Performer": 0.1, "Tinker": 0.02, "Miner": 0.1, "Performer": 0.03, "Exotic": 0.05}
        }

        # Dictionary of exotic occupations and their selection probabilities for NPCs with "Exotic" jobs
        exotic = {"Monster Hunter": 0.05, "Witch/Warlock": 0.03, "Necromancer": 0.02, "Oracle/Dream Interpreter": 0.05, "Beast Tamer": 0.05, "Familiar Keeper": 0.02, "Artifact Collector": 0.05, "Inventor": 0.02, "Pirate": 0.02, "Gravekeeper": 0.01, "Assassin/Spy": 0.02, "Magical Item Broker": 0.12, "Rune Engraver/Enchanter": 0.1, "Wyvern Keeper": 0.02, "Demonologist": 0.01, "Traveler": 0.1, "Elemental Binder": 0.01, "Chronomancer": 0.01, "Portal Keeper": 0.04, "Astrologer": 0.02, "Vet/Beasts' Doctor": 0.04, "Arms Dealer/Drug Dealer": 0.06, "Slave Trader": 0.08, "Mafia Boss": 0.01, "Gangster": 0.03, "Other": 0.03}

        # Define employment stage weights based on age category
        age_weights = {
            "child": {"Unemployed": 0.55, "Apprentice/Student": 0.45},
            "teen": {"Unemployed": 0.15, "Apprentice/Student": 0.6, "Minor Worker": 0.2, "Full-time Occupation": 0.05},
            "adult": {"Full-time Occupation": 0.6,"Unemployed": 0.15, "Minor Worker": 0.2, "Apprentice/Student": 0.05},
            "middle-aged": {"Full-time Occupation": 0.6,"Unemployed": 0.15, "Minor Worker": 0.25},
            "elderly": {"Retired": 0.5, "Advisor": 0.3, "Minor Duties": 0.3}
        }

        # Choose the employment stage for this age
        stage_choices = list(age_weights[age_category].keys())
        stage_weights = list(age_weights[age_category].values())
        employment_stage = random.choices(stage_choices, weights=stage_weights, k=1)[0]


        # Choose the job for this social level
        job_choices = list(occupations_by_social[social_level].keys())
        job_weights = list(occupations_by_social[social_level].values())
        job = random.choices(job_choices, weights=job_weights, k=1)[0]

        # If job is Exotic, pick a specific exotic job
        if job == "Exotic":
            job_choices = list(exotic.keys())
            job_weights = list(exotic.values())
            job = random.choices(job_choices, weights=job_weights, k=1)[0]

        # Build the output depending on stage
        if "Unemployed" in employment_stage or "Minor Duties" in employment_stage:
            # Output format: “Employment Stage”, e.g., “Unemployed” or “Minor Duties”
            occupation = employment_stage
        elif "Retired" in employment_stage or "Advisor" in employment_stage:
            # Output format: “Employment Stage (Last known occupation: Job)”, e.g., “Retired (Last known occupation: Blacksmith)” or “Advisor (Last known occupation: Healer)”
            occupation = f"{employment_stage} (Last known occupation: {job})"
        else:
            # Output format: “Employment Stage (Job)”, e.g., “Apprentice/Student (Blacksmith)” or “Full-time Occupation (Healer)”
            occupation = f"{employment_stage} ({job})"

        return occupation

    # Map2
    social_levels = [("Royal", 0.01), ("Noble", 0.14), ("Peasant", 0.30), ("Commoner", 0.35), ("Slave", 0.2)]

    def generate_wealth(self, social_level):
        # Return wealth appropriate for social class
        # Map2
        wealth_by_social = {
            "Royal": ["Opulent", "Rich", "Wealthy"],
            "Noble": ["Opulent", "Wealthy", "Rich", "Modest"],
            "Commoner": ["Modest", "Poor", "Wealthy"],
            "Peasant": ["Poor", "Modest", "Wealthy"],
            "Slave": ["Poor", "Modest"]
        }

        # Randomly pick one from the social-level pool
        wealth = random.choice(wealth_by_social.get(social_level))
        return wealth

    def generate_personality_traits(self, personality_traits_count):
        # Return a list of personality traits
        default_traits = [
            "Brave", "Cautious", "Curious", "Loyal", "Greedy", "Honest", "Deceptive",
            "Charismatic", "Impulsive", "Reserved", "Ambitious", "Lazy", "Friendly",
            "Temperamental", "Righteous", "Sarcastic", "Arrogant", "Protective", "Dreamy",
            "Pessimistic", "Cheerful", "Brooding", "Stoic", "Generous", "Vindictive", "Adventurous",
            "Meticulous", "Reckless", "Optimistic", "Skeptical", "Compassionate", "Calculating",
            "Patient", "Hot-headed", "Wise", "Naive", "Cynical", "Romantic", "Pragmatic", "Stubborn",
            "Ruthless", "Manipulative", "Hypercritical", "Obsessive", "Cruel", "Fanatical",
            "Jealous", "Crazy", "Eccentric"]

        
        traits = random.sample(default_traits, k=personality_traits_count)
        return traits
    
    def infer_alignment_from_personality(self, traits):

        # Simple heuristic: count good vs evil traits
        good_traits = {"Brave", "Loyal", "Honest", "Friendly", "Righteous", "Protective", "Generous", "Compassionate", "Wise", "Patient", "Optimistic"}
        evil_traits = {"Greedy", "Deceptive", "Arrogant", "Vindictive", "Calculating", "Cynical", "Manipulative", "Ruthless", "Cruel", "Obsessive", "Fanatical"}
        #Good is counted as positive, Evil as negative
        good_evil_score = 0
        for trait in traits:
            if trait in good_traits:
                good_evil_score += 1
            elif trait in evil_traits:
                good_evil_score -= 1

        # Simple heuristic: count lawful vs chaotic traits
        lawful_traits = {"Cautious", "Loyal", "Honest", "Reserved", "Meticulous", "Patient", "Wise", "Pragmatic", "Righteous", "Calculating", "Stoic", "Obsessive"}
        chaotic_traits = {"Impulsive", "Temperamental", "Reckless", "Adventurous", "Dreamy", "Romantic", "Hot-headed", "Stubborn", "Curious", "Crazy", "Eccentric", "Jealous"}
        #Lawful is counted as positive, Chaotic as negative
        lawful_chaotic_score = 0
        for trait in traits:
            if trait in lawful_traits:
                lawful_chaotic_score += 1
            elif trait in chaotic_traits:
                lawful_chaotic_score -= 1
        
        # Determine alignment based on scores
        if good_evil_score > 0:
            alignment = "Good"
        elif good_evil_score < 0:
            alignment = "Evil"
        else:
            alignment = "Neutral"
        
        if lawful_chaotic_score > 0:
            alignment = f"Lawful {alignment}"
        elif lawful_chaotic_score < 0:
            alignment = f"Chaotic {alignment}"
        else:
            if alignment == "Neutral":
                alignment = "True Neutral"
                #Special case for pure neutral
            else:
                alignment = f"Neutral {alignment}"
        
        
        return alignment
    
    def infer_reputation_from_personality(self, traits):
        # List of reputation types and their initial scores
        # All reputation types are initialized to 0 except "Lightly Noticeable" and "Unknown", which start at 1 to ensure every NPC has a standard valid reputation.
        reputation_types = {"Lovely": 0, "Respectful": 0, "Honorable": 0, "Trustworthy": 0, "Valuable": 0, "Unknown": 0, "Mysterious": 0,
                            "Lightly Noticeable": 1, "Fearsome": 0, "Loathsome": 0, "Unreliable": 0, "Ruthless": 0, "Disgraceful": 0,
                            "Cunning": 0, "Ambiguous": 0,"Infamous": 0, "Bearable": 1, "Edgy": 0, "Charming": 0, "Dull": 0}
        # Dictionary mapping: trait to reputation score adjustments
        # Map3
        trait_to_reputation = {
            "Brave": {"Respectful": 2, "Fearsome": 2, "Valuable": 2, "Cunning": 1, "Dull": -1, "Lightly Noticeable": -1},
            "Cautious": {"Trustworthy": 2, "Respectful": 1, "Dull": 1, "Edgy": -1, "Unknown": 1},
            "Curious": {"Mysterious": 1, "Dull": -1, "Lightly Noticeable": -1, "Ambiguous": 1, "Bearable": 1, "Lovely": 1},
            "Loyal": {"Honorable": 2, "Trustworthy": 3, "Respectful": 2, "Infamous": -1, "Loathsome": -1, "Unreliable": -1,},
            "Greedy": {"Loathsome": 1, "Cunning": 1, "Infamous": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1},
            "Honest": {"Honorable": 2, "Trustworthy": 2, "Respectful": 1, "Cunning": -1, "Ambiguous": -1, "Infamous": -1, "Loathsome": -1, "Disgraceful": -1},
            "Deceptive": {"Unreliable": 1, "Cunning": 1, "Infamous": 1, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Ambiguous": 2, "Charming": -1, "Dull": -1},
            "Charismatic": {"Charming": 3, "Lovely": 2, "Trustworthy": 1, "Loathsome": -1, "Dull": -1, "Unknown": -1, "Lightly Noticeable": -1},
            "Impulsive": {"Edgy": 1, "Fearsome": 1, "Dull": -1, "Respectful": -1, "Honorable": -1, "Cunning": -1, "Unknown": -1, "Bearable": -1},
            "Reserved": {"Dull": 2, "Mysterious": 1, "Respectful": 1, "Charming": -1, "Edgy": -1, "Lightly Noticeable": -1, "Unknown": 1, "Ambiguous": 1},
            "Ambitious": {"Mysterious": 1, "Fearsome": 1, "Edgy": 1, "Cunning": 2, "Dull": -1},
            "Lazy": {"Unknown": 1, "Charming": -1, "Bearable": -1, "Honorable": -1, "Disgraceful": 1, "Loathsome": 1},
            "Friendly": {"Valuable": 2,"Lovely": 2, "Trustworthy": 2, "Charming": 2, "Dull": -1, "Mysterious": -1, "Loathsome": -1},
            "Temperamental": {"Unreliable": 1, "Charming": -1, "Dull": -1, "Respectful": -1, "Unknown": -1, "Bearable": -1,},
            "Righteous": {"Honorable": 3, "Respectful": 2, "Trustworthy": 1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Unknown": -1, "Lightly Noticeable": -1, "Dull": 1},
            "Sarcastic": {"Cunning": 2, "Edgy": 2, "Charming": 2, "Dull": -1, "Lovely": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": 1, "Mysterious": 1},
            "Arrogant": {"Loathsome": 2, "Infamous": 2, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1, "Unknown": -1, "Disgraceful": 1},
            "Protective": {"Honorable": 2, "Respectful": 2, "Trustworthy": 2, "Lovely": 1, "Fearsome": 1, "Charming": 1, "Valuable": 1},
            "Dreamy": {"Mysterious": 2, "Edgy": 1, "Dull": -1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Bearable": 1, "Lightly Noticeable": 1},
            "Pessimistic": {"Dull": 2, "Unknown": 1, "Bearable": -1, "Lovely": -1, "Charming": -1, "Edgy": -1},
            "Cheerful": {"Lovely": 2, "Charming": 2, "Respectful": 1, "Dull": -1, "Mysterious": -1, "Loathsome": -1},
            "Brooding": {"Mysterious": 2, "Edgy": 1, "Dull": 1, "Lovely": -1, "Charming": -1, "Lightly Noticeable": -1, "Unknown": 2, "Ambiguous": 1, "Fearsome": 1, "Loathsome": 1},
            "Stoic": {"Respectful": 1, "Honorable": 1, "Dull": 2, "Mysterious": 1, "Charming": -1, "Edgy": -1, "Lightly Noticeable": -1, "Unknown": 1, "Ambiguous": 1},
            "Generous": {"Lovely": 2, "Honorable": 2, "Trustworthy": 1, "Respectful": 1, "Cunning": -1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Charming": 1},
            "Vindictive": {"Ruthless": 2, "Infamous": 2, "Loathsome": 1, "Cunning": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1, "Charming": -1, "Unknown": -1},
            "Adventurous": {"Edgy": 1, "Fearsome": 1, "Mysterious": 1, "Dull": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Lightly Noticeable": 1},
            "Meticulous": {"Respectful": 2, "Trustworthy": 2, "Honorable": 1, "Dull": 1, "Edgy": -1, "Unknown": 2},
            "Reckless": {"Fearsome": 2, "Edgy": 2, "Dull": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Ruthless": 1},
            "Optimistic": {"Lovely": 2, "Charming": 2, "Trustworthy": 1, "Respectful": 1, "Dull": -1, "Mysterious": -1, "Loathsome": -1, "Unknown": -1, "Lightly Noticeable": -1, "Disgraceful": -1},
            "Skeptical": {"Cunning": 1, "Mysterious": 1, "Dull": 1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Unreliable": 1},
            "Compassionate": {"Lovely": 2, "Honorable": 2, "Respectful": 1, "Valuable": 1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Cunning": -1},
            "Calculating": {"Cunning": 1, "Infamous": 1, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Charming": -1},
            "Patient": {"Respectful": 2, "Trustworthy": 1, "Honorable": 1, "Dull": 1, "Edgy": -1, "Unknown": 2, "Lovely": 1},
            "Hot-headed": {"Edgy": 2, "Fearsome": 1, "Dull": -1, "Respectful": -1, "Honorable": -1, "Cunning": -1, "Unknown": -1, "Bearable": -1, "Unreliable": 1},
            "Wise": {"Respectful": 2, "Honorable": 2, "Trustworthy": 2, "Valuable": 1, "Mysterious": 1, "Dull": 1, "Charming": -1, "Edgy": -1, "Unknown": 1},
            "Naive": {"Dull": 2, "Lovely": 1, "Charming": 1, "Respectful": 1, "Edgy": -1, "Cunning": -1, "Loathsome": -1, "Infamous": -1, "Disgraceful": -1, "Unknown": 1, "Bearable": 1},
            "Cynical": {"Cunning": 2, "Dull": 1, "Lovely": -1, "Charming": -1, "Unknown": 1, "Ambiguous": 1, "Unreliable": 1},
            "Romantic": {"Charming": 3, "Lovely": 2, "Mysterious": 1, "Dull": -1, "Unknown": 1, "Lightly Noticeable": 1, "Disgraceful": -1},
            "Pragmatic": {"Respectful": 1, "Trustworthy": 2, "Cunning": 1, "Dull": 1, "Edgy": -1, "Unknown": 2},
            "Stubborn": {"Dull": 2, "Edgy": 1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Unreliable": 2},
            "Ruthless": {"Ruthless": 3, "Infamous": 2, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1, "Charming": -1, "Unknown": -1, "Disgraceful": 1},
            "Manipulative": {"Cunning": 2, "Infamous": 2, "Loathsome": 1, "Honorable": -1, "Trustworthy": -1, "Lovely": -1, "Ruthless": 1, "Ambiguous": 2, "Charming": 1, "Dull": -1},
            "Hypercritical": {"Cunning": 1, "Dull": 1, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Disgraceful": 1},
            "Obsessive": {"Cunning": 2, "Edgy": 1, "Mysterious": 1, "Dull": 1, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1},
            "Cruel": {"Edgy": 2, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Unknown": -1, "Bearable": -1, "Disgraceful": 2, "Loathsome": 2, "Infamous": 1, "Ruthless": 2},
            "Fanatical": {"Ruthless": 2, "Fearsome": 1, "Loathsome": 1, "Infamous": 1, "Honorable": -1, "Trustworthy": -1, "Respectful": -1, "Lovely": -1, "Charming": -1, "Unknown": -1, "Disgraceful": 1, "Unreliable": 1},
            "Jealous": {"Edgy": 1, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Unknown": -1, "Bearable": -1, "Disgraceful": 2, "Loathsome": 1, "Infamous": 1},
            "Crazy": {"Mysterious": 2, "Edgy": 2, "Lovely": -1, "Charming": -1, "Respectful": -1, "Honorable": -1, "Trustworthy": -1, "Unknown": -1, "Bearable": -1, "Lightly Noticeable": -1, "Cunning": -1},
            "Eccentric": {"Mysterious": 2, "Edgy": 1, "Lovely": -1, "Charming": -1, "Dull": -1, "Unknown": 1, "Ambiguous": 1, "Lightly Noticeable": 1}
        }

        # Adjust reputation scores based on personality traits
        for trait in traits:
            if trait in trait_to_reputation:
                adjustments = trait_to_reputation[trait]
                for rep_type, score in adjustments.items():
                    reputation_types[rep_type] += score
        # Determine the top 2 reputation types
        sorted_reputations = sorted(reputation_types.items(), key=lambda x: x[1], reverse=True)
        top_reputations = [rep for rep, score in sorted_reputations if score == sorted_reputations[0][1]]
        # If multiple top reputations, randomly select one
        reputation = random.choice(top_reputations)
        return reputation

    # Data extractor for mapping letters
    with open(r"C:\Users\balea\Desktop\.py\NPC generator\names_transition.json", "r", encoding="utf-8") as f:
        name_data = json.load(f)

    # Race → flavour mapping
    flavour_map = {
        "Polar Human": "Human",
        "Quarryan Human": "Human",
        "South Herian Human": "Human",
        "North Herian Human": "Human",
        "Plains Dorojan Human": "Human",
        "Mountains Dorojan Human": "Human",
        "Half-Elf": "Human",
        "Plasmoid": "Human",
        "Spirit": "Human",
        "Lopunnie": "Human",
        "Common Birdling": "Human",
        "Hybrid": "Human",
        "Other": "Human",
        "Common Elf": "Fairy",
        "Dark Elf": "Fairy",
        "Wood Elf": "Fairy",
        "Deep Elf": "Fairy",
        "Moonskin Elf": "Fairy",
        "Pixie": "Fairy",
        "Fairy": "Fairy",
        "Firbolg": "Fairy",
        "Elementalfolk": "Fairy",
        "Sylph": "Fairy",
        "Dryad": "Fairy",
        "Gnome": "Dwarvish",
        "Dwarf": "Dwarvish",
        "Tabaxi": "Dwarvish",
        "Kenku": "Dwarvish",
        "Goliath": "Dwarvish",
        "Beastfolk": "Dwarvish",  # shared flavour
        "Satyr": "Dwarvish",
        "Bugbear": "Dwarvish",
        "Sentient Construct": "Dwarvish",
        "Giant": "Dwarvish",
        "Wolfang": "Dwarvish",
        "Dragonborn": "Draconic",
        "Half-Dragon": "Draconic",
        "True Dragon": "Draconic",
        "Kobold": "Draconic",
        "Lizardfolk": "Draconic",
        "Firefly": "Draconic",
        "Pale Knight": "Draconic",
        "Lost Goblin": "Wildermagic",
        "Hobgoblin": "Wildermagic",
        "Lost Sea Goblin": "Wildermagic",
        "Mushroomfolk": "Wildermagic",
        "Ogre": "Wildermagic",
        "Half-Ogre": "Wildermagic",
        "Insectoid": "Wildermagic",
        "Grung": "Wildermagic",
        "Kling": "Wildermagic",
        "Halfling": "Wildermagic",
        "Orc": "Wildermagic",
        "Plantfolk": "Wildermagic",
        "Tiefling": "Fiendish",
        "Demonoid": "Fiendish",
        "Yuan-Ti": "Fiendish",
        "Demon": "Fiendish",
        "Salamanderman": "Fiendish",
        "Oni": "Fiendish",
        "Kijin": "Fiendish",
        "Majin": "Fiendish",
        "Strix": "Fiendish",
        "Nightmare": "Fiendish",
        "Celestial": "Celestial",
        "Angel": "Celestial",
        "Aarakocra": "Celestial",
        "Aasimar": "Celestial",
        "Moonling": "Celestial",
        "Foxling": "Celestial",
        "Shadowkin": "Shadowy",
        "Wisp": "Shadowy",
        "Voidling": "Shadowy",
        "Lycantropus": "Shadowy",
        "Sentient Undead": "Shadowy",
        "Starborn": "Shadowy",
        "Crystalborn": "Shadowy",
        "Changeling": "Shadowy",
        "True Vampire": "Shadowy",
        "Spectre": "Shadowy",
        "Triton": "Marine",
        "Mermaid": "Marine",
        "Nymph": "Marine",
        "Turtoid": "Marine",
        "Gooba": "Marine",
        "Banshee": "Marine",
    }

    # Word assembler
    def generate_name(self, transitions, min_len, max_len):
        start_symbol = "/"
        end_symbol = "$"
        vowels = set("aeiouyáéíóúýàèìòùäëû")
        
        current = start_symbol
        name = ""
        consonant_streak = 0

        while True:
            # Get next transition
            rand = random.random()
            cumulative = 0
            next_char = None

            for nxt, prob in transitions[current]:
                cumulative += prob
                if rand <= cumulative:
                    next_char = nxt
                    break

            if not next_char:
                break

            if next_char == end_symbol:
                if len(name) >= min_len:
                    break
                else:
                    continue

            # If we've had too many consonants, force a vowel
            if consonant_streak >= 2:
                possible_vowels = [v for v in vowels if v in [n for n, _ in transitions[current]]]
                if possible_vowels:
                    next_char = random.choice(possible_vowels)
                else:
                    next_char = random.choice(vowels)
                consonant_streak = 0  # reset after forcing a vowel

            # Add the letter
            if next_char != start_symbol:
                name += next_char

            # Update consonant streak
            if next_char in vowels:
                consonant_streak = 0
            else:
                consonant_streak += 1

            current = next_char

            # Safety cutoff
            if len(name) >= max_len:
                break

        return name.capitalize()

    # Actual name generating function
    def generate_npc_name(self, race, with_surname=True):
        flavour = self.flavour_map.get(race, "Human")
        transitions = self.name_data.get(flavour, {})
        if not transitions:
            return "Nameless"

        first = self.generate_name(transitions, random.randint(3, 5), random.randint(6, 12))
        if with_surname:
            surname = self.generate_name(transitions, random.randint(3, 7), random.randint(8, 12))
            return f"{first} {surname}"
        return first

    # Load the matrix for languages
    l_matrix = pd.read_csv(r"C:\Users\balea\Desktop\.py\NPC generator\languages_matrix.csv", index_col=0)

    # Race → native language mapping
    language_map = {
        "Polar Human": "Iceshard (Polar Humans)",
        "Quarryan Human": "Monochi (Quarryan Humans)",
        "South Herian Human": "Boulgbet (Herian Humans)",
        "North Herian Human": "Boulgbet (Herian Humans)",
        "Plains Dorojan Human": "Eclelcommon (Plains Dorojan Humans)",
        "Mountains Dorojan Human": "Naive (Mountains Dorojan Humans)",
        "Half-Elf": "Elvish",
        "Plasmoid": "Trumoid (Plasmoids)",
        "Spirit": "Enaven (Spirits)",
        "Lopunnie": "Bongy (Lopunnies)",
        "Common Birdling": "Avian (Birdlings)",
        "Hybrid": "Growl (Beastfolks)",
        "Other": "Growl (Beastfolks)",
        "Common Elf": "Elvish",
        "Dark Elf": "Drowic (Drows)",
        "Wood Elf": "Elvish",
        "Deep Elf": "Shofil (Deep Elves)",
        "Moonskin Elf": "Paleydrin (Moonskin Elves)",
        "Pixie": "Sylvan",
        "Fairy": "Sylvan",
        "Firbolg": "Goblin",
        "Elementalfolk": "Ancient Primordial",
        "Sylph": "Sylph",
        "Dryad": "Dryadic",
        "Gnome": "Gnim",
        "Dwarf": "Dwarvish",
        "Tabaxi": "Tabaxi",
        "Kenku": "Crowden (Kenkus)",
        "Goliath": "Gol-Kaa (Goliaths)",
        "Beastfolk": "Clorphine (Beastfolks)",
        "Satyr": "Faun",
        "Bugbear": "Goblin",
        "Sentient Construct": "Bit-Byte (Sentient Constructs)",
        "Giant": "Giant",
        "Wolfang": "Wolfang",
        "Dragonborn": "Draconic",
        "Half-Dragon": "Draconic",
        "True Dragon": "Draconic",
        "Kobold": "Yipyak",
        "Lizardfolk": "Draconic",
        "Firefly": "Ferish (Fireflies)",
        "Pale Knight": "Paladrin (Pale Knights)",
        "Lost Goblin": "Goblin",
        "Hobgoblin": "Goblin",
        "Lost Sea Goblin": "Goblin",
        "Mushroomfolk": "Mushrik (Mushroomfolk)",
        "Ogre": "Ogrish",
        "Half-Ogre": "Ogrish",
        "Insectoid": "Netfery (Insectoids)",
        "Grung": "Grung",
        "Kling": "Kling (Klings)",
        "Halfling": "Luiric",
        "Orc": "Orcish",
        "Plantfolk": "Leafly (Plantfolk)",
        "Tiefling": "Infernal",
        "Demonoid": "Abyssal",
        "Yuan-Ti": "Yuan-Tish (Yuan-Ti)",
        "Demon": "Abyssal",
        "Salamanderman": "Larsh (Salamandermen)",
        "Oni": "Oopkni (Oni people)",
        "Kijin": "Snept (Kijin people)",
        "Majin": "Ancient Primordial",
        "Strix": "Strict (Strixes)",
        "Nightmare": "Shriek (Nightmares)",
        "Celestial": "Celestial",
        "Angel": "Celestial",
        "Aarakocra": "Aarakocra",
        "Aasimar": "Celestial",
        "Moonling": "Moonlight (Moonlings)",
        "Foxling": "Vulpin (Foxlings)",
        "Shadowkin": "Darkspeak (Shadowkins)",
        "Wisp": "Auran",
        "Voidling": "Voshedi (Voidlings)",
        "Lycantropus": "Growl (Beastfolks)",
        "Sentient Undead": "Dark Speech",
        "Starborn": "Flashmy (Starborns)",
        "Crystalborn": "Pick Neet (Crystalborn)",
        "Changeling": "Sylvan",
        "True Vampire": "Echosnhachy (True Vampires)",
        "Spectre": "Dark Speech",
        "Triton": "Abyssal",
        "Mermaid": "Abyssal",
        "Nymph": "Sylvan",
        "Turtoid": "Turtoid (Turtoids)",
        "Gooba": "Goo Bee Nie (Gooba)",
        "Banshee": "Elvish",
    }

    def pick_languages(self, race):
        # Returns list of languages an NPC might know.
        native_lang = self.language_map.get(race, "Gibberish/Mute")
        if native_lang not in self.l_matrix.index:
            return [native_lang]
        
        weights = self.l_matrix.loc[native_lang]
        known = {native_lang}
        for lang, weight in weights.items():
            # Roll for each possible neighbour
            if random.random() < weight:
                known.add(lang)
        
        return ", ".join(known)

    # Constructor of NPC
    def __init__(self):
        self.fake = Faker()


    # From this point on i'll handle common stats useful for DMs

            # --- Core combat and progression ---
    hp = 10                   # depends on CON (and maybe race, size, level)
    ac = 10                   # base 10, modified by DEX, armor, and possibly race
    initiative = 0            # equals DEX mod (+ race or feats if you add them later)
    speed = {"walking": 30,
            "flying": 0,
            "swimming": 0,
            "climbing": 0}    # race-based primarily, possibly age-based
    level = 1                 # influences proficiency and class-like features
    size = "medium"           # depends on race and age category

    proficiency_bonus = 2     # directly derived from level

    # --- Ability scores and modifiers ---
    strength = 10             # race and age category affect
    strength_mod = 0          # derived from strength
    dexterity = 10            # race and age category affect
    dexterity_mod = 0         # derived from dexterity
    constitution = 10         # race and age category affect
    constitution_mod = 0      # derived from constitution
    intelligence = 10         # race and age category affect
    intelligence_mod = 0      # derived from intelligence
    wisdom = 10               # race and age category affect
    wisdom_mod = 0            # derived from wisdom
    charisma = 10             # race and age category affect
    charisma_mod = 0          # derived from charisma

    # --- Proficiencies ---
    weapons = []              # race, background, occupation
    armors = []               # race, background, occupation
    tools = []                # race, background, occupation
    skills = []               # race, background, occupation
    saving_throws = []        # race, background, occupation

    # --- Magic ---
    magic_source = None       # race, background, occupation (can be none, innate (spellcasting ability not required) or learned; those three parameters have power on each other in that order)
    spellcasting_ability = random.choice(["wisdom", "intelligence", "charisma"]) # race, background, occupation
    spell_save_dc = 0         # = 8 + prof_bonus + spellcasting ability mod
    spell_attack_bonus = 0    # = prof_bonus + spellcasting ability mod
    spell_slots = {level: 0 for level in range(1, 10)} # race, background, occupation
    known_spells = []         # race, background, occupation
    known_cantrips = []        # race, background, occupation

    # --- Other DM-facing info ---
    passive_perception = 10      # = 10 + WIS mod (+ proficiency if applicable)
    advantage_on = []            # race, background
    disadvantage_on = []         # race, background
    resistances = []             # race, background
    immunities = []              # race
    vulnerabilities = []         # race
    other_physical_features = [] # race
    equipment = []               # occupation, background, wealth level
    overall_cr = 0.125           # manual input or computed later

    # That's the map for modify the base attributes
    # Notes on things to post format: darkvision ?ft, breath hold ? min, armor (light <- medium ecc)
    # Notes on list for post format: random_weapon_list, plantfolk_vulnerability_list, random_tool/kit_list, random_damage_type_list, lycantrope_natural_weapons_list, aasimar_transformation_list, random_skill_list, giant_element_list, draconic_ancestory_list, musical_instrument_list, wizard_cantrip_list, druid_cantrip_list, martial_weapon_list, simple_weapon_list
    # When any list is mentioned, it means that it should be rolled from the items in that list, because the list name is a placeholder.
    modifiers = {
        "race": { # Common elf contains the complete template
            "Common Elf": {
                "core_combat": {
                    "hp": 0,
                    "ac": 0,
                    "initiative": 0,
                    "speed_bonus": {"walking": 0}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "" #basic is medium
                },
                "ability_scores": {
                    "strength": 0,
                    "dexterity": 2,
                    "constitution": 0,
                    "intelligence": 1,
                    "wisdom": 0,
                    "charisma": 0
                },
                "proficiencies": {
                    "weapons": ["longsword","shortsword","longbow","shortbow"],
                    "armors": [],
                    "tools": [],
                    "skills": ["perception"],
                    "saving_throws": []
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "",
                    "spell_slots": {1: 0, 2: 0},
                    "known_spells": [],
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": [],
                    "immunities": ["charmed (magic-induced sleep)"],
                    "vulnerabilities": [],
                    "add_advantage_on": [],
                    "add_disadvantage_on": [],
                    "other_physical_features": ["darkvision 60ft"]
                }
            },
            "Polar Human": {
                "ability_scores": {
                    "strength": 1,
                    "constitution": 1,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["shortsword","spear","harpoon","shortbow"],
                    "armors": ["light armors"],
                    "tools": ["ice fishing tools"],
                    "skills": ["survival","athletics"]
                },
                "other_info": {
                    "resistances": ["cold"]
                }
            },
            "Quarryan Human": {
                "ability_scores": {
                    "dexterity": 1,
                    "intelligence": 1,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["shortsword","light crossbow","flintlock pistol","spear"],
                    "tools": ["navigation tools"],
                    "skills": ["deception","persuasion"]
                }
            },
            "South Herian Human": {
                "ability_scores": {
                    "dexterity": 1,
                    "wisdom": 1,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["longsword","shortsword","longbow","shortbow","rapier"],
                    "armors": ["light armors"],
                    "skills": ["persuasion","insight"]
                }
            },
            "North Herian Human": {
                "ability_scores": {
                    "dexterity": 1,
                    "constitution": 1,
                    "intelligence": 1
                },
                "proficiencies": {
                    "weapons": ["longsword","shortsword","light crossbow","shortbow","hand crossbow"],
                    "tools": ["mason's tools"],
                    "skills": ["history"]
                }
            },
            "Plains Dorojan Human": {
                "ability_scores": {
                    "strength": 1,
                    "constitution": 1,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["longsword","shortsword","longbow","shortbow"],
                    "skills": ["animal handling","survival"]
                }
            },
            "Mountains Dorojan Human": {
                "ability_scores": {
                    "strength": 1,
                    "constitution": 1,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["shortsword","shortbow"],
                    "skills": ["athletics","acrobatics"]
                },
                "other_info": {
                    "resistances": ["cold"]
                }
            },
            "Half-Elf": {
                "ability_scores": {
                    "strength": 1,
                    "dexterity": 1,
                    "charisma": 2
                },
                "proficiencies": {
                    "weapons": ["martial_weapon_list","martial_weapon_list"],
                    "armors": ["light armors"],
                    "skills": ["perception", "random_skill_list"]
                },
                "other_info": {
                    "immunities": ["charmed (magic-induced sleep)"],
                    "other_physical_features": ["darkvision 60ft"]
                }
            },
            "Plasmoid": {
                "ability_scores": {
                    "constitution": 2,
                    "intelligence": 1
                },
                "other_info": {
                    "resistances": ["acid"],
                    "immunities": ["poisoned"],
                    "other_physical_features": ["darkvision 60ft", "breath hold 60 min",
                                                "amorphous form (can squeeze through 1-inch gaps)",
                                                "fatural pseudopods (can manipulate objects without hands)"]
                }
            },
            "Spirit": {
                "ability_scores": {
                    "strength": -1,
                    "dexterity": 1,
                    "wisdom": 2
                },
                "proficiencies": {
                    "weapons": ["scyter","dagger","quarterstaff"],
                    "skills": ["insight","perception"],
                    "saving_throws": ["wisdom"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "wisdom",
                    "known_cantrips": ["druid_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["necrotic"],
                    "vulnerabilities": ["radiant"],
                    "other_physical_features": ["darkvision 60ft, breath hold 10 min",
                                                "incorporeal movement (can move through creatures and objcts as if they're difficult terrain)",
                                                "ethereal sight 60ft",
                                                "spectral sense (sense living creatures within 15ft)"]
                }
            },
            "Lopunnie": {
                "core_combat": {
                    "initiative": 5,
                    "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "dexterity": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","simple_weapon_list"],
                    "skills": ["acrobatics"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft",
                                                "keen hearing",
                                                "keen smell"]
                }
            },
            "Common Birdling": {
                "core_combat": {
                    "speed_bonus": {"walking": 5, "flying": 30} #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "strength": -1,
                    "dexterity": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","simple_weapon_list"],
                    "armors": ["light armors"],
                    "skills": ["perception"]
                },
                "other_info": {
                    "other_physical_features": ["keen sight"]
                }
            },
            "Hybrid": {
                "ability_scores": {
                    "strength": +1,
                    "dexterity": +1,
                    "constitution": +1,
                    "intelligence": +1,
                    "wisdom": +1,
                    "charisma": +1
                },
                "proficiencies": {
                    "skills": ["random_skill_list", "random_skill_list"]
                },
                "other_info": {
                    "other_physical_features": [
                        "adaptive physiology (once per long rest, gain advantage on one saving throw of choice for the day)"
                    ]
                }
            },
            "Other": {
                "ability_scores": {
                    "constitution": +1,
                    "intelligence": +1
                },
                "proficiencies": {
                    "weapons": ["random_weapon_list"],
                    "skills": ["random_skill_list", "random_skill_list"],
                    "tools": ["random_tool/kit_list"]
                },
                "other_info": {
                    "resistances": ["random_damage_type_list"]
                }
            },
            "Dark Elf": {
                "ability_scores": {
                    "dexterity": 2,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["longsword","shortsword","longbow","shortbow"],
                    "skills": ["perception"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["Dancing Lights", "Faerie Fire", "Darkness"]
                },
                "other_info": {
                    "immunities": ["charmed (magic-induced sleep)"],
                    "vulnerabilities": ["sunlight sensitivity"],
                    "other_physical_features": ["darkvision 120ft"]
                }
            },
            "Wood Elf": {
                "core_combat": {
                    "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "dexterity": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["longsword","shortsword","longbow","shortbow"],
                    "skills": ["perception"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["wizard_cantrip_list", "Mask of the Wild"]
                },
                "other_info": {
                    "immunities": ["charmed (magic-induced sleep)"],
                    "other_physical_features": ["darkvision 60ft"]
                }
            },
            "Deep Elf": {
                "ability_scores": {
                    "dexterity": 2,
                    "constitution": 1
                },
                "proficiencies": {
                    "weapons": ["light crossbow","spiked ball and chain"],
                    "skills": ["perception"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "immunities": ["charmed (magic-induced sleep)"],
                    "vulnerabilities": ["sunlight sensitivity"],
                    "other_physical_features": ["darkvision 120ft"]
                }
            },
            "Moonskin Elf": {
                "core_combat": {
                    "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "dexterity": 1,
                    "intelligence": 1
                },
                "proficiencies": {
                    "weapons": ["spear","javelin","longbow","shortbow"],
                    "skills": ["perception"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["druid_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["suffocation"],
                    "immunities": ["charmed (magic-induced sleep)"],
                    "other_physical_features": ["darkvision 60ft", "breath hold 10 min"]
                }
            },
            "Pixie": {
                "core_combat": {
                    "hp": -4,
                    "speed_bonus": {"flying": 30}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "tiny" #basic is medium
                },
                "ability_scores": {
                    "strength": -4,
                    "dexterity": 3,
                    "wisdom": 1,
                    "charisma": 2
                },
                "proficiencies": {
                    "weapons": ["shortsword", "shortbow"],
                    "skills": ["perception", "stealth"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "known_spells": ["invisibility (free 1/day)"],
                    "known_cantrips": ["druidcraft"]
                }
            },
            "Fairy": {
                "core_combat": {
                    "speed_bonus": {"walking": 0}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "small", #basic is medium
                },
                "ability_scores": {
                    "strength": -1,
                    "dexterity": 2,
                    "charisma": 2
                },
                "proficiencies": {
                    "weapons": ["shortsword","shield","shortbow"],
                    "skills": ["persuasion"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "known_spells": ["faerie fire (free 1/day)"],
                    "known_cantrips": ["light"]
                },
                "other_info": {
                    "add_advantage_on": ["charmed (magic-induced sleep)"]
                }
            },
            "Firbolg": {
                "core_combat": {
                    "hp": 4
                },
                "ability_scores": {
                    "strength": 1,
                    "constitution": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","simple_weapon_list","shield"],
                    "skills": ["animal handling"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "wisdom",
                    "known_spells": ["detect magic (free 1/day)", "disguise self (free 1/day)"]
                },
                "other_info": {
                    "immunities": ["charmed (magic-induced sleep)"],
                    "other_physical_features": ["hidden step (free invisibility 1/rest)", "darkvision 60ft"]
                }
            },
            "Elementalfolk": {
                "ability_scores": {
                    "constitution": +2
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["mage armor (free 1/day)"]
                }
            },
            "Sylph": {
                "core_combat": {
                    "speed_bonus": {"walking": 5} #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "dexterity": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","simple_weapon_list"],
                    "skills": ["acrobatics"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "wisdom",
                    "known_spells": ["gust of wind (free 1/day)"],
                    "known_cantrips": ["gust"]
                },
                "other_info": {
                    "resistances": ["thunder", "lightning"],
                    "vulnerabilities": [],
                    "other_physical_features": ["slow fall (reduce fall damage by 20ft)"]
                }
            },
            "Dryad": {
                "ability_scores": {
                    "constitution": 1,
                    "wisdom": 2,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["club","quarterstaff","shortbow"],
                    "skills": ["nature","survival"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "wisdom",
                    "known_spells": ["entangle (free 1/day)"],
                    "known_cantrips": ["druidcraft"]
                }
            },
            "Gnome": {
                "core_combat": {
                    "size": "small", #basic is medium
                },
                "ability_scores": {
                    "dexterity": 1,
                    "intelligence": 2
                },
                "proficiencies": {
                    "tools": ["tinker's tools"],
                    "skills": ["history"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "intelligence",
                    "known_spells": ["detect magic (free 1/day)"],
                    "known_cantrips": ["minor illusion"]
                },
                "other_info": {
                    "immunities": ["charmed (magic-induced sleep)"],
                    "other_physical_features": ["darkvision 60ft"]
                }
            },
            "Dwarf": {
                "core_combat": {
                    "speed_bonus": {"walking": -5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "strength": 1,
                    "constitution": 2
                },
                "proficiencies": {
                    "weapons": ["battleaxe","warhammer","handaxe","shield"],
                    "armors": ["light armors","medium armors"],
                    "tools": ["smith's tools","brewer's supplies","mason's tools"]
                },
                "other_info": {
                    "resistances": ["poison"],
                    "other_physical_features": ["darkvision 60ft"]
                }
            },
            "Tabaxi": {
                "core_combat": {
                    "speed_bonus": {"walking": 10, "climbing": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "dexterity": 2,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["claws"],
                    "skills": ["perception","stealth"]
                },
                "other_info": {
                    "immunities": ["charmed (magic-induced sleep)"],
                    "other_physical_features": ["feline agility (free dash 1/rest)", "darkvision 60ft",
                                                "cat's claws (natural weapons, 1d4 slashing damage)"]
                }
            },
            "Kenku": {
                "ability_scores": {
                    "dexterity": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "tools": ["forgery kit", "disguise kit"],
                    "skills": ["stealth", "sleight of hand"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft", "mimicry"]
                }
            },
            "Goliath": {
                "core_combat": {
                    "hp": 3
                },
                "ability_scores": {
                    "strength": 2,
                    "constitution": 2
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","martial_weapon_list","shield"],
                    "armors": ["light armors", "medium armors"],
                    "skills": ["athletics"]
                },
                "other_info": {
                    "resistances": ["cold"],
                    "other_physical_features": ["stone's endurance (free stone skin 1/rest)"]
                }
            },
            "Beastfolk": {
                "ability_scores": {
                    "strength": 1,
                    "dexterity": 1
                },
                "proficiencies": {
                    "skills": ["perception"]
                },
                "other_info": {
                    "other_physical_features": ["enhanced senses (advantage on perception checks involving smell, sight, or hearing)"]
                }
            },
            "Satyr": {
                "ability_scores": {
                    "dexterity": 2,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["horns"],
                    "tools": ["musical_instrument_list"],
                    "skills": ["performance","persuasion"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "known_spells": ["charm person (free 1/day)"],
                    "known_cantrips": ["minor illusion"]
                },
                "other_info": {
                    "other_physical_features": ["horns (natural weapons, 1d4 bludgeoning damage)"]
                }
            },
            "Bugbear": {
                "core_combat": {
                    "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "strength": 2,
                    "dexterity": 1,
                    "constitution": 1,
                    "intelligence": -1,
                    "charisma": -1
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","martial_weapon_list"],
                    "armors": ["light armors"],
                    "skills": ["intimidation", "stealth"]
                },
                "other_info": {
                    "other_physical_features": ["long-limbed (reach increased by 5ft)",
                                                "sneaky (advantage on stealth checks in dim light or darkness)"]
                }
            },
            "Sentient Construct": {
                "core_combat": {
                    "ac": 2,
                    "speed_bonus": {"walking": -5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "constitution": 2,
                    "intelligence": 1,
                    "wisdom": 0,
                    "charisma": -1
                },
                "proficiencies": {
                    "tools": ["artisan's tools"],
                    "skills": ["arcana"],
                    "saving_throws": []
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "intelligence",
                    "spell_slots": {1: 2, 2: 1},
                    "known_spells": ["mage armor", "shield"],
                    "known_cantrips": ["mending", "mage hand"]
                },
                "other_info": {
                    "resistances": ["poison"],
                    "immunities": ["diseased"],
                    "vulnerabilities": ["cold"],
                    "other_physical_features": ["does not need to eat, drink, breathe, or sleep", "can concentrate on spells even while incapacitated"]
                }
            },
            "Giant": {
                "core_combat": {
                    "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "large", #basic is medium
                },
                "ability_scores": {
                    "strength": 3,
                    "dexterity": -1,
                    "constitution": 2
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","martial_weapon_list"],
                    "armors": ["light armors","medium armors"],
                    "skills": ["athletics"]
                },
                "other_info": {
                    "resistances": ["giant_element_list"],
                    "other_physical_features": ["enlarged reach (reach increased by 5ft)"]
                }
            },
            "Wolfang": {
                "core_combat": {
                    "speed_bonus": {"walking": 5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "strength": 1,
                    "dexterity": 2,
                    "constitution": 1
                },
                "proficiencies": {
                    "weapons": ["claws","bite"],
                    "skills": ["perception", "survival"]
                },
                "other_info": {
                    "resistances": ["diseases"],
                    "other_physical_features": ["darkvision 60ft", "keen hearing", "keen smell",
                                                "pack tactics (advantage on attack rolls against a creature if at least one of your allies is within 5ft of it and isn't incapacitated)",
                                                "natural weapons (claws 1d4 slashing damage, bite 1d6 piercing damage)"]
                }
            },
            "Dragonborn": {
                "ability_scores": {
                    "strength": 2,
                    "constitution": 1
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","martial_weapon_list"]
                },
                "other_info": {
                    "resistances": ["draconic_ancestory_list"],
                    "other_physical_features": ["breath weapon (15ft cone or 30ft line, 2d6 damage, DC 12 dex save for half)"]
                }
            },
            "Half-Dragon": {
                "core_combat": {
                    "ac": 2,
                    "speed_bonus": {"walking": 0, "flying": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "strength": 2,
                    "constitution": 1
                },
                "proficiencies": {
                    "weapons": ["bite"],
                    "skills": ["intimidation"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "immunities": ["draconic_ancestory_list"],
                    "other_physical_features": ["breath weapon (15ft cone or 30ft line, 2d6 damage, DC 12 dex save for half)",
                                                "natural weapons (bite 1d8 piercing damage)"]
                }
            },
            "True Dragon": {
                "core_combat": {
                    "hp": 30,
                    "ac": 3,
                    "speed_bonus": {"walking": 10}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "strength": 1,
                    "constitution": 2,
                    "charisma": 2
                },
                "proficiencies": {
                    "weapons": ["breath weapon","claws","bite"],
                    "skills": ["intimidation","perception"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "known_spells": ["fear (free 1/day)", "telepathy (at will)"]
                },
                "other_info": {
                    "resistances": ["diseases"],
                    "immunities": ["draconic_ancestory_list"],
                    "other_physical_features": ["darkvision 120ft",
                                                "breath weapon (30ft cone or 60ft line, 4d6 damage, DC 15 dex save for half)",
                                                "trasformation (can polymorph into dragonish (and back) form gaining flight 60ft, natural weapons (bite 2d10 piercing damage, claw 2d6 slashing damage))",
                                                "legendary resistance (3/rest, can choose to succeed a failed saving throw)"]
                }
            },
            "Kobold": {
                "core_combat": {
                    "size": "small", #basic is medium
                },
                "ability_scores": {
                    "dexterity": 2,
                    "intelligence": 1
                },
                "proficiencies": {
                    "weapons": ["dagger","sling","shortbow"],
                    "skills": ["random_skill_list"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft",
                                                "pack tactics (advantage on attack rolls against a creature if at least one of your allies is within 5ft of it and isn't incapacitated)",
                                                "sunlight sensitivity"]
                }
            },
            "Lizardfolk": {
                "core_combat": {
                    "ac": 1,
                    "speed_bonus": {"swimming": 30}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "constitution": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["bite","club","javelin","spear"],
                    "skills": ["survival","perception"]
                },
                "other_info": {
                    "other_physical_features": ["breath hold 15 min", "natural weapons (bite 1d6 piercing damage)"]
                }
            },
            "Firefly": {
                "core_combat": {
                    "speed_bonus": {"walking": -10, "flying": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "tiny", #basic is medium
                },
                "ability_scores": {
                    "dexterity": 2,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["sting"],
                    "skills": ["stealth"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "known_spells": ["produce flame (free at will)"],
                    "known_cantrips": ["faerie fire"]
                },
                "other_info": {
                    "resistances": ["fire"],
                    "vulnerabilities": ["cold"],
                    "other_physical_features": ["darkvision 60ft", "bioluminescence (can emit bright light in 10ft radius and dim light for additional 10ft)"]
                }
            },
            "Pale Knight": {
                "core_combat": {
                    "ac": +constitution_mod,
                    "initiative": -dexterity_mod,
                    "speed_bonus": {"walking": -10},  # 20 ft base
                    "size": "small"
                },
                "ability_scores": {
                    "dexterity": -1,
                    "constitution": +2,
                    "intelligence": +1,
                    "wisdom": +1
                },
                "proficiencies": {
                    "weapons": ["dagger", "rapier"],
                    "tools": ["masons_tools"],
                    "skills": ["perception", "deception"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["druid_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["necrotic", "poison"],
                    "add_advantage_on": ["petrified"],
                    "other_physical_features": [
                        "blind (cannot see normally)",
                        "telepathy 60ft (Paladrin only)",
                        "thermal vision 10ft",
                        "dark sustenance (does not need to eat or drink normally)",
                        "mute (doesn't speak normally)"
                    ]
                }
            },
            "Lost Goblin": {
                "core_combat": {
                    "size": "small", #basic is medium
                },
                "ability_scores": {
                    "dexterity": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["shortsword", "shortbow"],
                    "skills": ["insight","intimidation"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft", "nimble escape (can take disengage or hide action as a bonus action on each of its turns)"]
                }
            },
            "Hobgoblin": {
                "ability_scores": {
                    "strength": 1,
                    "constitution": 1,
                    "intelligence": 2
                },
                "proficiencies": {
                    "weapons": ["martial_weapon_list"],
                    "skills": ["history","intimidation"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft", "martial advantage (when it or an ally within 5ft attacks with a martial weapon, can roll with advantage)"]
                }
            },
            "Lost Sea Goblin": {
                "core_combat": {
                    "speed_bonus": {"walking": -5, "swimming": 40}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "small", #basic is medium
                },
                "ability_scores": {
                    "dexterity": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["trident", "shortbow"],
                    "skills": ["athletics", "insight"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "wisdom",
                    "known_spells": ["minor illusion (free 4/day)"]
                    },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft", "breath hold 30 min"]
                }
            },
            "Mushroomfolk": {
                "core_combat": {
                    "speed_bonus": {"walking": -5}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "small", #basic is medium
                },
                "ability_scores": {
                    "constitution": 2,
                    "wisdom": 1
                },
                "proficiencies": {
                    "weapons": ["unarmed strike"],
                    "skills": ["nature", "medicine"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "wisdom",
                    "known_spells": ["fungal spores (free 2/day)"],
                    "known_cantrips": ["druid_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["poison"],
                    "other_physical_features": ["keen smell"]
                }
            },
            "Ogre": {
                "core_combat": {
                    "ac": 2,
                    "speed_bonus": {"walking": 10}, #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                    "size": "large", #basic is medium
                },
                "ability_scores": {
                    "strength": 2,
                    "constitution": 1
                },
                "proficiencies": {
                    "weapons": ["unarmed strike", "greatclub"],
                    "skills": ["intimidation"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft", "powerful build (counts as one size larger for carrying capacity and push/drag/lift)",
                                                "fists of steel (natural weapons, 1d8 bluedgeoning damage)"]
                }
            },
            "Half-Ogre": {
                "ability_scores": {
                    "strength": 2,
                    "constitution": 1
                },
                "proficiencies": {
                    "weapons": ["unarmed strike", "greatclub"],
                    "skills": ["intimidation", "athletics"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft", "powerful build (counts as one size larger for carrying capacity and push/drag/lift)",
                                                "heavy fists (natural weapons, 1d6 bluedgeoning damage)"]
                }
            },
            "Insectoid": {
                "core_combat": {
                    "ac": +3
                },
                "ability_scores": {
                    "dexterity": +2
                },
                "proficiencies": {
                    "skills": ["perception"]
                },
                "other_info": {
                    "other_physical_features": [
                        "darkvision 60ft",
                        "electroreception (sense electrical fields within 30ft)",
                        "compound eyes or mandibles",
                        "insectoid physiology"
                    ]
                }
            },
            "Grung": {
                "core_combat": {
                    "speed_bonus": {"climbing": 25},
                    "size": "small"
                },
                "ability_scores": {
                    "dexterity": +2,
                    "constitution": +1
                },
                "proficiencies": {
                    "skills": ["athletics"]
                },
                "other_info": {
                    "resistances": ["poison"],
                    "immunities": [],
                    "vulnerabilities": [],
                    "add_advantage_on": ["poisoned"],
                    "add_disadvantage_on": [],
                    "other_physical_features": [
                        "amphibious (can breathe air and water)",
                        "poisonous skin (contact poison, DC 12 con save or be poisoned for 1 min)",
                        "standing leap (long jump 25ft, high jump 15ft without run-up)"
                    ]
                }
            },
            "Kling": {
                "core_combat": {
                    "speed_bonus": {"swimming": 20},
                    "size": "small"
                },
                "ability_scores": {
                    "dexterity": +2,
                    "intelligence": +1
                },
                "proficiencies": {
                    "tools": ["tinkers_tools"],
                    "skills": ["sleight_of_hand", "survival"]
                },
                "other_info": {
                    "other_physical_features": [
                        "darkvision 60ft",
                        "amphibious (can breathe air and water)",
                        "scavenger culture (advantage on checks to find usable materials)"
                    ]
                }
            },
            "Halfling": {
                "core_combat": {
                    "speed_bonus": {"walking": -5},
                    "size": "small"
                },
                "ability_scores": {
                    "dexterity": 2,
                    "charisma": 1
                },
                "proficiencies": {
                    "skills": ["stealth"]
                },
                "other_info": {
                    "add_advantage_on": ["frightened"],
                    "other_physical_features": ["lucky (reroll a nat 1 on a d20)", "nimbleness (you can move through a creature bigger than you)"]
                }
            },
            "Orc": {
                "ability_scores": {
                    "strength": 2,
                    "constitution": 1
                },
                "proficiencies": {
                    "weapons": ["greataxe", "javelin"]
                },
                "other_info": {
                    "other_physical_features": ["darkvision 60ft", "powerful build (counts as one size larger for carrying capacity and push/drag/lift"]
                }
            },
            "Plantfolk": {
                "core_combat": {
                    "speed_bonus": {"climbing": 10}
                },
                "ability_scores": {
                    "dexterity": 1,
                    "constitution": 2,
                    "wisdom": 2,
                },
                "proficiencies": {
                    "weapons": ["dagger", "quarterstaff", "sickle"],
                    "tools": ["herbalism kit", "alchemist supplies"],
                    "skills": ["nature", "perception", "survival"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["entangle (free at will)", "goodberry (free 1/day)"],
                    "known_cantrips": ["druidcraft"]
                },
                "other_info": {
                    "resistances": ["poison"],
                    "vulnerabilities": ["plantfolk_vulnerability_list"],
                    "add_advantage_on": ["nature", "herbalism kit", "prone", "stealth (in foliage)"]
                }
            },
            "Tiefling": {
                "ability_scores": {
                    "intelligence": 1,
                    "charisma": 2
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["thaumaturgy"],
                    "known_spells": ["disguise self (free 1/day)", "hellish rebuke (free 1/day)"]
                },
                "other_info": {
                    "resistances": ["fire"],
                    "other_physical_features": ["darkvision 60ft"]
                }
            },
            "Demonoid": {
                "core_combat": {
                    "initiative": +charisma_mod,
                    "speed_bonus": {"flying": 15}
                },
                "ability_scores": {
                    "strength": 1,
                    "dexterity": 1,
                    "constitution": 1,
                    "charisma": 1
                },
                "proficiencies": {
                    "weapons": ["dagger", "longsword", "shortsword"],
                    "skills": ["intimidation", "arcana"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["hellish rebuke (free 1/day)"],
                    "known_cantrips": ["thaumaturgy", "wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["fire"],
                    "other_physical_features": [
                        "demonic heritage (can recall demonic powers, manifests as luminescent horns, wings or tail)",
                        "darkvision 60ft"
                    ]
                },
            },
            "Yuan-Ti": {
                "ability_scores": {
                    "intelligence": 1,
                    "charisma": 2
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["poison spray"],
                    "known_spells": ["suggestion (free 1/day)"]
                },
                "other_info": {
                    "immunities": ["poison"],
                    "other_physical_features": ["darkvision 60ft", "magic resistance (advantage vs spells)"]
                }
            },
            "Demon": {
                "core_combat": {
                    "initiative": +charisma_mod,
                    "speed_bonus": {"flying": 30}
                },
                "ability_scores": {
                    "strength": 2,
                    "charisma": 2
                },
                "proficiencies": {
                    "weapons": ["dagger", "longsword", "shortsword"],
                    "skills": ["intimidation", "arcana"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["darkness (free 1/day)", "teleport (free 1/day)", "hellish rebuke (free 1/day)"],
                    "known_cantrips": ["thaumaturgy", "wizard_cantrip_list", "message"]
                },
                "other_info": {
                    "resistances": ["fire", "cold", "lightning", "force"],
                    "immunities": ["charmed", "frightened"],
                    "vulnerabilities": ["radiant", "necrotic"],
                    "other_physical_features": ["darkvision 120ft",
                                                "regeneration (regain 5 HP at the start of its turn if it has at least 1 HP)",
                                                "demonic taunt (once per turn, can deal extra 7 (2d6) necrotic damage to a creature it hits with a weapon attack)",
                                                "true sight 45ft"]
                }
            },
            "Salamanderman": {
                "core_combat": {
                    "speed_bonus": {"swimming": 20}
                },
                "ability_scores": {
                    "strength": 1,
                    "dexterity": 2,
                },
                "proficiencies": {
                    "weapons": ["dagger", "shortsword"],
                    "skills": ["survival", "nature"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["fire"],
                    "add_advantage_on": ["athletics (when balance is needed)"],
                    "other_physical_features": [
                        "regenerative skin (heals minor wounds faster for 1d4 HP at the start of its turn)",
                        "tail can be used for balance or minor attacks (1d4 bludgeoning)",
                        "darkvision 60ft"
                    ]
                }
            },
            "Oni": {
                "core_combat": {
                    "initiative": +dexterity_mod
                },
                "ability_scores": {
                    "strength": +2,
                    "dexterity": +1,
                    "charisma": +1
                },
                "proficiencies": {
                    "weapons": ["longsword", "katana", "shortsword"],
                    "skills": ["intimidation"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["fire bolt"]
                },
                "other_info": {
                    "resistances": ["fire"],
                    "other_physical_features": [
                        "darkvision 60ft",
                        "horns (natural weapons, 1d6 piercing damage)",
                        "innate flame affinity (fire spells are deep red or purple)"
                    ]
                }
            },
            "Kijin": {
                "core_combat": {
                    "initiative": +dexterity_mod+2,
                    "size": "medium"
                },
                "ability_scores": {
                    "dexterity": +2,
                    "intelligence": +1,
                    "wisdom": +1
                },
                "proficiencies": {
                    "weapons": ["longsword", "katana", "longbow"],
                    "skills": ["arcana"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["mage armor (free at will)", "detect magic (free at will)"],
                    "known_cantrips": ["wizard_cantip_list"]
                },
                "other_info": {
                    "resistances": ["fire"],
                    "other_physical_features": [
                        "darkvision 60ft",
                        "magic vision (can see magic energy and auras)"
                    ]
                }
            },
            "Majin": {
                "core_combat": {
                    "initiative": +dexterity_mod+5,
                    "ac": +constitution_mod
                },
                "ability_scores": {
                    "strength": +2,
                    "dexterity": +2,
                    "charisma": +2
                },
                "proficiencies": {
                    "skills": ["perception", "intimidation"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["mage armor (free at will)", "detect magic (free at will)"],
                    "known_cantrips": ["wizard_cantrip_list", "wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["fire", "necrotic"],
                    "other_physical_features": [
                        "darkvision 60ft",
                        "thermal vision 10ft",
                        "tremorsense 10ft",
                        "heightened senses (advantage on perception checks involving smell, sight, or hearing)",
                        "overwhelming presence (once per day, force all creatures within 30ft that can see you to make a DC 15 wisdom saving throw or be frightened for 1 minute)"
                    ]
                }
            },
            "Strix": {
                "ability_scores": {
                    "intelligence": +2,
                    "wisdom": +1,
                    "constitution": -1
                },
                "proficiencies": {
                    "skills": ["insight", "arcana"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["psychic"],
                    "add_advantage_on": ["charmed", "frightened"],
                    "other_physical_features": [
                        "tentacle manifestation (can grow/absorb grown tentacles from the back)",
                        "grown tentacles can manipulate objects but cannot wield weapons",
                        "self-replication capable (rare, slow process)"
                    ]
                }
            },
            "Nightmare": {
                "core_combat": {
                    "hp": -proficiency_bonus,
                },
                "ability_scores": {
                    "strength": -1,
                    "dexterity": 1,
                    "intelligence": 1,
                    "charisma": 2
                },
                "proficiencies": {
                    "skills": ["deception", "insight"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "spell_slots": {1: 2, 2: 2},
                    "known_spells": ["sleep (free 1/day)", "cause fear (free 1/day)"],
                    "known_cantrips": ["minor illusion", "friendship"]
                },
                "other_info": {
                    "resistances": ["psychic"],
                    "immunities": ["magical sleep"],
                    "add_advantage_on": ["feared"],
                    "other_physical_features": [
                        "shapeshifter (humanoid forms only)",
                        "nightmare induction (creatures that sleep within 30ft may suffer disturbing dreams and not gain benefits of a long rest at your discrection)",
                        "dream-feeding (regain 2d6 hp after inducing a nightmare)"
                    ]
                }
            },
            "Celestial": {
                "core_combat": {
                    "initiative": +wisdom_mod,
                    "speed_bonus": {"flying": 15}
                },
                "ability_scores": {
                    "constitution": 1,
                    "wisdom": 1,
                    "charisma": 2
                },
                "proficiencies": {
                    "weapons": ["simple_weapon_list","martial_weapon_list"],
                    "skills": ["insight"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["cure wounds (free 1/day)", "protection from evil and good (free 1/day)"],
                    "known_cantrips": ["thaumaturgy", "light"]
                },
                "other_info": {
                    "resistances": ["radiant"],
                    "add_advantage_on": ["feared"],
                    "other_physical_features": [
                        "celestial heritage (can manifest wings of light, halo or radiant tail)",
                        "darkvision 60ft"
                    ]
                }
            },
            "Angel": {
                "core_combat": {
                    "hp": +proficiency_bonus*level,
                    "ac": +proficiency_bonus,
                    "speed_bonus": {"flying": 30}
                },
                "ability_scores": {
                    "strength": 2,
                    "constitution": 2,
                    "intelligence": 1,
                    "wisdom": 1,
                    "charisma": 2
                },
                "proficiencies": {
                    "weapons": ["spear", "longsword", "longbow", "simple_weapon_list"],
                    "armors": ["light", "medium", "heavy"],
                    "tools": [],
                    "skills": ["insight", "arcana"],
                    "saving_throws": ["wisdom", "charisma"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["shield of faith (free at will)", "lesser restoration (free 1/day)"],
                    "known_cantrips": ["light", "thaumaturgy", "wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["radiant", "necrotic"],
                    "immunities": ["charmed", "frightened"],
                    "other_physical_features": [
                        "divine regeneration (regain 5 hp at the start of its turn if it has at least 1 hp)",
                        "angelic touch (heals a creature or mends an object for 2d4 + 3 hp as an action)",
                        "darkvision 120ft",
                        "truesight 30ft"
                    ]
                }
            },
            "Aarakocra": {
                "core_combat": {
                    "speed_bonus": {"flying": 50} #it's going to be added to the base speed (walking is 30ft others are 0) of the specified type
                },
                "ability_scores": {
                    "dexterity": 2,
                    "wisdom": 1
                },
                "other_info": {
                    "other_physical_features": ["keen sight (advantage on perception checks that rely on sight)", "talons (natural weapons, 1d4 slashing)"]
                }
            },
            "Aasimar": {
                "ability_scores": {
                    "charisma": +2,
                    "wisdom": +1
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["light"]
                },
                "other_info": {
                    "resistances": ["radiant", "necrotic"],
                    "other_physical_features": [
                        "darkvision 60ft",
                        "celestial legacy (aasimar_transformation_list)"
                    ]
                }
            },
            "Moonling": {
                "core_combat": {
                    "speed_bonus": {"walking": -5},
                    "size": "small"
                },
                "ability_scores": {
                    "strength": -1,
                    "dexterity": +2,
                    "intelligence": +1,
                    "wisdom": +2
                },
                "proficiencies": {
                    "skills": ["survival", "perception"]
                },
                "magic": {
                    "magic_source": None
                },
                "other_info": {
                    "other_physical_features": [
                        "light-perception vision (cannot see shapes or colors, only light intensity; blinded by magical darkness)",
                        "tremorsense 30ft",
                        "magnetic sense 60ft",
                        "keen hunter (advantage on survival checks to track creatures)",
                        "generational grudge (once a Moonling has been harmed by a creature, that creature has disadvantage on charisma checks against Moonlings of the same community)"
                    ]
                }
            },
            "Foxling": {
                "ability_scores": {
                    "dexterity": +2,
                    "charisma": +1
                },
                "core_combat": {
                    "speed": +5
                },
                "proficiencies": {
                    "weapons": ["crossbows", "polearms", "hand fans"],
                    "skills": ["stealth", "insight"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["minor illusion"]
                },
                "other_info": {
                    "senses": ["darkvision 60ft"],
                    "other_physical_features": [
                        "fox senses (recognizes individuals by scent and magical trace)",
                        "heat sensitivity (can detect warm creatures within 10ft)",
                        "natural agility (advantage on dexterity saving throws against effects you can see)"
                    ]
                }
            },
            "Shadowkin": {
                "core_combat": {
                    "ac": +4
                },
                "ability_scores": {
                    "strength": +1,
                    "dexterity": +1,
                    "charisma": +1
                },
                "proficiencies": {
                    "armors": ["light", "medium", "heavy"],
                    "weapons": ["simple_weapon_list","martial_weapon_list","shield"],
                    "skills": ["intimidation"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["necrotic"],
                    "add_advantage_on": ["frightened"],
                    "other_physical_features": [
                        "darkvision 60ft",
                        "armor shell (can inhabit incomplete or abandoned armor that drops if defeated)"
                    ]
                }
            },
            "Wisp": {
                "core_combat": {
                    "ac": +5,
                    "initiative": +2,
                    "speed_bonus": {"flying": 30},
                    "size": "small"
                },
                "ability_scores": {
                    "strength": -2,
                    "dexterity": 2,
                    "constitution": -1,
                    "intelligence": 1,
                    "wisdom": 1,
                    "charisma": 2
                },
                "proficiencies": {
                    "skills": ["arcana", "stealth"],
                    "saving_throws": ["dexterity", "wisdom"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "spell_slots": {1: 2},
                    "known_spells": ["light (free 1/day)", "mage hand (free 2/day)", "minor illusion (free 1/day)"],
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["lightning", "poison"],
                    "vulnerabilities": ["bludgeoning (nonmagical)", "piercing (nonmagical)", "slashing (nonmagical)"],
                    "add_advantage_on": ["stealth (in dim light or darkness)"],
                    "other_physical_features": [
                        "incorporeal form (can pass through small openings, 1 inch wide, cannot wear armor or carry objects)",
                        "glowing body (light radius 10ft, can dim at will)",
                        "possessive ability (can attempt to possess a willing or helpless humanoid once per short rest, duration 1 minute)",
                        "hovering flight (can hover and fly)"
                    ]
                }
            },
            "Voidling": {
                "core_combat": {
                    "speed_bonus": {"walking": -5},
                    "size": "small"
                },
                "ability_scores": {
                    "strength": -2,
                    "dexterity": +2,
                    "intelligence": +1,
                    "charisma": +1
                },
                "proficiencies": {
                    "weapons": ["dagger", "rapier"],
                    "tools": ["tinkers_tools", "jewelers_tools"],
                    "skills": ["stealth"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["wizard_cantrip_list"]
                },
                "other_info": {
                    "resistances": ["necrotic"],
                    "add_disadvantage_on": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"],
                    "other_physical_features": [
                        "darkvision 60ft",
                        "telepathy 60ft (Voshedi only)",
                        "dark sustenance (does not need to eat or drink normally)",
                        "darknesssynthesis (inverted photosynthesis)",
                        "mute (doesn't speak normally)"
                    ]
                }
            },
            "Lycanthrope": {
                "core_combat": {
                    "ac": +2
                },
                "ability_scores": {
                    "strength": +2,
                    "constitution": +1
                },
                "proficiencies": {
                    "skills": ["perception"]
                },
                "other_info": {
                    "resistances": ["bludgeoning (nonmagical)", "piercing (nonmagical)", "slashing (nonmagical)"],
                    "immunities": [],
                    "vulnerabilities": ["silvered weapons"],
                    "add_advantage_on": ["perception (smell)"],
                    "add_disadvantage_on": [],
                    "other_physical_features": [
                        "hybrid nightime transformation (can transform into hybrid form only at night; transformation is more severe the more the moon is visible)",
                        "natural weapons (lycantrope_natural_weapons_list)"
                    ]
                }
            },
            "Sentient Undead": {
                "ability_scores": {
                    "constitution": 2,
                    "intelligence": 1,
                    "charisma": -1
                },
                "proficiencies": {
                    "skills": ["history"]
                },
                "other_info": {
                    "resistances": ["necrotic"],
                    "immunities": ["poison", "disease"],
                    "vulnerabilities": ["radiant"],
                    "add_advantage_on": ["feared"],
                    "add_disadvantage_on": ["charisma checks (dealing with the living)"],
                    "other_physical_features": [
                        "does not need food or air"
                    ]
                }
            },
            "Starborn": {
                "core_combat": {
                    "hp": -proficiency_bonus,
                    "initiative": +proficiency_bonus,
                    "speed_bonus": {"walking": 10, "flying": 20},
                },
                "ability_scores": {
                    "strength": -1,
                    "dexterity": 1,
                    "constitution": -1,
                    "intelligence": 3,
                    "wisdom": 1,
                    "charisma": 3
                },
                "proficiencies": {
                    "skills": ["arcana", "history", "persuasion"],
                    "saving_throws": ["intelligence", "charisma", "constitution"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "spellcasting_ability": "charisma",
                    "spell_slots": {
                        1: 4,
                        2: 3,
                        3: 3,
                        4: 3,
                        5: 3,
                        6: 2,
                        7: 2,
                        8: 2,
                        9: 2
                    },
                    "known_spells": ["wish", "meteor swarm", "plane shift", "disintegrate", "magic missle", "counterspell", "detect magic"],
                    "known_cantrips": ["light", "fire bolt"]
                },
                "other_info": {
                    "resistances": ["radiant", "force"],
                    "immunities": ["diseased", "exhaustion (nonmagical)"],
                    "vulnerabilities": ["psychic"],
                    "other_physical_features": [
                        "stellar core (no need for air, food or sleep)",
                        "energy dependency (at 16 spell slots or less, cannot fly and all the resistances are lost; at 5 spell slots or less gains mortal needs; at 0 suffer from 1d8 + 2 damage for every half hour without sleep)",
                        "slow recharge (regain spell slots only up to the 4th level after a long rest, plus 2 additional slot of the lowest level spent over 5th)",
                        "half-familiar (you can bond with an other humanoid with a ritual: Stellar Covenant, 9th-level transmutation (ritual), Casting Time: 24 hours, Range: Touch, Components: V, S, M (a focus attuned to stellar energy worth at least 10,000 gp, consumed), Duration: Until broken, Description: this ritual forges a one-way metaphysical bond between a Starborn and a single willing creature, designating that creature as the Starborn's Chosen. In exchange of a predefined thing, the Chosen can order the Starborn to act. The pact can be broken by both if one is not fullfilling the pact's terms. The pact is exclusive.)",
                        "loyal bond (can cast spells above the 4th level only for a chosen bonded creature)",
                        "restricted attunement (only one weapon or focus)",
                        "fatigue sensitivity (disadvantage on constitution saving throws against exhaustion effects)",
                        "darkvision 120ft"
                    ]
                }
            },
            "Crystalborn": {
                "core_combat": {
                    "size": "small"
                },
                "ability_scores": {
                    "strength": -2,
                    "constitution": 1,
                    "intelligence": 1,
                    "wisdom": 1,
                    "charisma": 1
                },
                "proficiencies": {
                    "tools": ["artisan_tools"],
                    "skills": ["arcana", "perception"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["light"]
                },
                "other_info": {
                    "resistances": ["psychic"],
                    "vulnerabilities": ["thunder"],
                    "add_advantage_on": ["arcana"],
                    "add_disadvantage_on": ["stealth"],
                    "other_physical_features": [
                        "darkvision 60ft"
                    ]
                }
            },
            "Changeling": {
                "ability_scores": {
                    "charisma": +2,
                    "dexterity": +1
                },
                "proficiencies": {
                    "skills": ["deception"]
                },
                "other_info": {
                    "add_advantage_on": ["deception (related to identity)"],
                    "other_physical_features": [
                        "shapechanger (humanoid appearance only)"
                    ]
                }
            },
            "True Vampire": {
                "core_combat": {
                    "hp": +constitution_mod,
                    "ac": +1,
                    "initiative": +charisma_mod,
                    "speed_bonus": {
                        "walking": +5,
                        "flying": 30
                    }
                },
                "ability_scores": {
                    "strength": +1,
                    "dexterity": +2,
                    "constitution": +1,
                    "charisma": +2
                },
                "proficiencies": {
                    "skills": ["perception", "persuasion"]
                },
                "magic": {
                    "magic_source": None
                },
                "other_info": {
                    "resistances": ["necrotic"],
                    "immunities": ["diseases", "poison", "exhaustion (non-magical)", "aging effects"],
                    "add_advantage_on": ["death effects"],
                    "add_disadvantage_on": ["perception (smell, when garlic is in 5ft)"],
                    "other_physical_features": [
                        "darkvision 120ft",
                        "enhanced senses (advantage on perception checks relying on smell, taste, or hearing)",
                        "no heartbeat",
                        "does not need to breathe",
                        "regeneration (regain hit points equal to proficiency bonus at the start of turn if at least 1 HP and has consumed blood in the last 24 hours)",
                        "phase step (once per short rest, can move through solid objects up to 10ft as difficult terrain)",
                        "flight (hover; cannot wear heavy armor)",
                        "mist form (once per long rest, transform into mist for 1 minute; cannot attack or cast spells, can pass through tiny openings, speed becomes flying 40ft)",
                        "no reflection (mirrors and reflective surfaces do not show the vampire)"
                    ]
                }
            },
            "Spectre": {
                "core_combat": {
                    "hp": -proficiency_bonus,
                    "speed_bonus": {"flying": 30}
                },
                "ability_scores": {
                    "strength": -2,
                    "dexterity": 1,
                    "constitution": -2,
                    "intelligence": 1,
                    "wisdom": 1,
                },
                "proficiencies": {
                    "skills": ["perception", "stealth"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["thaumaturgy"]
                },
                "other_info": {
                    "resistances": ["necrotic", "psychic"],
                    "immunities": ["poison", "diseased", "poisoned"],
                    "vulnerabilities": ["radiant"],
                    "add_advantage_on": ["stealth"],
                    "other_physical_features": [
                        "incorporeal movement (can move through solid objects as if they're difficult terrain)",
                        "darkvision 60ft"
                    ]
                }
            },
            "Triton": {
                "core_combat": {
                    "speed_bonus": {"swimming": 30}
                },
                "ability_scores": {
                    "strength": +1,
                    "constitution": +1,
                    "charisma": +1
                },
                "proficiencies": {
                    "weapons": ["trident", "spear"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["fog cloud (free 1/day)"]
                },
                "other_info": {
                    "resistances": ["cold"],
                    "other_physical_features": [
                        "amphibious (breathe air and water)",
                        "aquatic adaptation (water contact reveals scale skin, gills, webbed fingers/toes)",
                        "darkvision 60ft"
                    ]
                }
            },
            "Mermaid": {
                "core_combat": {
                    "speed_bonus": {"walking": -20, "swimming": 45}
                },
                "ability_scores": {
                    "constitution": 1,
                    "charisma": 2
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_cantrips": ["shape water"],
                    "known_spells": ["water breathing (free at will)"]
                },
                "other_info": {
                    "other_physical_features": ["amphibious (breath air and water)"]
                }
            },
            "Nymph": {
                "ability_scores": {
                    "wisdom": 1,
                    "charisma": 2
                },
                "proficiencies": {
                    "saving_throws": ["dexterity"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["charm person (free 3/day)", "entangle (free at will)"]
                },
                "other_info": {
                    "add_advantage_on": ["charmed"]
                }
            },
            "Turtoid": {
                "core_combat": {
                    "ac": +1,
                    "initiative": -dexterity_mod,
                    "speed_bonus": {"walking": -5, "swimming": 15}
                },
                "ability_scores": {
                    "dexterity": -1,
                    "constitution": 2,
                    "wisdom": 1,
                },
                "proficiencies": {
                    "weapons": ["club", "spear"],
                    "skills": ["survival"],
                },
                "other_info": {
                    "resistances": ["cold"],
                    "add_advantage_on": ["strength (carrying or pushing)"],
                    "add_disadvantage_on": ["dexterity saving throws"],
                    "other_physical_features": [
                        "tough shell (can retract as a bonus action to increase AC by 3)",
                        "natural swimmer (can hold breath for 15 minutes)"
                    ]
                }
            },
            "Gooba": {
                "core_combat": {
                    "speed_bonus": {"walking": -10, "swimming": 30}
                },
                "ability_scores": {
                    "dexterity": +2,
                    "constitution": +2,
                    "intelligence": +1,
                    "charisma": -1
                },
                "proficiencies": {
                    "skills": ["stealth", "athletics"]
                },
                "magic": {
                    "magic_source": None
                },
                "other_info": {
                    "add_disadvantage_on": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"],
                    "other_physical_features": [
                        "amphibious (can breathe air and water)",
                        "dehydration weakness (after 24 hours without at least 2 hours submerged in water, gain one level of exhaustion per day)",
                        "tentacular limbs (can interact with objects, grapple, or climb using tentacles; advantage on grapple checks)",
                        "chromatic shift (can change skin color briefly; gains advantage on stealth checks)",
                        "ink burst (once per short rest, release ink in a 10ft radius underwater, heavily obscured for 1 minute)",
                        "darkvision 60ft"
                    ]
                }
            },
            "Banshee": {
                "core_combat": {
                    "speed_bonus": {"flying": 30}
                },
                "ability_scores": {
                    "strength": -1,
                    "constitution": -1,
                    "wisdom": 1,
                    "charisma": 3
                },
                "proficiencies": {
                    "skills": ["intimidation", "performance"]
                },
                "magic": {
                    "magic_source": "Innate",
                    "known_spells": ["fear (free 1/day)", "silent image (free 1/day)"],
                    "known_cantrips": ["vicious mockery"]
                },
                "other_info": {
                    "resistances": ["necrotic", "psychic"],
                    "immunities": ["poison", "charmed", "poisoned", "frightened"],
                    "vulnerabilities": ["radiant"],
                    "add_advantage_on": ["intimidation"],
                    "add_disadvantage_on": ["concentration (for maintaining spells)"],
                    "other_physical_features": [
                        "incorporeal movement (can move through solid objects as if they're difficult terrain)",
                        "wail resonance (once per long rest, emit a wail causing all creatures within 30ft to make a DC 15 constitution saving throw or take 4d6 psychic damage and be frightened for 1 minute; half damage and no fright on successful save)",
                        "darkvision 60ft"
                    ]
                }
            }
        },
        "subtype_modifiers": {
            "Shell": {
                "other_info": {
                    "resistances": ["force"],
                    "other_physical_features": [
                        "shell recall (1/day, grant temporary protection: any creature within 10ft gain 1d8 temporary hp for the next turn if starts the turn there)"
                    ]
                }
            },
            "Lush": {
                "ability_scores": {
                    "charisma": 1
                },
                "other_info": {
                    "resistances": ["poison"],
                    "other_physical_features": [
                        "lush recall (1/day, restore vitality in area: any object suffers from mending effect, every creature heal for 1d4 hp if starts the turn there)"
                    ]
                }
            },
            "Grace": {
                "ability_scores": {
                    "wisdom": 1,
                    "constitution": 1
                },
                "other_info": {
                    "resistances": ["cold"],
                    "other_physical_features": [
                        "frost aura (standing still, can freeze up surroundings, up to freezing water and brittle metal in a 5ft radius, 1/day)"
                    ]
                }
            },
            "Ghost": {
                "core_combat": {
                    "hp": -proficiency_bonus,
                    "initiative": +proficiency_bonus,
                    "speed_bonus": {"flying": 30}
                },
                "ability_scores": {
                    "strength": -3,
                    "dexterity": 2,
                    "constitution": -3,
                    "intelligence": 1,
                    "wisdom": 1,
                    "charisma": 1
                },
                "other_info": {
                    "resistances": ["necrotic", "nonmagical weapons"],
                    "vulnerabilities": ["radiant"],
                    "other_physical_features": [
                        "incorporeal movement (can move through objects as if they're difficult terrain)",
                        "cannot wear armor"
                    ]
                }
            },
            "Skeleton": {
                "ability_scores": {
                    "strength": -1,
                    "dexterity": 2,
                    "constitution": -1,
                    "charisma": -1
                },
                "other_info": {
                    "resistances": ["piercing"],
                    "vulnerabilities": ["bludgeoning"],
                    "other_physical_features": [
                        "does not bleed"
                    ]
                }
            },
            "Zombie": {
                "core_combat": {
                    "hp": +constitution_mod,
                    "initiative": -dexterity_mod,
                    "speed_bonus": {"walking": -5}
                },
                "ability_scores": {
                    "strength": 1,
                    "dexterity": -2,
                    "constitution": 2,
                    "intelligence": -1,
                    "charisma": -1
                },
                "other_info": {
                    "vulnerabilities": ["fire"],
                    "other_physical_features": [
                        "relentless endurance (first time reduced to 0 hp, drop to 1 instead, once per long rest)"
                    ]
                }
            },
            "Cerberian": {
                "ability_scores": {"strength": 1, "constitution": 1},
                "other_info": {
                    "other_physical_features": [
                        "heat aura (standing still, can warm surroundings, up to melting metal in a 5ft radius, 1/day)"
                    ]
                }
            },
            "Blood Beat": {
                "ability_scores": {"charisma": 2},
                "other_info": {
                    "other_physical_features": [
                        "blood manipulation (can control blood in a small area, up to 15ft radius, 1/day)"
                    ]
                }
            },
            "Wither": {
                "ability_scores": {"wisdom": 1, "constitution": 1},
                "other_info": {
                    "other_physical_features": [
                        "life drain (1/day, can recall powers to drain life in a area of 10ft radius: any creature that starts its turn there takes 1d4 necrotic damage and you heal for half the amount)"
                    ]
                }
            },
            "Steam": {
                "ability_scores": {
                    "constitution": +1,
                    "wisdom": +1
                },
                "other_info": {
                    "resistances": ["fire"],
                    "add_advantage_on": ["concentration (for maintaining spells)"],
                    "other_physical_features": [
                        "obscuring mist (can lightly obscure a 10ft radius once per long rest)"
                    ]
                }
            },
            "Dust": {
                "ability_scores": {
                    "dexterity": +2
                },
                "other_info": {
                    "resistances": ["poison"],
                    "other_physical_features": [
                        "dust cloud body (can impose disadvantage on one ranged attack against you per short turn)"
                    ]
                }
            },
            "Smoke": {
                "ability_scores": {
                    "dexterity": +1,
                    "charisma": +1
                },
                "other_info": {
                    "resistances": ["fire"],
                    "other_physical_features": [
                        "smoky form (can lightly obscure a 5ft radius around self)",
                        "choking presence (creatures adjacent have disadvantage on perception checks relying on sight)"
                    ]
                }
            },
            "Lava": {
                "ability_scores": {
                    "strength": +1,
                    "charisma": +1
                },
                "core_combat": {
                    "ac": +constitution_mod
                },
                "proficiencies": {
                    "skills": ["intimidation"]
                },
                "other_info": {
                    "resistances": ["fire"],
                    "other_physical_features": [
                    ]
                }
            },
            "Ice": {
                "ability_scores": {
                    "dexterity": +1
                },
                "other_info": {
                    "immunities": ["cold"],
                    "vulnerabilities": ["fire"],
                    "other_physical_features": [
                        "frozen skin (creatures grappling you take 1 cold damage per round)"
                    ]
                }
            },
            "Mud": {
                "ability_scores": {
                    "constitution": +1,
                    "strength": +1
                },
                "core_combat": {
                    "speed_bonus": {"walking": -10}
                },
                "other_info": {
                    "resistances": ["poison"],
                    "add_advantage_on": ["poisoned", "prone"],
                    "other_physical_features": [
                        "difficult terrain affinity (ignores non-magical mud-based difficult terrain)"
                    ]
                }
            },
            "Earth": {
                "ability_scores": {
                    "strength": +1
                },
                "proficiencies": {
                    "skills": ["animal handling", "nature"]
                },
                "other_info": {
                    "resistances": ["poison"],
                    "other_physical_features": [
                        "tremorsense 10ft"
                    ]
                }
            },
            "Wind": {
                "ability_scores": {
                    "dexterity": +1
                },
                "core_combat": {
                    "speed_bonus": {"walking": +5}
                },
                "other_info": {
                    "resistances": ["force"],
                    "vulnerabilities": ["bludgeoning"],
                    "other_physical_features": [
                        "flickering form (disadvantage on opportunity attacks against you)",
                        "lightweight body (can hover 5ft off the ground)"
                    ]
                }
            },
            "Fire": {
                "ability_scores": {
                    "charisma": +1
                },
                "other_info": {
                    "immunities": ["fire"],
                    "vulnerabilities": ["cold"],
                    "other_physical_features": [
                        "heated body (you illuminate a 5ft radius with bright light and an additional 5ft with dim light)"
                    ]
                }
            },
            "Water": {
                "ability_scores": {
                    "wisdom": +1
                },
                "core_combat": {
                    "speed_bonus": {"swimming": 30}
                },
                "other_info": {
                    "resistances": ["cold"],
                    "add_advantage_on": ["stealth (if underwater)"],
                    "other_physical_features": [
                        "amphibious (air and water breathing)",
                        "darkvision 60ft"
                    ]
                }
            },
            "Flying Mantis": {
                "core_combat": {
                    "speed_bonus": {"flying": 20}
                },
                "ability_scores": {
                    "strength": +1
                },
                "other_info": {
                    "other_physical_features": [
                        "acid production (natural acid secretion)",
                        "sharp forelimbs (1d6 slashing damage)"
                    ]
                }
            },
            "Hornet": {
                "core_combat": {
                    "speed_bonus": {"flying": 30}
                },
                "ability_scores": {
                    "constitution": +1
                },
                "other_info": {
                    "other_physical_features": [
                        "honey production",
                        "natural stinger (1d4 piercing + poison)"
                    ]
                }
            },
            "Bumblebee": {
                "core_combat": {
                    "speed_bonus": {"flying": 25}
                },
                "ability_scores": {
                    "constitution": +2
                },
                "other_info": {
                    "other_physical_features": [
                        "honey production",
                        "robust build (resistance to bludgeoning damage)"
                    ]
                }
            },
            "Fly": {
                "core_combat": {
                    "speed_bonus": {"flying": 35},
                    "size": "small"
                },
                "ability_scores": {
                    "dexterity": +1
                },
                "other_info": {
                    "other_physical_features": [
                        "erratic flight (advantage on dexterity saves vs effects)"
                    ]
                }
            },
            "Cockroacher": {
                "ability_scores": {
                    "constitution": +2
                },
                "other_info": {
                    "resistances": ["poison"],
                    "other_physical_features": [
                        "limited flight (can glide up to 20ft)",
                        "extreme survivability (once per long rest, can drop to 0 hp and stabilize automatically)"
                    ]
                }
            },
            "Antsyote": {
                "core_combat": {
                    "ac": +constitution_mod
                },
                "ability_scores": {
                    "strength": +2
                },
                "other_info": {
                    "other_physical_features": [
                        "hive coordination (advantage on checks when allies are nearby)"
                    ]
                }
            },
            "Ladybudger": {
                "core_combat": {
                    "speed_bonus": {"flying": 20}
                },
                "ability_scores": {
                    "constitution": +1,
                    "wisdom": +1
                },
                "other_info": {
                    "resistances": ["poison"],
                    "other_physical_features": [
                        "aposematic coloration (bright warning colors)",
                        "defensive secretions (creatures that grapple you have disadvantage on ability checks)",
                        "fortune symbol (once per day, you can reroll a failed saving throw for yourself or an ally within 10ft)"
                    ]
                }
            },
            "Mothyel": {
                "core_combat": {
                    "speed_bonus": {"flying": 35}
                },
                "ability_scores": {
                    "dexterity": +1,
                    "charisma": +1
                },
                "other_info": {
                    "add_disadvantage_on": ["perception (sight, under direct sunlight)", "attack rolls (if sight is needed under direct sunlight)"],
                    "other_physical_features": [
                        "nocturnal affinity (advantage on perception checks in dim light or darkness relying on sight)",
                        "powdered wings (can shed scales to escape grapples once per short rest)"
                    ]
                }
            },
            "Bebeesner": {
                "ability_scores": {
                    "dexterity": +2
                },
                "core_combat": {
                    "speed_bonus": {"walking": 5, "climbing": 25},
                    "size": "small"
                }
            },
            "Dawg": {
                "ability_scores": {
                    "strength": +1,
                    "charisma": +1
                },
                "proficiencies": {
                    "skills": ["athletics"]
                },
                "other_info": {
                    "other_physical_features": [
                        "canine loyalty (advantage on saving throws against being frightened when an ally is within 5ft)",
                        "playful demeanor (advantage on charisma checks when interacting with children and animals)",
                        "keen smell (advantage on perception checks that rely on smell)"
                    ]
                }
            },
            "Crimson Devil": {
                "ability_scores": {
                    "strength": +1,
                    "charisma": +2
                },
                "proficiencies": {
                    "skills": ["intimidation"]
                },
                "other_info": {
                    "add_advantage_on": ["death effects"],
                    "other_physical_features": [
                        "small horns (1d4 piercing damage, light, versatile)"
                    ]
                }
            },
            "Light Blue Devil": {
                "ability_scores": {
                    "wisdom": +2,
                    "charisma": +1
                },
                "proficiencies": {
                    "skills": ["insight"]
                },
                "other_info": {
                    "add_advantage_on": ["death effects"],
                    "other_physical_features": [
                        "small horns (1d4 piercing damage, light, versatile)"
                    ]
                }
            },
            "Jaguarfolk": {
                "ability_scores": {
                    "strength": +2,
                    "dexterity": +1
                },
                "core_combat": {
                    "speed_bonus": {"walking": 5, "climbing": 30, "swimming": 25}
                },
                "other_info": {
                    "other_physical_features": [
                        "powerful build (carries/pushes as one size larger)",
                        "predatory instincts (advantage on perception and survival checks related to hunting/tracking)",
                        "silent movement"
                    ]
                }
            },
            "Onicronimb": {
                "ability_scores": {
                    "dexterity": +2,
                    "constitution": +1
                },
                "other_info": {
                    "resistances": ["cold", "fire"],
                    "other_physical_features": [
                        "jumping spider heritage (can jump up to 30ft horizontally and 15ft vertically)",
                        "wall-climbing (can climb difficult surfaces, including upside down on ceilings, without needing to make an ability check)"
                    ]
                }
            },
            "Octolen": {
                "ability_scores": {
                    "constitution": +2,
                    "intelligence": +1
                },
                "other_info": {
                    "other_physical_features": [
                        "tentacled lower body (can use tentacles for manipulation and movement)",
                        "amphibious (breath air and water)",
                        "ink secretion (can release ink to obscure vision in a 10ft radius once per short rest)"
                    ]
                }
            },
            "Browish": {
                "core_combat": {
                    "ac": +2,
                    "size": "large"
                },
                "ability_scores": {
                    "strength": +2,
                    "constitution": +1
                },
                "other_info": {
                    "resistances": ["cold"]
                }
            },
            "Skullywag": {
                "ability_scores": {
                    "dexterity": +1,
                    "charisma": +1
                },
                "proficiencies": {
                    "skills": ["performance", "sleight of hand"],
                    "tools": ["disguise kit"],
                    "armors": ["light"]
                }
            },
            "Other": {
                "ability_scores": {
                    "constitution": +1
                },
                "proficiencies": {
                    "weapons": ["random_weapon_list"],
                    "skills": ["random_skill_list"]
                }
            }
        },
        "age_category": {
            "child": {"strength": +1},
            "teen": {"wisdom": +2, "speed": -5},
            "adult": {"dexterity": +2},
            "middle-aged": {"dexterity": +2},
            "elderly": {"dexterity": +2}
        },
        "occupation": {
            "Farmer/Field Worker": {"dexterity": +2},
            "Unemployed": {"dexterity": +2}
        },
        "backstory_seed": {
            "Runaway noble child": {"dexterity": +2},
            "Former slave": {"dexterity": +2}
        },
        "wealth": {
            "Royal": {"dexterity": +2},
            "Noble": {"dexterity": +2},
            "Commoner": {"dexterity": +2},
            "Peasant": {"dexterity": +2},
            "Slave": {"dexterity": +2}
        }       
    }

    def set_core_combat_mod(self, hp, ac, initiative, speed, level, size, proficiency_bonus, strenght):
        return
    
    def get_ability_scores_mod(self, modifiers):
        return
    def update_ability_mods(self, strenght, dexterity, constitution, intelligence, wisdom, charisma):
        return
    def set_ability_scores(self, strenght, strenght_mod, dexterity, dexterity_mod, constitution, constitution_mod, intelligence,
                           intelligence_mod, wisdom, wisdom_mod, charisma, charisma_mod):
        return
    

    def set_proficiencies(self, weapons, armor, tools, skills, saving_throws):
        return
    

    def set_other_dm_facing_info(self, passive_perception, advantage_on, disadvantage_on, resistances, immunities,
                        vulnerabilities, other_physical_features, equipment, overall_cr):
        return
    

    def apply_modifiers(self, hp, ac, initiative, speed, level, size, proficiency_bonus, strenght, strenght_mod, dexterity, dexterity_mod,
                        constitution, constitution_mod, intelligence, intelligence_mod, wisdom, wisdom_mod, charisma, charisma_mod, weapons,
                        armor, tools, skills, saving_throws, passive_perception, advantage_on, disadvantage_on, resistances, immunities,
                        vulnerabilities, other_physical_features, equipment, overall_cr):
        return
        

    def generate_npc(self):
        race = self.choose_race(self.races)
        language = self.pick_languages(race)
        gender = self.choose_gender(self.genders, race)
        name = self.generate_npc_name(race)
        backstory_seed = random.choice(self.backstory_seeds)
        social_level = self.choose_social_level(self.social_levels)
        age_category, age = self.generate_age_and_category(race)
        occupation = self.generate_occupation(social_level, age_category)
        wealth = self.generate_wealth(social_level)
        partnership = self.generate_partnership(age_category)
        offsprings = self.generate_num_descendants(age_category, partnership)
        personality_traits = self.generate_personality_traits(self.personality_traits_count)
        alignment = self.infer_alignment_from_personality(personality_traits)
        reputation = self.infer_reputation_from_personality(personality_traits)
        backstory = self.generate_backstory(backstory_seed, name, age_category, race)
        subtype = self.conditional_choose_subtype(self.available_subtypes, race)







        return NPC(name, gender, race, subtype, language, occupation, age_category, age, alignment, partnership, personality_traits, offsprings, reputation, wealth, backstory_seed, social_level, backstory)





#Main execution
if __name__ == "__main__":
    gen = NPCGenerator()
    npc = gen.generate_npc()
    print(npc)


"""
idk = [
    ("Polar Human",100), ("Quarryan Human", 200)
    ]

#One time usable tool
if __name__ == "__main__":
    # Prints idk, copy and paste here the list you want to normalize
    
    
    # Step 1: normalize
    total_weight = sum(weight for _, weight in idk)
    normalized_idk = [(name, weight / total_weight) for name, weight in idk]

    # Step 2: print normalized list (copy-paste ready)
    for name, weight in normalized_idk:
        print(f'("{name}", {weight:.4f}),')
"""