# learn.py

from model import ChessNet
from self_play import self_play
from train import train_model
import torch
import os
from torch.utils.tensorboard import SummaryWriter

MODEL_PATH = "model.pth"

def load_or_initialize_model():
    model = ChessNet()
    if os.path.exists(MODEL_PATH):
        model.load_state_dict(torch.load(MODEL_PATH))
        print("Loaded existing model.")
    else:
        print("Initialized new model.")
    return model


def reinforcement_loop(iterations=10, games_per_iter=100, epochs=3):
    writer = SummaryWriter("runs/chess_rl")
    for i in range(iterations):
        print(f"\n=== Training Iteration {i+1}/{iterations} ===")
        model = load_or_initialize_model()
        data = self_play(model, num_games=games_per_iter)
        train_results = train_model(model, data, epochs=epochs)
        writer.add_scalar("Training/Loss_Iteration", sum(train_results['losses']) / len(train_results['losses']), i)
        torch.save(model.state_dict(), MODEL_PATH)
        print(f"Model saved after iteration {i+1}.")
    writer.close()


if __name__ == "__main__":
    reinforcement_loop(iterations=10, games_per_iter=100, epochs=3)