from npc_static_data.enums import Size, SocialLevel, Wealth

# This file contains data for npc generation

#lists needed for backstory generation
#backstory seeds are the main theme that will be used to generate the backstory
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
#flavour is used to choose the main template for the backstory
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
#backstory basic templates, to be filled
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
#random things that could be called in backstory templates
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
#filling used for the basic templates, to be called in the backstory generation
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

    # Map

#list of races and their probability. do not touch without caring of normalization
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

#lists of subtypes. you can add any list, but make sure to update the available_subtypes list
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
#list of subtype lists that can be called
available_subtypes = [("Insectoid", insectoid_subtypes),
                        ("Beastfolk", beastfolk_subtypes),
                        ("Elementalfolk", elementalfolk_subtypes),
                        ("Demonoid", demonoid_subtypes),
                        ("Sentient Undead", sentient_undead_subtypes),
                        ("Celestial", celestial_subtypes)]

#genders generation. you can modify this list, but only after understanding the logic behind the generation itself
genders = ["Male", "Female", "Lost", "Androgine"]
#to understand the following map you might want to check the gender generation logic
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

#age and age category
#age categories and their ranges for each race. you can modify the list, but consistenly, and in accordion with race availables
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

#partnership status. you can modify the list, but do not add age categories unless you know what you're doing
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

#offspring generation. random.triangular distribution settings for the number of offsprings
distribution_settings = {
    # Distribution settings, negative values allowed for low end to simulate no descendants
    "child": (0, 0, 0),
    "teen": (-19, 1, -9),
    "adult": (-2, 4, 1),
    "middle-aged": (-4, 6, 2),
    "elderly": (-1, 10, 3)
}

#occupation generation
# Dictionary of occupations by social level with their selection probabilities
occupations_by_social = {
    SocialLevel.ROYAL: {"Monarch": 0.05, "Prince/Princess": 0.1, "High Diplomat": 0.25, "Chancelor": 0.05, "Chamberlain": 0.05, "General": 0.15, "High Priest": 0.05, "Royal Advisor": 0.2, "Exotic": 0.1},
    SocialLevel.NOBLE: {"Lord/Lady": 0.05, "Knight": 0.06, "Merchant Lord": 0.12, "Politician": 0.02, "Judge": 0.02, "Guildmaster": 0.05, "Cleric/Bishop": 0.01, "Temple Keeper": 0.01, "Archmage": 0.01, "Architect": 0.06, "Engineer": 0.06, "Historian": 0.05, "Cartographer": 0.03, "Explorer": 0.04, "Entrepreneur": 0.08, "Ship Captain/Admiral": 0.02, "Banker": 0.06, "Noble Hunter/Falconer": 0.01, "Artist": 0.02, "Patron of the Arts": 0.06, "Specialised Doctor": 0.06, "Exotic": 0.1},
    SocialLevel.COMMONER: {"Farmer": 0.065, "Blacksmith": 0.025, "Healer": 0.005, "Soldier": 0.08, "Merchant": 0.08, "Bard": 0.005, "Builder/Site Manager": 0.09, "Tailor/Leatherworker": 0.03, "Innkeeper": 0.04, "Cook": 0.02, "Brewer": 0.005, "Apothecary": 0.025, "Priest/Monk": 0.01, "Bard/Entertainer": 0.02, "Fisher": 0.08, "Sailor": 0.02, "Dockworker": 0.02, "Miner": 0.02, "Librarian": 0.01, "Hunter": 0.05, "Teacher/Tutor": 0.03, "Adventurer/Mercenary": 0.08, "Beggar/Vagrant": 0.03, "Artist": 0.01, "Explorer": 0.05, "Cartographer": 0.01, "Mage": 0.005, "Courier": 0.015, "Waiter": 0.05, "Doctor": 0.04, "Nurse": 0.01, "Exotic": 0.08},
    SocialLevel.PEASANT: {"Farmer/Field Worker": 0.8, "Shepherd": 0.08, "Laborer": 0.05, "Fisher": 0.1, "Servant/Housemaid": 0.05, "Peddler": 0.04, "Tinker": 0.02, "Stablehand": 0.01, "Nurse": 0.06, "Soldier": 0.1, "Monk": 0.07, "Beggar/Vagrant": 0.03, "Dockworker": 0.01, "Miner": 0.08, "Performer": 0.05, "Sailor": 0.05, "Hunter": 0.02, "Waiter": 0.04, "Exotic": 0.05},
    SocialLevel.SLAVE: {"Laborer": 0.15, "Domestic Servant": 0.15, "Field Worker": 0.3, "Pleasure Performer": 0.1, "Tinker": 0.02, "Miner": 0.1, "Performer": 0.03, "Exotic": 0.05}
}
# Dictionary of exotic occupations and their selection probabilities for NPCs with "Exotic" jobs
exotic = {"Monster Hunter": 0.05, "Witch/Warlock": 0.03, "Necromancer": 0.02, "Oracle/Dream Interpreter": 0.05, "Beast Tamer": 0.05, "Familiar Keeper": 0.02, "Artifact Collector": 0.05, "Inventor": 0.02, "Pirate": 0.02, "Gravekeeper": 0.01, "Assassin/Spy": 0.02, "Magical Item Broker": 0.12, "Rune Engraver/Enchanter": 0.1, "Wyvern Keeper": 0.02, "Demonologist": 0.01, "Traveler": 0.1, "Elemental Binder": 0.01, "Chronomancer": 0.01, "Portal Keeper": 0.04, "Astrologer": 0.02, "Vet/Beasts' Doctor": 0.04, "Arms Dealer/Drug Dealer": 0.06, "Slave Trader": 0.08, "Mafia Boss": 0.01, "Gangster": 0.03, "Other": 0.03}
# Definition of employment stage weights based on age category
age_weights = {
    "child": {"Unemployed": 0.55, "Apprentice/Student": 0.45},
    "teen": {"Unemployed": 0.15, "Apprentice/Student": 0.6, "Minor Worker": 0.2, "Full-time Occupation": 0.05},
    "adult": {"Full-time Occupation": 0.6,"Unemployed": 0.15, "Minor Worker": 0.2, "Apprentice/Student": 0.05},
    "middle-aged": {"Full-time Occupation": 0.6,"Unemployed": 0.15, "Minor Worker": 0.25},
    "elderly": {"Retired": 0.5, "Advisor": 0.3, "Minor Duties": 0.3}
}

