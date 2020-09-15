import sys
import asyncio

from flask import Flask, redirect, request
from gevent.pywsgi import WSGIServer
from geventwebsocket.handler import WebSocketHandler
from joycontrol import logging_default as log
from joycontrol.controller import Controller
from joycontrol.memory import FlashMemory
from joycontrol.protocol import controller_protocol_factory
from joycontrol.server import create_hid_server

DEVICE = int(sys.argv[1])
CODE = sys.argv[2]

app = Flask(__name__)

buttons = [
    'b',
    'a',
    'y',
    'x',
    'l',
    'r',
    'zl',
    'zr',
    'minus',
    'plus',
    'l_stick',
    'r_stick',
    'up',
    'down',
    'left',
    'right',
    'home',
    'capture'
]
buttons.reverse()

controller_state = None


@app.route('/')
def hello():
    return redirect("/static/gamepad.html")


def sitckAmount(d):
    a = int((d / 200.0 + 0.5) * 0x1000)
    if a < 0:
        a = 0
    if a >= 0x1000:
        a = 0x1000 - 1
    return a


@app.route('/pipe_' + CODE)
def pipe():
    if request.environ.get('wsgi.websocket'):
        ws = request.environ['wsgi.websocket']
        pre_state = 0
        while True:
            message = ws.receive()
            if message is None:
                break
            nums = message.split(',')
            btn_bit = int(nums[0])
            i = 1
            for b in buttons:
                if (btn_bit & i) > 0:
                    print('push ' + b)
                controller_state.button_state.set_button(b, pushed=(btn_bit & i) > 0)
                i = i << 1

            controller_state.l_stick_state.set_h(sitckAmount(int(nums[1])))
            controller_state.l_stick_state.set_v(sitckAmount(-int(nums[2])))
            controller_state.r_stick_state.set_h(sitckAmount(int(nums[3])))
            controller_state.r_stick_state.set_v(sitckAmount(-int(nums[4])))
            if pre_state != message:
                print(nums)
                try:
                    loop.run_until_complete(controller_state.send())
                except BaseException:
                    try:
                        loop.run_until_complete(setup("B8:78:26:2A:3C:6C"))
                    except BaseException:
                        loop.run_until_complete(setup(None))
                    finally:
                        return ''
            pre_state = message
    return ''


async def setup(reconnect_bt_addr):
    global controller_state
    factory = controller_protocol_factory(Controller.PRO_CONTROLLER, spi_flash=FlashMemory())
    transport, protocol = await create_hid_server(factory, reconnect_bt_addr=reconnect_bt_addr,
                                                  ctl_psm=17,
                                                  itr_psm=19, capture_file=None,
                                                  device_id=DEVICE)
    controller_state = protocol.get_controller_state()
    await controller_state.connect()


if __name__ == "__main__":
    log.configure()
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(setup("B8:78:26:2A:3C:6C"))
    except BaseException:
        loop.run_until_complete(setup(None))

    app.debug = True

    host = '0.0.0.0'
    port = 5000 + DEVICE

    host_port = (host, port)
    server = WSGIServer(
        host_port,
        app,
        handler_class=WebSocketHandler
    )
    server.serve_forever()
