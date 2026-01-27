import asyncio
from kasa import SmartPlug

class FanController:
    def __init__(self, device_ip):
        self.device_ip = device_ip
        self.device = SmartPlug(device_ip)
    
    async def turn_on(self):
        await self.device.update()
        await self.device.turn_on()
    
    async def turn_off(self):
        await self.device.update()
        await self.device.turn_off()
    
    async def get_status(self):
        await self.device.update()
        return self.device.is_on

# Synchronous wrapper functions for Flask
def turn_fan_on(device_ip):
    controller = FanController(device_ip)
    return asyncio.run(controller.turn_on())

def turn_fan_off(device_ip):
    controller = FanController(device_ip)
    return asyncio.run(controller.turn_off())

def get_fan_status(device_ip):
    controller = FanController(device_ip)
    return asyncio.run(controller.get_status())
