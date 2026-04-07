export const GAME_WIDTH = 1280;
export const GAME_HEIGHT = 720;
export const TILE_SIZE = 64;
export const HUD_WIDTH = 360;
export const FONT_FAMILY = 'Georgia, "Times New Roman", serif';

export const COLORS = {
  background: 0x141319,
  panelText: "#f7f2e8",
  accent: "#8ae3d5",
  accentWarm: "#e0be5c",
  danger: "#d86a58",
  muted: "#c8bba3",
  ink: "#17120d",
  panelLightTextured: 0xe9dfcb,
  panelLightStroke: 0x5b4f41,
};

export const DIRECTION_ORDER = ["up", "right", "down", "left"];

export const DIRECTION_VECTORS = {
  up: { x: 0, y: -1 },
  right: { x: 1, y: 0 },
  down: { x: 0, y: 1 },
  left: { x: -1, y: 0 },
  stay: { x: 0, y: 0 },
};

export const RELATIVE_OUTCOMES = ["intended", "opposite", "left", "right", "stay"];
