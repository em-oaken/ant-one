"""
Tau is Ant One's time engine.
Its purpose is to:
- Keep track of play time and real time
- Handle action progression
- Manage game speed

Name chosen after the greek letter regularly used for time in science.
"""

import asyncio
import datetime
import logging
import time


class Tau():
    def __init__(self):
        """Initiates time engine"""
        # Accessors
        self.world = None
        self.render = None

        # Core. rt = Real Time. vt = Virtual (game) time
        self.rt_start = datetime.datetime.now()  
        self.vtime = datetime.datetime(year=1, month=1, day=1)
        self.time_factor = 10
        self.loopno = 0

    async def event_loop_manager(self):
        """Manages the event loop"""
        self.rt_loop_starttime = datetime.datetime.now()
        while True:
            # Loop data
            self.loopno += 1
            rt_now = datetime.datetime.now()
            self.rt_loop_duration = rt_now - self.rt_loop_starttime
            self.rt_loop_starttime = rt_now
            self.game_duration = (rt_now - self.rt_start).total_seconds()

            self.vt_loop_duration = self.time_factor * self.rt_loop_duration
            self.vtime += self.vt_loop_duration
            self.vt_loop_duration = self.vt_loop_duration.total_seconds()

            for obj in self.world.living_objects:
                obj.live()
            self.render()
            
            await asyncio.sleep(0.03)
    
    def add_world(self, world):
        self.world = world
    
    def add_render(self, render):
        self.render = render
