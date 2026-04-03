import { levels } from "../data/levels/index.js";

const STORAGE_KEY = "markovs-maze-save";

const defaultState = {
  unlockedLevelIds: [1],
  completedLevelIds: [],
  settings: {
    soundEnabled: true,
    musicEnabled: true,
  },
};

function normalizeState(rawState) {
  const state = rawState ?? {};
  const unlocked = Array.isArray(state.unlockedLevelIds) ? state.unlockedLevelIds : [1];
  const completed = Array.isArray(state.completedLevelIds) ? state.completedLevelIds : [];
  const settings = {
    soundEnabled: state.settings?.soundEnabled ?? true,
    musicEnabled: state.settings?.musicEnabled ?? true,
  };

  return {
    unlockedLevelIds: Array.from(new Set([1, ...unlocked])).sort((a, b) => a - b),
    completedLevelIds: Array.from(new Set(completed)).sort((a, b) => a - b),
    settings,
  };
}

export class SaveManager {
  static load() {
    try {
      const raw = globalThis.localStorage?.getItem(STORAGE_KEY);
      return normalizeState(raw ? JSON.parse(raw) : defaultState);
    } catch {
      return normalizeState(defaultState);
    }
  }

  static save(nextState) {
    const normalized = normalizeState(nextState);
    globalThis.localStorage?.setItem(STORAGE_KEY, JSON.stringify(normalized));
    return normalized;
  }

  static getState() {
    return this.load();
  }

  static isLevelUnlocked(levelId) {
    return this.getState().unlockedLevelIds.includes(levelId);
  }

  static isLevelCompleted(levelId) {
    return this.getState().completedLevelIds.includes(levelId);
  }

  static completeLevel(levelId) {
    const current = this.getState();
    const next = {
      ...current,
      completedLevelIds: Array.from(new Set([...current.completedLevelIds, levelId])),
      unlockedLevelIds: Array.from(new Set([...current.unlockedLevelIds, levelId, levelId + 1])).filter(
        (candidate) => levels.some((level) => level.id === candidate),
      ),
    };
    return this.save(next);
  }

  static getUnlockedLevelIds() {
    return this.getState().unlockedLevelIds;
  }

  static unlockAllLevels() {
    const current = this.getState();
    return this.save({
      ...current,
      unlockedLevelIds: levels.map((level) => level.id),
    });
  }

  static getRecommendedLevelId() {
    const state = this.getState();
    const firstUnlockedIncomplete = levels.find(
      (level) => state.unlockedLevelIds.includes(level.id) && !state.completedLevelIds.includes(level.id),
    );
    return firstUnlockedIncomplete?.id ?? state.unlockedLevelIds.at(-1) ?? 1;
  }

  static isSoundEnabled() {
    return this.getState().settings.soundEnabled;
  }

  static isMusicEnabled() {
    return this.getState().settings.musicEnabled;
  }

  static updateSettings(partialSettings) {
    const current = this.getState();
    const next = {
      ...current,
      settings: {
        ...current.settings,
        ...partialSettings,
      },
    };
    return this.save(next);
  }

  static toggleSound() {
    const current = this.getState();
    return this.updateSettings({ soundEnabled: !current.settings.soundEnabled });
  }

  static toggleMusic() {
    const current = this.getState();
    return this.updateSettings({ musicEnabled: !current.settings.musicEnabled });
  }
}