#social level generation: social levels and their probabilities. if you modify this you need to normalise the list
social_levels = [(SocialLevel.ROYAL, 0.01), (SocialLevel.NOBLE, 0.14), (SocialLevel.PEASANT, 0.30), (SocialLevel.COMMONER, 0.35), (SocialLevel.SLAVE, 0.2)]

#wealth generation
wealth_ranges = {
SocialLevel.ROYAL: (3, 5),
SocialLevel.NOBLE: (2, 5),
SocialLevel.COMMONER: (1, 3),
SocialLevel.PEASANT: (1, 3),
SocialLevel.SLAVE: (1, 2),
}

#personality traits list. do not touch it because it has following logic
default_traits = [
    "Brave", "Cautious", "Curious", "Loyal", "Greedy", "Honest", "Deceptive",
    "Charismatic", "Impulsive", "Reserved", "Ambitious", "Lazy", "Friendly",
    "Temperamental", "Righteous", "Sarcastic", "Arrogant", "Protective", "Dreamy",
    "Pessimistic", "Cheerful", "Brooding", "Stoic", "Generous", "Vindictive", "Adventurous",
    "Meticulous", "Reckless", "Optimistic", "Skeptical", "Compassionate", "Calculating",
    "Patient", "Hot-headed", "Wise", "Naive", "Cynical", "Romantic", "Pragmatic", "Stubborn",
    "Ruthless", "Manipulative", "Hypercritical", "Obsessive", "Cruel", "Fanatical",
    "Jealous", "Crazy", "Eccentric"]

#alignment generation. you can add only existing traits. to keep a trait "neutral" just don't add it to either list
# Simple heuristic: count good vs evil traits
good_traits = {"Brave", "Loyal", "Honest", "Friendly", "Righteous", "Protective", "Generous", "Compassionate", "Wise", "Patient", "Optimistic"}
evil_traits = {"Greedy", "Deceptive", "Arrogant", "Vindictive", "Calculating", "Cynical", "Manipulative", "Ruthless", "Cruel", "Obsessive", "Fanatical"}
# Simple heuristic: count lawful vs chaotic traits
lawful_traits = {"Cautious", "Loyal", "Honest", "Reserved", "Meticulous", "Patient", "Wise", "Pragmatic", "Righteous", "Calculating", "Stoic", "Obsessive"}
chaotic_traits = {"Impulsive", "Temperamental", "Reckless", "Adventurous", "Dreamy", "Romantic", "Hot-headed", "Stubborn", "Curious", "Crazy", "Eccentric", "Jealous"}

#reputation generation... that's a mess
#some reputations are set to 1 to give a default ones, but they can be modified. make sure to keep at least one that has a non 0 value
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
        # List of reputation types and their initial scores
    # All reputation types are initialized to 0 except "Lightly Noticeable" and "Unknown", which start at 1 to ensure every NPC has a standard valid reputation.
#each reputation type will be modified by traits according to the trait_to_reputation dictionary
reputation_types = {"Lovely": 0, "Respectful": 0, "Honorable": 0, "Trustworthy": 0, "Valuable": 0, "Unknown": 0, "Mysterious": 0,
                    "Lightly Noticeable": 1, "Fearsome": 0, "Loathsome": 0, "Unreliable": 0, "Ruthless": 0, "Disgraceful": 0,
                    "Cunning": 0, "Ambiguous": 0,"Infamous": 0, "Bearable": 1, "Edgy": 0, "Charming": 0, "Dull": 0}

#name generation
# Race → flavour mapping. can be changed at will, but make sure every race has a legitimate flavour assigned
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

#language pick
# Race → native language mapping. that's the list of native language per race... to actually modify that list you need to modify the npc_static_data/languages_matrix
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


