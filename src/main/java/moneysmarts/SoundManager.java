package moneysmarts;

public class SoundManager {
    public void playSound(String soundName) {
        // TODO: Implement sound playback using JavaFX or another library
    }
}
package moneysmarts;

import java.util.HashMap;
import java.util.Map;

public class AssetManager {
    private Map<String, Object> assets = new HashMap<>();

    public void loadAsset(String name, Object asset) {
        assets.put(name, asset);
    }

    public Object getAsset(String name) {
        return assets.get(name);
    }
}

