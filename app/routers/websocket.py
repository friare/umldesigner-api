from fastapi import FastAPI, APIRouter, WebSocket
from fastapi.responses import HTMLResponse
from ..repository import uml as nlp
from ..schemas import schemas

router = APIRouter(
    prefix='/socket',
    tags=['UML/socket']
)

html = """
<!DOCTYPE html>
<html lang="fr"><head><meta charset="utf-8"><meta http-equiv="X-UA-Compatible" content="IE=edge"><meta http-equiv="content-type" content="text/html; charset=UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1"><link rel="icon" href="https://umldesigner.app/favicon.ico"><title>umlDesigner</title><meta name="description" content="UMLDesigner est un outil text-diagramme permettant la création de diagramme uml à partir de text brute."><meta property="og:type" content="website"><meta property="og:title" content="umlDesigner"><meta property="og:url" content="https://www.umldesigner.app"><meta property="og:description" content="UMLDesigner est un outil text-diagramme permettant la création de diagramme uml à partir de text brute."><meta property="og:image" content="logo.svg"><meta property="og:locale" content="en_FR"><meta name="robots" content="index, follow"><style>.uml-text {
          margin-top: 5em;
          margin-left: .5em;
      }
      .uml-text span{
          color: white;
          font-weight: bold;
          text-space: 2px;
          color: #000;
          font-size: 30px;
      }
      .umlLoader {
          display: flex;
          flex-direction: column;
          justify-content: center;
          align-items: center;
          height: 100vh;
          width: 100vw;
          margin: 0;
          padding: 0;
          /*background: #263238;*/
          position: absolute;
          z-index: 100000;
      }
      .loadContainer {
          position: relative;
          top: 1.5em;
          height: 70px;/*100*/
          width: 60px;/*86*/
          transform: scale(0.5);
      }
      .cube {
          position: absolute;
          height: 70px;/*100*/
          width: 60px;/*86*/
      }
      .right {
          background: #fc45a3;
          transform: rotate(-30deg) skewX(-30deg) translate(49px, 65px) scaleY(0.86);
      }
      .left {
          background: #50c9c3;
          transform: rotate(90deg) skewX(-30deg) scaleY(0.86) translate(25px, -50px);
      }
      .top {
          background: #6960fd;
          transform: rotate(210deg) skew(-30deg) translate(-75px, -22px) scaleY(0.86);
          z-index: 2;
      }
      .face {
          height: 50px;
          width: 50px;
          position: absolute;
          transform-origin: 0 0;
      }
      .h1.w1.l1 {
          z-index: -1;
          animation-name: h1w1l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w1l1 {
          0% {
              transform: translate(0%, -100%);
          }
          14% {
              transform: translate(-50%, -125%);
          }
          28% {
              transform: translate(0%, -150%);
          }
          43% {
              transform: translate(0%, -200%);
          }
          57% {
              transform: translate(50%, -175%);
          }
          71% {
              transform: translate(0%, -150%);
          }
          85% {
              transform: translate(0%, -100%);
          }
          100% {
              transform: translate(0%, -100%);
          }
      }
      .h1.w1.l2 {
          z-index: -1;
          animation-name: h1w1l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w1l2 {
          0% {
              transform: translate(50%, -75%);
          }
          14% {
              transform: translate(50%, -75%);
          }
          28% {
              transform: translate(100%, -100%);
          }
          43% {
              transform: translate(100%, -150%);
          }
          57% {
              transform: translate(100%, -150%);
          }
          71% {
              transform: translate(50%, -125%);
          }
          85% {
              transform: translate(50%, -75%);
          }
          100% {
              transform: translate(50%, -75%);
          }
      }
      .h1.w1.l3 {
          z-index: -1;
          animation-name: h1w1l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w1l3 {
          0% {
              transform: translate(100%, -50%);
          }
          14% {
              transform: translate(150%, -25%);
          }
          28% {
              transform: translate(200%, -50%);
          }
          43% {
              transform: translate(200%, -100%);
          }
          57% {
              transform: translate(150%, -125%);
          }
          71% {
              transform: translate(100%, -100%);
          }
          85% {
              transform: translate(100%, -50%);
          }
          100% {
              transform: translate(100%, -50%);
          }
      }
      .h1.w2.l1 {
          z-index: -1;
          animation-name: h1w2l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w2l1 {
          0% {
              transform: translate(-50%, -75%);
          }
          14% {
              transform: translate(-100%, -100%);
          }
          28% {
              transform: translate(-100%, -100%);
          }
          43% {
              transform: translate(-100%, -150%);
          }
          57% {
              transform: translate(-50%, -125%);
          }
          71% {
              transform: translate(-50%, -125%);
          }
          85% {
              transform: translate(-50%, -75%);
          }
          100% {
              transform: translate(-50%, -75%);
          }
      }
      .h1.w2.l2 {
          z-index: -1;
          animation-name: h1w2l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w2l2 {
          0% {
              transform: translate(0%, -50%);
          }
          14% {
              transform: translate(0%, -50%);
          }
          28% {
              transform: translate(0%, -50%);
          }
          43% {
              transform: translate(0%, -100%);
          }
          57% {
              transform: translate(0%, -100%);
          }
          71% {
              transform: translate(0%, -100%);
          }
          85% {
              transform: translate(0%, -50%);
          }
          100% {
              transform: translate(0%, -50%);
          }
      }
      .h1.w2.l3 {
          z-index: -1;
          animation-name: h1w2l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w2l3 {
          0% {
              transform: translate(50%, -25%);
          }
          14% {
              transform: translate(100%, 0%);
          }
          28% {
              transform: translate(100%, 0%);
          }
          43% {
              transform: translate(100%, -50%);
          }
          57% {
              transform: translate(50%, -75%);
          }
          71% {
              transform: translate(50%, -75%);
          }
          85% {
              transform: translate(50%, -25%);
          }
          100% {
              transform: translate(50%, -25%);
          }
      }
      .h1.w3.l1 {
          z-index: -1;
          animation-name: h1w3l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w3l1 {
          0% {
              transform: translate(-100%, -50%);
          }
          14% {
              transform: translate(-150%, -75%);
          }
          28% {
              transform: translate(-200%, -50%);
          }
          43% {
              transform: translate(-200%, -100%);
          }
          57% {
              transform: translate(-150%, -75%);
          }
          71% {
              transform: translate(-100%, -100%);
          }
          85% {
              transform: translate(-100%, -50%);
          }
          100% {
              transform: translate(-100%, -50%);
          }
      }
      .h1.w3.l2 {
          z-index: -1;
          animation-name: h1w3l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w3l2 {
          0% {
              transform: translate(-50%, -25%);
          }
          14% {
              transform: translate(-50%, -25%);
          }
          28% {
              transform: translate(-100%, 0%);
          }
          43% {
              transform: translate(-100%, -50%);
          }
          57% {
              transform: translate(-100%, -50%);
          }
          71% {
              transform: translate(-50%, -75%);
          }
          85% {
              transform: translate(-50%, -25%);
          }
          100% {
              transform: translate(-50%, -25%);
          }
      }
      .h1.w3.l3 {
          z-index: -1;
          animation-name: h1w3l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h1w3l3 {
          0% {
              transform: translate(0%, 0%);
          }
          14% {
              transform: translate(50%, 25%);
          }
          28% {
              transform: translate(0%, 50%);
          }
          43% {
              transform: translate(0%, 0%);
          }
          57% {
              transform: translate(-50%, -25%);
          }
          71% {
              transform: translate(0%, -50%);
          }
          85% {
              transform: translate(0%, 0%);
          }
          100% {
              transform: translate(0%, 0%);
          }
      }
      .h2.w1.l1 {
          z-index: -2;
          animation-name: h2w1l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w1l1 {
          0% {
              transform: translate(0%, -50%);
          }
          14% {
              transform: translate(-50%, -75%);
          }
          28% {
              transform: translate(0%, -100%);
          }
          43% {
              transform: translate(0%, -100%);
          }
          57% {
              transform: translate(50%, -75%);
          }
          71% {
              transform: translate(0%, -50%);
          }
          85% {
              transform: translate(0%, -50%);
          }
          100% {
              transform: translate(0%, -50%);
          }
      }
      .h2.w1.l2 {
          z-index: -2;
          animation-name: h2w1l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w1l2 {
          0% {
              transform: translate(50%, -25%);
          }
          14% {
              transform: translate(50%, -25%);
          }
          28% {
              transform: translate(100%, -50%);
          }
          43% {
              transform: translate(100%, -50%);
          }
          57% {
              transform: translate(100%, -50%);
          }
          71% {
              transform: translate(50%, -25%);
          }
          85% {
              transform: translate(50%, -25%);
          }
          100% {
              transform: translate(50%, -25%);
          }
      }
      .h2.w1.l3 {
          z-index: -2;
          animation-name: h2w1l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w1l3 {
          0% {
              transform: translate(100%, 0%);
          }
          14% {
              transform: translate(150%, 25%);
          }
          28% {
              transform: translate(200%, 0%);
          }
          43% {
              transform: translate(200%, 0%);
          }
          57% {
              transform: translate(150%, -25%);
          }
          71% {
              transform: translate(100%, 0%);
          }
          85% {
              transform: translate(100%, 0%);
          }
          100% {
              transform: translate(100%, 0%);
          }
      }
      .h2.w2.l1 {
          z-index: -2;
          animation-name: h2w2l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w2l1 {
          0% {
              transform: translate(-50%, -25%);
          }
          14% {
              transform: translate(-100%, -50%);
          }
          28% {
              transform: translate(-100%, -50%);
          }
          43% {
              transform: translate(-100%, -50%);
          }
          57% {
              transform: translate(-50%, -25%);
          }
          71% {
              transform: translate(-50%, -25%);
          }
          85% {
              transform: translate(-50%, -25%);
          }
          100% {
              transform: translate(-50%, -25%);
          }
      }
      .h2.w2.l2 {
          z-index: -2;
          animation-name: h2w2l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w2l2 {
          0% {
              transform: translate(0%, 0%);
          }
          14% {
              transform: translate(0%, 0%);
          }
          28% {
              transform: translate(0%, 0%);
          }
          43% {
              transform: translate(0%, 0%);
          }
          57% {
              transform: translate(0%, 0%);
          }
          71% {
              transform: translate(0%, 0%);
          }
          85% {
              transform: translate(0%, 0%);
          }
          100% {
              transform: translate(0%, 0%);
          }
      }
      .h2.w2.l3 {
          z-index: -2;
          animation-name: h2w2l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w2l3 {
          0% {
              transform: translate(50%, 25%);
          }
          14% {
              transform: translate(100%, 50%);
          }
          28% {
              transform: translate(100%, 50%);
          }
          43% {
              transform: translate(100%, 50%);
          }
          57% {
              transform: translate(50%, 25%);
          }
          71% {
              transform: translate(50%, 25%);
          }
          85% {
              transform: translate(50%, 25%);
          }
          100% {
              transform: translate(50%, 25%);
          }
      }
      .h2.w3.l1 {
          z-index: -2;
          animation-name: h2w3l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w3l1 {
          0% {
              transform: translate(-100%, 0%);
          }
          14% {
              transform: translate(-150%, -25%);
          }
          28% {
              transform: translate(-200%, 0%);
          }
          43% {
              transform: translate(-200%, 0%);
          }
          57% {
              transform: translate(-150%, 25%);
          }
          71% {
              transform: translate(-100%, 0%);
          }
          85% {
              transform: translate(-100%, 0%);
          }
          100% {
              transform: translate(-100%, 0%);
          }
      }
      .h2.w3.l2 {
          z-index: -2;
          animation-name: h2w3l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w3l2 {
          0% {
              transform: translate(-50%, 25%);
          }
          14% {
              transform: translate(-50%, 25%);
          }
          28% {
              transform: translate(-100%, 50%);
          }
          43% {
              transform: translate(-100%, 50%);
          }
          57% {
              transform: translate(-100%, 50%);
          }
          71% {
              transform: translate(-50%, 25%);
          }
          85% {
              transform: translate(-50%, 25%);
          }
          100% {
              transform: translate(-50%, 25%);
          }
      }
      .h2.w3.l3 {
          z-index: -2;
          animation-name: h2w3l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h2w3l3 {
          0% {
              transform: translate(0%, 50%);
          }
          14% {
              transform: translate(50%, 75%);
          }
          28% {
              transform: translate(0%, 100%);
          }
          43% {
              transform: translate(0%, 100%);
          }
          57% {
              transform: translate(-50%, 75%);
          }
          71% {
              transform: translate(0%, 50%);
          }
          85% {
              transform: translate(0%, 50%);
          }
          100% {
              transform: translate(0%, 50%);
          }
      }
      .h3.w1.l1 {
          z-index: -3;
          animation-name: h3w1l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w1l1 {
          0% {
              transform: translate(0%, 0%);
          }
          14% {
              transform: translate(-50%, -25%);
          }
          28% {
              transform: translate(0%, -50%);
          }
          43% {
              transform: translate(0%, 0%);
          }
          57% {
              transform: translate(50%, 25%);
          }
          71% {
              transform: translate(0%, 50%);
          }
          85% {
              transform: translate(0%, 0%);
          }
          100% {
              transform: translate(0%, 0%);
          }
      }
      .h3.w1.l2 {
          z-index: -3;
          animation-name: h3w1l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w1l2 {
          0% {
              transform: translate(50%, 25%);
          }
          14% {
              transform: translate(50%, 25%);
          }
          28% {
              transform: translate(100%, 0%);
          }
          43% {
              transform: translate(100%, 50%);
          }
          57% {
              transform: translate(100%, 50%);
          }
          71% {
              transform: translate(50%, 75%);
          }
          85% {
              transform: translate(50%, 25%);
          }
          100% {
              transform: translate(50%, 25%);
          }
      }
      .h3.w1.l3 {
          z-index: -3;
          animation-name: h3w1l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w1l3 {
          0% {
              transform: translate(100%, 50%);
          }
          14% {
              transform: translate(150%, 75%);
          }
          28% {
              transform: translate(200%, 50%);
          }
          43% {
              transform: translate(200%, 100%);
          }
          57% {
              transform: translate(150%, 75%);
          }
          71% {
              transform: translate(100%, 100%);
          }
          85% {
              transform: translate(100%, 50%);
          }
          100% {
              transform: translate(100%, 50%);
          }
      }
      .h3.w2.l1 {
          z-index: -3;
          animation-name: h3w2l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w2l1 {
          0% {
              transform: translate(-50%, 25%);
          }
          14% {
              transform: translate(-100%, 0%);
          }
          28% {
              transform: translate(-100%, 0%);
          }
          43% {
              transform: translate(-100%, 50%);
          }
          57% {
              transform: translate(-50%, 75%);
          }
          71% {
              transform: translate(-50%, 75%);
          }
          85% {
              transform: translate(-50%, 25%);
          }
          100% {
              transform: translate(-50%, 25%);
          }
      }
      .h3.w2.l2 {
          z-index: -3;
          animation-name: h3w2l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w2l2 {
          0% {
              transform: translate(0%, 50%);
          }
          14% {
              transform: translate(0%, 50%);
          }
          28% {
              transform: translate(0%, 50%);
          }
          43% {
              transform: translate(0%, 100%);
          }
          57% {
              transform: translate(0%, 100%);
          }
          71% {
              transform: translate(0%, 100%);
          }
          85% {
              transform: translate(0%, 50%);
          }
          100% {
              transform: translate(0%, 50%);
          }
      }
      .h3.w2.l3 {
          z-index: -3;
          animation-name: h3w2l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w2l3 {
          0% {
              transform: translate(50%, 75%);
          }
          14% {
              transform: translate(100%, 100%);
          }
          28% {
              transform: translate(100%, 100%);
          }
          43% {
              transform: translate(100%, 150%);
          }
          57% {
              transform: translate(50%, 125%);
          }
          71% {
              transform: translate(50%, 125%);
          }
          85% {
              transform: translate(50%, 75%);
          }
          100% {
              transform: translate(50%, 75%);
          }
      }
      .h3.w3.l1 {
          z-index: -3;
          animation-name: h3w3l1;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w3l1 {
          0% {
              transform: translate(-100%, 50%);
          }
          14% {
              transform: translate(-150%, 25%);
          }
          28% {
              transform: translate(-200%, 50%);
          }
          43% {
              transform: translate(-200%, 100%);
          }
          57% {
              transform: translate(-150%, 125%);
          }
          71% {
              transform: translate(-100%, 100%);
          }
          85% {
              transform: translate(-100%, 50%);
          }
          100% {
              transform: translate(-100%, 50%);
          }
      }
      .h3.w3.l2 {
          z-index: -3;
          animation-name: h3w3l2;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w3l2 {
          0% {
              transform: translate(-50%, 75%);
          }
          14% {
              transform: translate(-50%, 75%);
          }
          28% {
              transform: translate(-100%, 100%);
          }
          43% {
              transform: translate(-100%, 150%);
          }
          57% {
              transform: translate(-100%, 150%);
          }
          71% {
              transform: translate(-50%, 125%);
          }
          85% {
              transform: translate(-50%, 75%);
          }
          100% {
              transform: translate(-50%, 75%);
          }
      }
      .h3.w3.l3 {
          z-index: -3;
          animation-name: h3w3l3;
          animation-timing-function: ease;
          animation-duration: 3s;
          animation-iteration-count: infinite;
      }
      @keyframes h3w3l3 {
          0% {
              transform: translate(0%, 100%);
          }
          14% {
              transform: translate(50%, 125%);
          }
          28% {
              transform: translate(0%, 150%);
          }
          43% {
              transform: translate(0%, 200%);
          }
          57% {
              transform: translate(-50%, 175%);
          }
          71% {
              transform: translate(0%, 150%);
          }
          85% {
              transform: translate(0%, 100%);
          }
          100% {
              transform: translate(0%, 100%);
          }
      }</style></head><body><noscript><strong>We're sorry but umldesigner doesn't work properly without JavaScript enabled. Please enable it to continue.</strong></noscript><div id="app"><div class="hero__bg" data-v-e855e7d2=""><div class="hero__bg" style="font-family: -apple-system, BlinkMacSystemFont, Roboto, &quot;Segoe UI&quot;, &quot;Fira Sans&quot;, Avenir, &quot;Helvetica Neue&quot;, &quot;Lucida Grande&quot;, sans-serif; height: 100vh; text-align: center; display: flex; flex-direction: column; align-items: center; justify-content: center;" data-v-e855e7d2=""><div data-v-e855e7d2="">
      
      <h1 style="margin-bottom: 0em;">WebSocket API CALL</h1>
      <small style="color: red;">Enter here a uml management rule for a class diagram.</small>
        <form style="margin-top: 2em;" action="" onsubmit="sendMessage(event)">
            <input type="text" id="messageText" autocomplete="off"/>
            <button>Send</button>
        </form>
        <ul id='messages'>
        </ul>
        <script>
            var ws = new WebSocket("ws://localhost:8000/ws/class-diagram-xml");
            ws.onmessage = function(event) {
                var messages = document.getElementById('messages')
                var message = document.createElement('li')
                var content = document.createTextNode(event.data)
                message.appendChild(content)
                messages.appendChild(message)
            };
            function sendMessage(event) {
                var input = document.getElementById("messageText")
                ws.send(input.value)
                input.value = ''
                event.preventDefault()
            }
        </script>
        
      </div></div></div></div></body></html>
"""

@router.get("/class-diagram-xml")
async def get():
    return HTMLResponse(html)

@router.websocket("/ws/class-diagram-xml")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        formated = schemas.UMLText(text=data)
        print(formated)
        result = nlp.toClassDigramXML(formated)
        print(result)
        await websocket.send_text(result.xml)
