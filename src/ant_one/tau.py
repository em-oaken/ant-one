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
        self.start_time = datetime.datetime.now()
        self.loopno = 0
        self.living_objects = []
        self.render = None
    
    def add_life(self, object):
        self.living_objects.append(object)
    
    def add_render(self, render):
        self.render = render

    async def event_loop_manager(self):
        """Manages the event loop"""
        self.loop_starttime = datetime.datetime.now()
        while True:
            self.loopno += 1
            time_now = datetime.datetime.now()
            self.loop_duration = (time_now - self.loop_starttime).total_seconds()
            self.loop_starttime = time_now

            for obj in self.living_objects:
                obj.live()
            self.render()
            
            await asyncio.sleep(0.03)

