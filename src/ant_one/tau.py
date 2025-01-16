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


class Tau():
    def __init__(self):
        """Initiates time engine"""
        self.start_time = datetime.datetime.now()
        self.loopno = 0
        self.objects = []
        self.render = None
    
    def add_object(self, object):
        self.objects.append(object)
    
    def add_render(self, render):
        self.render = render

    async def event_loop_manager(self):
        """Manages the event loop"""
        while True:
            self.loopno += 1
            self.looptime = datetime.datetime.now()

            logging.info(f'Loop #{self.loopno}')
            for obj in self.objects:
                obj.live()
            self.render()
            
            await asyncio.sleep(0.1)

