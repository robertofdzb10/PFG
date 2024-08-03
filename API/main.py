from fastapi import FastAPI, HTTPException, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from game_logic import TicTacToe
import io

app = FastAPI()

class Click(BaseModel):
    x: int
    y: int

game = TicTacToe(board_size=4)  # Puedes cambiar el tamaño del tablero aquí

app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/click/")
def click_board(click: Click):  
    game_status = game.click_cell(click.x, click.y)
    
    # Print the current state of the board
    print("Current Board State after click:")
    for row in range(game.board_size):
        print(game.board.squares[row * game.board_size:(row + 1) * game.board_size])

    return {"board": game.get_board(), "current_player": game.current_player, "game_over": game.game_over, "status": game_status}

@app.get("/board/image/")
def get_board_image():

    # Impresión del estado actual del tablero
    print("Generating board image with current state:")
    for row in range(game.board_size):
        print(game.board.squares[row * game.board_size:(row + 1) * game.board_size])

    image = game.get_board_image()
    buf = io.BytesIO()
    image.save(buf, format="PNG")
    buf.seek(0)
    return StreamingResponse(buf, media_type="image/png")

@app.post("/reset/")
def reset_game():
    game.reset()
    print("Game reset")
    print("Current Board State after reset:")
    for row in range(game.board_size):
        print(game.board.squares[row * game.board_size:(row + 1) * game.board_size])
    return {"message": "Game reset", "board": game.get_board()}
