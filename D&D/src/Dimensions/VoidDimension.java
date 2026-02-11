package Dimensions;

import java.util.EnumSet;

import Enums.CosmologyLayer;
import Enums.GravityModel;
import Enums.MagicBehavior;
import Enums.TimeFlowModel;
import Enums.TravelRule;

public class VoidDimension extends Dimension {

    // Allowed options for this layer
    private static final EnumSet<TimeFlowModel> ALLOWED_TIME = EnumSet.of(
        TimeFlowModel.FRACTURED, TimeFlowModel.FROZEN, TimeFlowModel.REVERSED, TimeFlowModel.DECELERATED
    );
    private static final EnumSet<MagicBehavior> ALLOWED_MAGIC = EnumSet.of(
        MagicBehavior.WARPED, MagicBehavior.FORBIDDEN, MagicBehavior.SUPPRESSED
    );
    private static final EnumSet<GravityModel> ALLOWED_GRAVITY_MODELS = EnumSet.of(
        GravityModel.CHAOTIC, GravityModel.NONE, GravityModel.DIRECTIONAL
    );


    public VoidDimension(String name, TimeFlowModel timeFlow,
                                MagicBehavior magic, GravityModel gravity, TravelRule rule) {

        super(name,
              checkAllowed(timeFlow, ALLOWED_TIME, "timeFlow"),
              checkAllowed(magic, ALLOWED_MAGIC, "magic"),
              checkAllowed(gravity, ALLOWED_GRAVITY_MODELS, "gravity"),
              CosmologyLayer.ASTRAL,
              rule);
    }

    private static <T extends Enum<T>> T checkAllowed(T value, EnumSet<T> allowed, String fieldName) {
        if (!allowed.contains(value)) {
            throw new IllegalArgumentException(
                fieldName + " " + value + " is not allowed in VoidDimension"
            );
        }
        return value;
    }
}