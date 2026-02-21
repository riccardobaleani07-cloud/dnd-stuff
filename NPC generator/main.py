from npc_generation.NPC_generator_yay import NPCGenerator

#Main execution
if __name__ == "__main__":
    gen = NPCGenerator()
    npc = gen.generate_npc()
    print(npc)