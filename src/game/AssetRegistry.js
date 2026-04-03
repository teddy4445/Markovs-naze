import artManifest from "../../data/asset_manifest.json";
import audioManifest from "../../data/audio_manifest.json";

const assetFiles = import.meta.glob("../../assets/processed/**/*.{png,ogg,wav}", {
  eager: true,
  import: "default",
  query: "?url",
});

function normalizePath(path) {
  return path.replace(/^\.\.\/\.\.\//, "").replace(/\\/g, "/");
}

const processedUrlByPath = Object.fromEntries(
  Object.entries(assetFiles).map(([path, url]) => [normalizePath(path), url]),
);

const visualAssets = artManifest.assets.map((entry) => ({
  ...entry,
  key: entry.asset_id,
  url: processedUrlByPath[entry.paths.processed] ?? null,
}));

const audioAssets = audioManifest.items.map((entry) => ({
  ...entry,
  key: entry.asset_id,
  url: processedUrlByPath[entry.processed_path] ?? null,
}));

const visualById = new Map(visualAssets.map((entry) => [entry.asset_id, entry]));
const audioById = new Map(audioAssets.map((entry) => [entry.asset_id, entry]));

export function getVisualAssets() {
  return visualAssets;
}

export function getAudioAssets() {
  return audioAssets;
}

export function getVisualAsset(assetId) {
  return visualById.get(assetId) ?? null;
}

export function getAudioAsset(assetId) {
  return audioById.get(assetId) ?? null;
}

export function getVisualUrl(assetId) {
  return getVisualAsset(assetId)?.url ?? null;
}

export function getAudioUrl(assetId) {
  return getAudioAsset(assetId)?.url ?? null;
}

export function getSpriteSheetConfig(assetId) {
  const entry = getVisualAsset(assetId);
  if (!entry?.animation?.animated) {
    return null;
  }

  return {
    frameWidth: entry.animation.frame_width,
    frameHeight: entry.animation.frame_height,
  };
}

export function getTextureKey(assetId) {
  return getVisualAsset(assetId)?.key ?? assetId;
}

export function getAudioKey(assetId) {
  return getAudioAsset(assetId)?.key ?? assetId;
}
