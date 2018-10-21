
import calendar
import json
import os
import re
import sys
import time
from random import randint, shuffle

from qdb import Post, Schedule, Time, Timer, Watch, init_database, sessionmaker

if __name__ == '__main__':

    DATA = {
        "messages": [
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\badheilen\\01-badheilen-forest.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\badheilen\\02-badheilen-bridge.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\badheilen\\03-badheilen-dash-prototype.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\badheilen\\04-badheilen-enemies-jumping.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\balance.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\football.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\helicopter.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\jumpjump.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\lookball.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\obstaculos-overflow.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\obstaculos.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\parachute.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\recycle1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\recycle2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\ciudadkolbi\\taptap.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\deaden\\a-weird-statue.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\deaden\\building-a-door.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\deaden\\building-a-road.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\deaden\\deaden-demon-eyes.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\deaden\\deaden1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\deaden\\deaden_bridge-building.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\deaden\\deaden_bridge-building2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\drybreed\\drybreed1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\drybreed\\drybreed_energy_post-compo.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\drybreed\\drybreed_itchio1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\drybreed\\drybreed_post-compo_itchio_cover.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\drybreed\\drybreed_tutorial_post-compo.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\drybreed\\Drybreed__NewTerrain.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\drybreed\\Drybreed__NewTutorial.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\a-tunnel-for-the-prison_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\creation-of-the-spike-environment_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\eon-vs-turtle_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\everything-is-3d.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\filling-it-with-trees_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\first-enemy-creation__haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\fly-attack-motion_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\fly-test-over-the-second_haldron_moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\haldron-moon_bad-walking.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\haldron-moon_floating-islands.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\haldron-moon_giass.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\haldron-moon_walking-and-flying.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\HaldronMoon_FlyingFruits1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\HaldronMoon_FlyingTest1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\HaldronMoon_FlyingTest2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\HaldronMoon_UIDialog1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\HaldronMoon_UIDialog2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\haldron_moon-giass1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\haldron_moon-houses1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\stealth-vibe_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\the-prison_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\the-second-island_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\traveling-to-another-island_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\trying.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\turtle-explosions_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\turtle-idle-animation.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\turtle-is-not-ready-to-fight.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\turtle-patrol_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\turtle-walking-animation-20s.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\turtle-walking-animation-v1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\zoom-mechanic-take-2_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon\\zoom-test_haldron-moon.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\auto-zoom-better-boss-walking1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\auto-zoom-better-boss-walking2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\bullets-stamina-ui.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\crossing-buildings.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\damage-ui-knockback1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\damage-ui-knockback2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\dash-feedback.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\destroying-the-ugly-island.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\editor-trailrenderer-darkness.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\editor-trailrenderer.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\firstfight1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\firstfight2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\firstfight3.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\firstfight4.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\firstfight5.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\firstfight6.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\flying-inthe-darkness.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\ground-destruction.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\ground-dive.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\ground-rain.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\holes-in-the-walls.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\hyperdash-v1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\improved-laser-fx.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\laser-destruction.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\missiles-laser-destruction.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-first-version.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-machine-gun.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-mecha-editor-motion-test.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-mecha-first-motion-test.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-preparing-to-attack.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-punch1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-punch2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-children-stomp-walk.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasite-mecha-pursuit.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasitechildren-machinegun-framedrop.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasitechildren-machinegun2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\parasitechildren-thinking.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\playingwith-dash-and-laser.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\playingwith-dash-and-laser2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\playingwith-dash-and-laser3.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\puncher-lasercounter-needmorefeedback.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\ricochet-bullets.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\haldronmoon-silx\\some-feedback-fx.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\heilen\\heilen_spider_test_1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\heilen\\heilen_spider_test_2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helevenium\\helevenium1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helevenium\\helevenium2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helevenium\\helevenium3.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helevenium\\helevenium4.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helevenium\\helevenium5.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\Itchio Selection\\hellcars_air-boost.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\Itchio Selection\\hellcars_boost-flip.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\Itchio Selection\\hellcars_planning.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\Itchio Selection\\hellcars_snap-jump.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\Itchio Selection\\hellcars_strong-jump.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\Itchio Selection\\hellcars_wall-jumping.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\hellcars_air-maneuver.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\hellcars_jump-turn.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\hellcars_landing-boost.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\Gif Pack 1\\hellcars_wall-jumping2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\hellcars_cool-landing.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\hellcars_jump-landing.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hellcars\\hellcars_turn-landing.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\a-new-scene_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\beach-trees_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\dash-attack_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\dash-dagger_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\first-enemy_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\hellvium-concept-v2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\helvium-joses-background-test.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\improving-the-2nd-scene_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\map_growth-hellvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\scene1_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\testing-the-attack_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-beach-v1_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-dagger_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-lizard_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-second-enemy_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-sword-soldier_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-sword_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-thieves-cave_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-third-enemy_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\the-walking-sucks_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\helvium\\walking-and-sword-holding_helvium.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\01_hunt_enemy1-test.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\02_hunt_enemy1-test2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\03_hunt_enemies-alerted-running.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\04_hunt_enemies-alerted-running2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\05_gem-protectors.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\06_they-are-connected.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\07_teleport-is-not-a-cheatcode.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\hunt\\08_teleport-and-laser.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\itchio\\helevenium_itchio1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\itchio\\onanigan_itchio1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\itchio\\phantom_garden_itchio1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\itchio\\valax+eon_itchio1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\minimalistherain\\minimalist-rain.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\minimalistherain\\minimalist-rain2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\numelica\\numelica-ernac-smaller.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\numelica\\numelica-ernac.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\numelica\\numelica-world-generation1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\numelica\\numelica1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\numelica\\numelica2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\onanigan\\onanigan-first-round.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\onanigan\\onanigan-teleport1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\onanigan\\onanigan-teleport2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\onanigan\\onanigan-title1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\onanigan\\onanigan1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\other\\lobulos.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\other\\mandinga.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\other\\obstaculos-camera-glitch.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\1-2-Wall-Attach.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\1-3-More-Wall-Attach.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\1-4-Wall-Crawling-Teleport.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\1-5-Teleport-and-particles.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\1-6-1-Fast-motion.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\1-6-1-Inclination-and-running-particles.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\1_1_concept.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\2-5-Precision-helps.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\2-6-It-moves.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\2-8-First-enemy-test.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\2-9-Ludum-Dare-Showcase.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-2-Experimenting-with-narrative-2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-2-Experimenting-with-narrative.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-3-Maybe-you-can-escape-the-bullets.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-3-Testing-out-the-first-enemy-encounter-1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-3-Testing-out-the-first-enemy-encounter-2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-4-Sneaky-test_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-6-Experimenting-with-zone-trails.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3-7-They-are-unconnected.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\3_9-Long-jump-test.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\carrierHangar.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\Endy.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\first-enemies-after-teleport.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\HighJump.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\levels-highlight.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\more-enemies-and-teleport.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer-dissolve-fx-test.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_attack-stun-test_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\Primer_Endy_IDLE.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\Primer_Endy_Run.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\Primer_Eon_retopology.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_first-world-overview.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_fungus-hunger_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_fungus-tree2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_fungus-tree_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_Hivelord-HunterBulletFat_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_horizontal-platform.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_HunterBullet_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_intro-scene.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_laser-danger-test_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_laser-prototype.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_laser-trio_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_lasers-double-jump1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_lasers-double-jump2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_more-teleport-learning.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_moving-and-teleporting-stuff.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_player-integration.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_player-model-teleport_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_rotating-platform.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_teleport-jump_itchio.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_teleporting-cams.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_the-terraformer-fungus.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\primer_vertical-platforms.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\teaching-the-teleport.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\the-game-has-just-started.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\Walker_running.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\Walker_walking.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\wip fall.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\wipStaticWalker.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\primer\\wipStaticWalker01.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\sadseed\\sadseed-big-building-destruction.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\sadseed\\sadseed-big-building.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\sadseed\\sadseed-construction.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\sadseed\\sadseed-construction2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\sadseed\\sadseed-seed-creature.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\silx\\silx1.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\silx\\silx2.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\silx\\silx3.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\silx\\silx4.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\silx\\silx5.gif"
            },
            {
                "text": "",
                "image": "D:\\Dropbox\\Public\\games\\gif\\silx\\silx6.gif"
            }
        ]
    }

    DIR = os.path.normpath(
        os.path.dirname(
            sys.executable if getattr(sys, 'frozen', False) else __file__))
    os.chdir(DIR)  # The current dir should be the script home

    hours = [f"{hour:02}:{30:02}"
             for hour in range(0, 24, 2)
             for minute in range(0, 60, 60)]

    print(hours)
    sys.exit(0)

    TAGS = [
        '#gamedev',
        '#indiedev'
    ]
    TAGIX = 0

    LPAD = ['(', '{', '[', '<', '|', ':', '*', '-']
    RPAD = [')', '}', ']', '>', '|', ':', '*', '-']
    PIX = randint(0, 256) % len(LPAD)

    # Rehashing DATA already on the database to fit a criteria

    ENGINE = init_database()
    SESSION = sessionmaker(bind=ENGINE)
    DB = SESSION()

    tweets = DB.query(Post)\
        .filter(Post.schedule_id == 6)\
        .filter(Post.published == 0)\
        .filter(Post.error == 0).all()

    OFFSET = 20
    COUNT = OFFSET + 1
    for i in tweets:

         # Date folder creation
        year, month, day, *_ = time.gmtime(os.path.getmtime(i.image_url))
        month = calendar.month_name[month]
        date = re.sub(" +", " ", f"{month}, {year}").strip()

        image_name = os.path.basename(i.image_url)
        count_info = f"{LPAD[PIX]}{COUNT} of {len(tweets)+OFFSET}{RPAD[PIX]}"
        tags = TAGS[TAGIX]
        i.text = f"{count_info} {image_name} {LPAD[PIX]}{date}{RPAD[PIX]} #gamedev #indiedev #matnesis"
        print(f"{i.text}")

        COUNT += 1
        PIX = (PIX + 1) % len(LPAD)
        TAGIX = (TAGIX + 1) % len(TAGS)

        DB.add(i)
    DB.commit()

    # Randomize tagged-counted qbot file with the DATA

    # MESSAGES = DATA['messages']
    # shuffle(MESSAGES)

    # COUNT = 1
    # for i in MESSAGES:
    #     i['text'] = f"{TAGS[TAGIX]} {LPAD[PIX]}{COUNT}/{len(MESSAGES)}{RPAD[PIX]}"
    #     COUNT += 1
    #     PIX = (PIX + 1) % len(LPAD)
    #     TAGIX += 1
    #     if TAGIX >= len(TAGS):
    #         shuffle(TAGS)
    #         TAGIX = 0

    # DATA['hours'] = [f"{hour:02}:{30:02}"
    #                  for hour in range(10, 22, 2)
    #                  for minute in range(0, 60, 60)]

    # with open('qscan.json', 'w') as f:
    #     json.dump(DATA, f)
