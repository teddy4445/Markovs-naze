import { DIRECTION_ORDER, DIRECTION_VECTORS, RELATIVE_OUTCOMES } from "../game/constants.js";

function rotate(direction, offset) {
  const startIndex = DIRECTION_ORDER.indexOf(direction);
  return DIRECTION_ORDER[(startIndex + offset + DIRECTION_ORDER.length) % DIRECTION_ORDER.length];
}

export function relativeToAbsoluteDirection(intendedDirection, relativeOutcome) {
  switch (relativeOutcome) {
    case "intended":
      return intendedDirection;
    case "opposite":
      return rotate(intendedDirection, 2);
    case "left":
      return rotate(intendedDirection, -1);
    case "right":
      return rotate(intendedDirection, 1);
    default:
      return "stay";
  }
}

export class ProbabilityResolver {
  static resolve(profile, intendedDirection, options = {}) {
    const rng = options.rng ?? Math.random;
    const validator = options.validator ?? (() => true);
    const origin = options.origin ?? { x: 0, y: 0 };

    const candidates = RELATIVE_OUTCOMES.map((relativeOutcome) => {
      const absoluteDirection = relativeToAbsoluteDirection(intendedDirection, relativeOutcome);
      const delta = DIRECTION_VECTORS[absoluteDirection];
      const target = {
        x: origin.x + delta.x,
        y: origin.y + delta.y,
      };
      const weight = profile[relativeOutcome] ?? 0;
      const valid = relativeOutcome === "stay" ? true : validator(target, absoluteDirection, relativeOutcome);
      return {
        relativeOutcome,
        absoluteDirection,
        delta,
        target,
        weight,
        valid,
      };
    }).filter((candidate) => candidate.weight > 0);

    const validCandidates = candidates.filter((candidate) => candidate.valid);
    const pool = validCandidates.length > 0 ? validCandidates : candidates.filter((candidate) => candidate.relativeOutcome === "stay");

    const totalWeight = pool.reduce((sum, candidate) => sum + candidate.weight, 0);
    let threshold = rng() * totalWeight;
    let selected = pool[pool.length - 1];

    for (const candidate of pool) {
      threshold -= candidate.weight;
      if (threshold <= 0) {
        selected = candidate;
        break;
      }
    }

    const invalidRelativeOutcomes = candidates
      .filter((candidate) => !candidate.valid)
      .map((candidate) => candidate.relativeOutcome);

    return {
      intendedDirection,
      profile,
      relativeOutcome: selected.relativeOutcome,
      absoluteDirection: selected.absoluteDirection,
      delta: selected.delta,
      target: selected.relativeOutcome === "stay" ? origin : selected.target,
      stayed: selected.relativeOutcome === "stay",
      resampled: invalidRelativeOutcomes.length > 0,
      invalidRelativeOutcomes,
      attemptedTarget: {
        x: origin.x + DIRECTION_VECTORS[intendedDirection].x,
        y: origin.y + DIRECTION_VECTORS[intendedDirection].y,
      },
    };
  }
}
