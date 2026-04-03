import { getAudioAssets, getSpriteSheetConfig, getVisualAssets } from "./AssetRegistry.js";

export function preloadAllAssets(scene) {
  for (const asset of getVisualAssets()) {
    if (!asset.url) {
      continue;
    }

    const spriteSheetConfig = getSpriteSheetConfig(asset.asset_id);
    if (spriteSheetConfig) {
      scene.load.spritesheet(asset.key, asset.url, spriteSheetConfig);
    } else {
      scene.load.image(asset.key, asset.url);
    }
  }

  for (const asset of getAudioAssets()) {
    if (!asset.url) {
      continue;
    }
    scene.load.audio(asset.key, asset.url);
  }
}
