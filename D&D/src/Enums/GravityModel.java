package Enums;

public enum GravityModel {
    NORMAL,        // Earth-like
    LOW,           // Floaty, long jumps
    HIGH,          // Crushing, oppressive
    DIRECTIONAL,   // Has a preferred direction (walls, towers)
    RADIAL,        // Pulls toward a center point
    CHAOTIC,       // Direction changes unpredictably
    NONE           // Free movement
}
