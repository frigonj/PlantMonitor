import asyncio
import time
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

def _retry (func, device_ip, retries=5):
    for attempt in range(retries):
        try:
            return asyncio.run(func(device_ip))
        except Exception as e:
            if attempt == retries -1:
                print(f"Failed after {retries} attempts: {e}")
                raise
            print(f"Attempt {attempt+1} failed: {e}, retrying...")
            time.sleep(2 ** attempt)  # Exponential backoff: 1s, 2s, 4s, 8s...
    raise Exception(f"All {retries} attempts failed")

def turn_fan_on(device_ip):
    _retry(_turn_on, device_ip)

def turn_fan_off(device_ip):
    _retry(_turn_off, device_ip)

def get_fan_status(device_ip):
    return _retry(_get_status, device_ip)
