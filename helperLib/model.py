from torch import nn
import torch
from torchvision import models


class vanilla_autoencoder(nn.Module):
    def __init__(self) -> None:
        super().__init__()

        # Encoder from vgg16
        vgg16_model = models.vgg16(weights="IMAGENET1K_V1")
        self.encoder_vgg16 = nn.Sequential(*list(vgg16_model.features.children())[:-1])
        for param in self.encoder_vgg16.parameters():
            param.requires_grad = False

        # Decoder
        self.decoder = nn.Sequential(
            nn.Conv2d(
                in_channels=512, out_channels=256, kernel_size=(3, 3), padding="same"
            ),
            nn.ReLU(),
            nn.Conv2d(
                in_channels=256, out_channels=128, kernel_size=(3, 3), padding="same"
            ),
            nn.ReLU(),
            nn.UpsamplingNearest2d(size=(28, 28)),
            nn.Conv2d(
                in_channels=128, out_channels=64, kernel_size=(3, 3), padding="same"
            ),
            nn.ReLU(),
            nn.Conv2d(
                in_channels=64, out_channels=32, kernel_size=(3, 3), padding="same"
            ),
            nn.ReLU(),
            nn.UpsamplingNearest2d(size=(56, 56)),
            nn.Conv2d(
                in_channels=32, out_channels=16, kernel_size=(3, 3), padding="same"
            ),
            nn.ReLU(),
            nn.UpsamplingNearest2d(size=(112, 112)),
            nn.Conv2d(
                in_channels=16, out_channels=2, kernel_size=(3, 3), padding="same"
            ),
            nn.Tanh(),
            nn.UpsamplingNearest2d(size=(224, 224)),
        )

    def forward(self, x):
        x = self.encoder_vgg16(x)
        x = self.decoder(x)
        return x


def getTrainedModel() -> vanilla_autoencoder:
    newModel: vanilla_autoencoder = vanilla_autoencoder()
    checkpoint: dict = torch.load(
        "./model/autoencoder_mse_50epoch.pth", map_location=torch.device("cpu")
    )
    newModel.load_state_dict(checkpoint["model_state_dict"])
    return newModel


if __name__ == "__main__":
    readyModel: vanilla_autoencoder = getTrainedModel()
