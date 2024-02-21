from dataclasses import dataclass
from time import sleep

import rpi_ws281x as rpi

strip = None

@dataclass
class STRIP_INIT:

  DELAY = 0.02

@dataclass
class STRIP:

  LED_COUNT = 1500
  LED_PIN = 18
  LED_FREQ = 800000
  LED_DMA = 10
  LED_INVERT = False
  LED_BRIGHTNESS = 100
  LED_CHANNEL = 0

def Clear():

  global strip

  for led in range(0, STRIP.LED_COUNT):
    strip.setPixelColor(led, rpi.Color(0,0,0))
  strip.show()

  sleep(STRIP_INIT.DELAY)

def Apply(data):

  global strip

  for instruction in data:
    print(instruction)
    slot, r, g, b = instruction
    strip.setPixelColor(slot, rpi.Color(r, g, b))
  strip.show()

def Init():

  global strip

  print(f"Pin: {STRIP.LED_PIN}")
  strip = rpi.Adafruit_NeoPixel(
    STRIP.LED_COUNT,
    STRIP.LED_PIN,
    STRIP.LED_FREQ,
    STRIP.LED_DMA,
    STRIP.LED_INVERT,
    STRIP.LED_BRIGHTNESS,
    STRIP.LED_CHANNEL
  )

  strip.begin()
  for pixel in range(0, STRIP.LED_COUNT):
    strip.setPixelColor(pixel, rpi.Color(0,0,0))
  strip.show()

  sleep(1)
  Clear()

numLEDs = 500
ledBuffer = [(0, 0, 0)] * numLEDs
maxIter = 1000
maxIndex = 1

base = (240, 100, 0)
ledBuffer[0] = base
rf, gf, bf = False, False, False
rs, gs, bs = 2, 3, 5

def newColor(c, cf, cs, maxVal=255, minVal=0):

  if cf:
    c = min(c+cs, maxVal)
    if c == maxVal:
      cf = False

  else:
    c = max(c-cs, minVal)
    if c == minVal:
      cf = True

  return c, cf

Init()
# Apply(
#   data=[
#     (i, 50, 50, 255) for i in range(3, 25)
#   ]
# )
# Apply(
#   data=[
#     (i, 100, 150, 255) for i in range(50, 55)
#   ] + [(i, 100, 150, 255) for i in range(72, 94)]
# )
# Apply(
#   data=[
#     (i, 255, 0, 0) for i in range(96, 118)
#   ]
# )
# Apply(
#   data=[
#     (i, 246, 174, 45) for i in range(142, 164)
#   ]
# )
# Apply(
#   data=[
#     (i, 255, 100, 150) for i in range(189, 211)
#   ]
# )

for iter in range(0, maxIter):

  Apply(data=[
    (i, r, g, b) 
    for (i, (r, g, b)) in enumerate(ledBuffer) 
    if i not in range(25,50)
    and i not in range(55,72)
    and i not in range(94, 96)
    and i not in range(118, 142)
    and i not in range(164, 189)
  ])

  counter = maxIndex
  if counter >= numLEDs:
    counter = numLEDs-1

  for index in range(counter, 0, -1):
    ledBuffer[index] = ledBuffer[index - 1]

  r, g, b = base
  r, rf = newColor(r, rf, rs)
  g, gf = newColor(g, gf, gs)
  b, bf = newColor(b, bf, bs)

  base = (r, g, b)
  ledBuffer[0] = base

  maxIndex += 1
