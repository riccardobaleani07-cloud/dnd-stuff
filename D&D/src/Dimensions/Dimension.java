package Dimensions;

import Enums.CosmologyLayer;
import Enums.GravityModel;
import Enums.MagicBehavior;
import Enums.TimeFlowModel;
import Enums.TravelRule;

public abstract class Dimension {
    protected final String name;
    protected final TimeFlowModel timeFlow;
    protected final MagicBehavior magic;
    protected final GravityModel gravity;
    protected final CosmologyLayer layer;
    protected final TravelRule rule;

    public Dimension(String name, TimeFlowModel timeFlow, MagicBehavior magic,
                        GravityModel gravity, CosmologyLayer layer, TravelRule rule) {
        this.name = name;
        this.timeFlow = timeFlow;
        this.magic = magic;
        this.gravity = gravity;
        this.layer = layer;
        this.rule = rule;
    }

    @Override
    public String toString() {
        return "[name: " + name + "\n" +
               "time flow model: " + timeFlow + "\n" +
               "magic behaviour: " + magic + "\n" +
               "gravity model: " + gravity + "\\n" +
               "macro type: " + layer + "\\n" +
               "entrance generic rule: " + rule + "]";
    }
}
