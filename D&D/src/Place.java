import Dimensions.Dimension;

public abstract class Place {

    protected final String name;
    protected final Dimension dimension;

    protected Place(String name, Dimension dimension) {
        this.name = name;
        this.dimension = dimension;
    }

    public Dimension getDimension() {
        return dimension;
    }
}
