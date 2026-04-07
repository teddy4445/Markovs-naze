import { SaveManager } from "./SaveManager.js";

export class AudioController {
  static stopMusic(scene) {
    const active = scene.game.__markovsMazeMusic;
    if (active?.sound) {
      active.sound.stop();
      active.sound.destroy();
      scene.game.__markovsMazeMusic = null;
    }
  }

  static playMusic(scene, key, config = {}) {
    if (!SaveManager.isMusicEnabled() || !scene.cache.audio.exists(key)) {
      this.stopMusic(scene);
      return null;
    }

    const active = scene.game.__markovsMazeMusic;
    if (active?.key === key && active.sound?.isPlaying) {
      return active.sound;
    }

    this.stopMusic(scene);
    const sound = scene.sound.add(key, {
      loop: true,
      volume: 0.35,
      ...config,
    });
    sound.play();
    scene.game.__markovsMazeMusic = { key, sound };
    return sound;
  }

  static playSfx(scene, key, config = {}) {
    if (!SaveManager.isSoundEnabled() || !scene.cache.audio.exists(key)) {
      return null;
    }

    return scene.sound.play(key, { volume: 0.65, ...config });
  }

  static playExclusiveSfx(scene, channel, key, config = {}) {
    if (!SaveManager.isSoundEnabled() || !scene.cache.audio.exists(key)) {
      return null;
    }

    scene.game.__markovsMazeExclusiveSfx ??= {};
    const activeSound = scene.game.__markovsMazeExclusiveSfx[channel];
    if (activeSound?.isPlaying) {
      return activeSound;
    }

    activeSound?.stop();
    activeSound?.destroy();

    const sound = scene.sound.add(key, { volume: 0.65, ...config });
    scene.game.__markovsMazeExclusiveSfx[channel] = sound;
    sound.once("complete", () => {
      if (scene.game.__markovsMazeExclusiveSfx[channel] === sound) {
        scene.game.__markovsMazeExclusiveSfx[channel] = null;
      }
      sound.destroy();
    });
    sound.play();
    return sound;
  }
}
