# Cluster Intelligence simulation

![DEMO GIF](https://user-images.githubusercontent.com/83420512/210019036-655bd569-49bb-4cc0-8cb3-3358c5f19485.gif)

## Description

This little dots called Boids. Red and Blue circles are supply bases. Each Boid wants to go to one of them.
### Boid behavior: 
- moves (slight randomly)
- If he hit the base, he starts counting distance from base and screaming that distance to nearby Boids. He also change his own target base
- listens
- screams
- If he listens the distance to his target base, he screams that distance too and starts moving in direction from which scream came

Each of them pretty stupid and never be able to transfer supplies from one base to another, but together they do it pretty well.

## Controls
- LMB - change the position of blue Station
- RMB - interaction line visible/invisible 
- MMB/MV - show/hide grid
