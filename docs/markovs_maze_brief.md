# Markov's Maze - Project Brief

## High concept
Markov's Maze is a browser-based 2D puzzle maze game built with Phaser 3. The player moves on a grid inside fantasy ruins, but movement is probabilistic rather than deterministic.

## Core movement system
Each walkable tile defines five probabilities:
- intended direction occurs
- opposite direction occurs
- 90 degree left occurs
- 90 degree right occurs
- nothing occurs

These probabilities are relative to the player's chosen input.
If a sampled move would hit a wall, resample until a valid result is found.

## Enemy
There is one enemy type in the MVP: a cursed knight.
Behavior:
- follows a predefined patrol path when not chasing
- if it has line of sight to the player in the same row or column, it chases
- enemy movement uses the same probabilistic tile rules as the player
- enemy cannot enter walls
- enemy cannot enter player-killing tiles such as trap or lava
- if a forbidden enemy move is sampled, resample
- if line of sight is lost, enemy returns to the closest point on its path and resumes patrol

## Lose conditions
The player loses if:
- stepping on forbidden tiles like trap or lava
- touching an enemy

There is no timer and no max-step lose condition.

## Progression
The MVP has 8 handcrafted levels.
Progress is saved in browser local storage.

## Theme
Fantasy ruins.

## Visual direction
- low-detail flat fantasy
- top-down 2D
- ancient magical ruins
- readable puzzle-first visuals
- probability visualization uses a compass-circle symbol on tiles
- player character is a ruins scholar
- enemy is a cursed knight
- audio tone is magical and mysterious

## Required scenes later
- MenuScene
- LevelSelectScene
- GameScene

## Important product requirement
This repository must keep clean documentation because the next phase after asset generation is full game development from the same docs.

## Asset goals
Generate or prepare all assets needed for the game:
- environment tiles
- overlays
- player sprites and animations
- enemy sprites and animations
- VFX
- menu backgrounds
- level select background
- gameplay background
- long parallax background
- logo
- menu buttons
- level buttons
- in-game UI buttons
- HUD panels
- icons
- sound effects
- music placeholders if full music is not sourced now

## Sound sourcing rule
Use OpenGameArt only for downloaded sound effects.
Do not use any asset with unclear licensing.
Record source, author, chosen license, and attribution text for every downloaded audio asset.