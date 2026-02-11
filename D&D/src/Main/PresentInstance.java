package Main;

import Dimensions.*;
import Enums.*;

public class PresentInstance {

    public static void main(String[] args) {

        // --- Material plane ---
        MaterialDimension materialPlane = new MaterialDimension(
                "Material Plane",
                TimeFlowModel.NORMAL,
                MagicBehavior.NORMAL,
                GravityModel.NORMAL,
                TravelRule.FREE
        );

        MaterialDimension feyWild = new MaterialDimension(
                "Fey Wild",
                TimeFlowModel.NORMAL,
                MagicBehavior.AMPLIFIED,
                GravityModel.NORMAL,
                TravelRule.FREE
        );

        MaterialDimension middleEarth = new MaterialDimension(
                "Middle Earth",
                TimeFlowModel.NORMAL,
                MagicBehavior.FORBIDDEN,
                GravityModel.NORMAL,
                TravelRule.FREE
        );

        MaterialDimension underdark = new MaterialDimension(
                "Underdark",
                TimeFlowModel.DECELERATED,
                MagicBehavior.NORMAL,
                GravityModel.NORMAL,
                TravelRule.FREE
        );

        MaterialDimension paleEarth = new MaterialDimension(
                "Pale Earth",
                TimeFlowModel.NORMAL,
                MagicBehavior.SUPPRESSED,
                GravityModel.HIGH,
                TravelRule.FREE
        );

        // --- Divine domains ---
        DivineDimension domainOfLove = new DivineDimension(
                "Domain of Love",
                TimeFlowModel.DECELERATED,
                MagicBehavior.WARPED,
                GravityModel.CHAOTIC,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfJustice = new DivineDimension(
                "Domain of Justice",
                TimeFlowModel.ACCELERATED,
                MagicBehavior.SENTIENT,
                GravityModel.DIRECTIONAL,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfTemperance = new DivineDimension(
                "Domain of Temperance",
                TimeFlowModel.DECELERATED,
                MagicBehavior.SUPPRESSED,
                GravityModel.NONE,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfFortitude = new DivineDimension(
                "Domain of Fortitude",
                TimeFlowModel.NORMAL,
                MagicBehavior.SUPPRESSED,
                GravityModel.DIRECTIONAL,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfFaith = new DivineDimension(
                "Domain of Faith",
                TimeFlowModel.DECELERATED,
                MagicBehavior.SUPPRESSED,
                GravityModel.CHAOTIC,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfWrath = new DivineDimension(
                "Domain of Wrath",
                TimeFlowModel.DECELERATED,
                MagicBehavior.WARPED,
                GravityModel.DIRECTIONAL,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfHope = new DivineDimension(
                "Domain of Hope",
                TimeFlowModel.DECELERATED,
                MagicBehavior.SENTIENT,
                GravityModel.NONE,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfPrudence = new DivineDimension(
                "Domain of Prudence",
                TimeFlowModel.DECELERATED,
                MagicBehavior.FORBIDDEN,
                GravityModel.NONE,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfGreed = new DivineDimension(
                "Domain of Greed",
                TimeFlowModel.NORMAL,
                MagicBehavior.WARPED,
                GravityModel.DIRECTIONAL,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfEnvy = new DivineDimension(
                "Domain of Envy",
                TimeFlowModel.FRACTURED,
                MagicBehavior.SENTIENT,
                GravityModel.CHAOTIC,
                TravelRule.RESTRICTED
        );

        DivineDimension domainOfGluttony = new DivineDimension(
                "Domain of Gluttony",
                TimeFlowModel.ACCELERATED,
                MagicBehavior.SENTIENT,
                GravityModel.CHAOTIC,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfPride = new DivineDimension(
                "Domain of Pride",
                TimeFlowModel.DECELERATED,
                MagicBehavior.SUPPRESSED,
                GravityModel.DIRECTIONAL,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfSloth = new DivineDimension(
                "Domain of Love",
                TimeFlowModel.DECELERATED,
                MagicBehavior.SUPPRESSED,
                GravityModel.NONE,
                TravelRule.INVITATION_ONLY
        );

        DivineDimension domainOfLust = new DivineDimension(
                "Domain of Lust",
                TimeFlowModel.DECELERATED,
                MagicBehavior.WARPED,
                GravityModel.NONE,
                TravelRule.INVITATION_ONLY
        );

        // --- Infernal Plane ---
        InfernalDimension pitOfCinders = new InfernalDimension(
                "Pit of Cinders",
                TimeFlowModel.DECELERATED,
                MagicBehavior.WARPED,
                GravityModel.HIGH,
                TravelRule.INVITATION_ONLY
        );

        // --- Astral / Far Realms ---
        AstralDimension infiniteVoid = new AstralDimension(
                "Infinite Void",
                TimeFlowModel.DECELERATED,
                MagicBehavior.AMPLIFIED,
                GravityModel.NONE,
                TravelRule.RESTRICTED
        );

        AstralDimension farRealmInnerRings = new AstralDimension(
                "Far Realm Inner Rings (Angel of Fortitude's Domain)",
                TimeFlowModel.FRACTURED,
                MagicBehavior.SUPPRESSED,
                GravityModel.NONE,
                TravelRule.RESTRICTED
        );

        AstralDimension farRealmOuterRings = new AstralDimension(
                "Far Realm Outer Rings (Witch of Envy's Domain)",
                TimeFlowModel.FRACTURED,
                MagicBehavior.SENTIENT,
                GravityModel.NONE,
                TravelRule.RESTRICTED
        );

        // --- Dream World ---
        PrimordialDimension dreamWorld = new PrimordialDimension(
                "Dream World",
                TimeFlowModel.NORMAL,
                MagicBehavior.SENTIENT,
                GravityModel.DIRECTIONAL,
                TravelRule.INVITATION_ONLY
        );

        // --- Digital Realm ---
        PrimordialDimension digitalRealm = new PrimordialDimension(
                "Digital Realm",
                TimeFlowModel.LOOPING,
                MagicBehavior.SENTIENT,
                GravityModel.NONE,
                TravelRule.RESTRICTED
        );

        // --- Realm Of Chaos ---
        PrimordialDimension realmOfChaos = new PrimordialDimension(
                "Realm Of Chaos",
                TimeFlowModel.FRACTURED,
                MagicBehavior.AMPLIFIED,
                GravityModel.CHAOTIC,
                TravelRule.FORBIDDEN
        );

        // --- Void Edges ---
        VoidDimension pitOfOblivion = new VoidDimension(
                "Pit Of Oblivion",
                TimeFlowModel.FROZEN,
                MagicBehavior.FORBIDDEN,
                GravityModel.NONE,
                TravelRule.ONE_WAY
        );

        VoidDimension outherEdges = new VoidDimension(
                "Outer Edges",
                TimeFlowModel.DECELERATED,
                MagicBehavior.SUPPRESSED,
                GravityModel.NONE,
                TravelRule.FREE
        );

        VoidDimension tunnelsOfDarkness = new VoidDimension(
                "tunnelsOfDarkness",
                TimeFlowModel.REVERSED,
                MagicBehavior.WARPED,
                GravityModel.NONE,
                TravelRule.RESTRICTED
        );

        System.out.println("All dimensions instantiated for PresentInstance.");
    }
}