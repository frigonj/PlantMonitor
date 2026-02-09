import asyncio
from kasa import SmartPlug

async def _turn_on(device_ip):
    device = SmartPlug(device_ip)
    await device.update()
    await device.turn_on()

async def _turn_off(device_ip):
    device = SmartPlug(device_ip)
    await device.update()
    await device.turn_off()

async def _get_status(device_ip):
    device = SmartPlug(device_ip)
    await device.update()
    return device.is_on

def turn_fan_on(device_ip):
    try:
        asyncio.run(_turn_on(device_ip))
    except Exception as e:
        print(f"Error turning fan on: {e}")
        raise

def turn_fan_off(device_ip):
    try:
        asyncio.run(_turn_off(device_ip))
    except Exception as e:
        print(f"Error turning fan off: {e}")
        raise

def get_fan_status(device_ip):
    try:
        return asyncio.run(_get_status(device_ip))
    except Exception as e:
        print(f"Error getting fan status: {e}")
        raise
